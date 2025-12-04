from fastapi import FastAPI, Depends, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import stripe
import json
from typing import Dict
from db import engine, get_db
from models import Base, User, Driver, Ride, Payment
from schemas import *
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from auth import verify_token
from services import get_fare_estimate, get_directions
from admin_routes import router as admin_router
from payment_routes import router as payment_router
from map_routes import router as map_router

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cab Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include admin routes
app.include_router(admin_router)

# Include payment routes
app.include_router(payment_router)

# Include map routes
app.include_router(map_router)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)

manager = ConnectionManager()

@app.post("/api/auth/register")
def register_user(user_data: dict, db: Session = Depends(get_db)):
    """Register new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data['email']).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    user = User(
        name=user_data['name'],
        email=user_data['email'],
        phone=user_data['phone'],
        role=user_data['role'],
        password=user_data['password']  # In production, hash this!
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message": "User registered successfully", "user_id": user.id}

@app.post("/api/auth/login")
def login_user(credentials: dict, db: Session = Depends(get_db)):
    """Login user"""
    user = db.query(User).filter(User.email == credentials['email']).first()
    if not user or user.password != credentials['password']:  # In production, verify hash!
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate token (simplified)
    token = f"token_{user.id}_{user.email}"
    
    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }

@app.get("/api/vehicle-types")
def get_vehicle_types():
    """Get available vehicle types with pricing"""
    from vehicle_types import VEHICLE_TYPES
    return VEHICLE_TYPES

@app.post("/api/auth/session")
def verify_session(token: str, db: Session = Depends(get_db)):
    """Verify token from Clerk/Supabase"""
    try:
        user_id = verify_token(token)
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user_id": user.id, "role": user.role, "name": user.name}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid session")

@app.post("/api/rides/request")
def request_ride(ride_data: RideRequest, user_id: int = Depends(verify_token), db: Session = Depends(get_db)):
    """Create ride request (returns ride id)"""
    directions = get_directions(ride_data.pickup_lat, ride_data.pickup_lng, ride_data.drop_lat, ride_data.drop_lng)
    if not directions:
        raise HTTPException(status_code=400, detail="Unable to calculate route")
    
    fare = get_fare_estimate(directions['distance'], directions['duration'])
    
    ride = Ride(
        rider_id=user_id,
        pickup_lat=ride_data.pickup_lat,
        pickup_lng=ride_data.pickup_lng,
        drop_lat=ride_data.drop_lat,
        drop_lng=ride_data.drop_lng,
        pickup_address=ride_data.pickup_address,
        drop_address=ride_data.drop_address,
        fare_estimate=fare,
        distance_meters=directions['distance'],
        duration_secs=directions['duration']
    )
    db.add(ride)
    db.commit()
    
    return {"ride_id": ride.id}

@app.get("/api/rides/estimate")
def get_fare_estimate_endpoint(origin: str, dest: str):
    """Return fare estimate (calls Google Distance Matrix)"""
    try:
        origin_coords = [float(x) for x in origin.split(',')]
        dest_coords = [float(x) for x in dest.split(',')]
        
        directions = get_directions(origin_coords[0], origin_coords[1], dest_coords[0], dest_coords[1])
        if not directions:
            raise HTTPException(status_code=400, detail="Unable to calculate route")
        
        fare = get_fare_estimate(directions['distance'], directions['duration'])
        
        return {
            "fare_estimate": fare,
            "distance_meters": directions['distance'],
            "duration_seconds": directions['duration']
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/rides/{ride_id}/status")
def get_ride_status(ride_id: int, db: Session = Depends(get_db)):
    """Poll ride status"""
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    return {
        "ride_id": ride.id,
        "status": ride.status,
        "driver_id": ride.driver_id,
        "driver_eta": ride.driver_eta,
        "fare_actual": ride.fare_actual
    }

@app.post("/api/webhooks/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    """Stripe webhook for payment events"""
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, "your_webhook_secret"
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        payment = db.query(Payment).filter(
            Payment.stripe_payment_intent_id == payment_intent['id']
        ).first()
        
        if payment:
            payment.status = "completed"
            payment.webhook_received = True
            
            ride = db.query(Ride).filter(Ride.id == payment.ride_id).first()
            if ride:
                ride.status = "completed"
            
            db.commit()
    
    return {"status": "success"}

@app.websocket("/ws/driver/{driver_id}")
async def driver_websocket(websocket: WebSocket, driver_id: str, db: Session = Depends(get_db)):
    """Driver socket to receive requests and send location"""
    await manager.connect(websocket, f"driver_{driver_id}")
    
    driver = db.query(Driver).filter(Driver.user_id == int(driver_id)).first()
    if driver:
        driver.status = "active"
        driver.socket_id = f"driver_{driver_id}"
        db.commit()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "location_update":
                if driver:
                    driver.current_lat = message["lat"]
                    driver.current_lng = message["lng"]
                    db.commit()
            
            elif message.get("type") == "accept_ride":
                ride_id = message.get("ride_id")
                ride = db.query(Ride).filter(Ride.id == ride_id).first()
                if ride:
                    ride.driver_id = int(driver_id)
                    ride.status = "accepted"
                    db.commit()
                    
                    await manager.send_personal_message(
                        json.dumps({"type": "ride_accepted", "driver_id": driver_id}),
                        f"rider_{ride.rider_id}"
                    )
    
    except WebSocketDisconnect:
        manager.disconnect(f"driver_{driver_id}")
        if driver:
            driver.status = "offline"
            driver.socket_id = None
            db.commit()

@app.websocket("/ws/rider/{rider_id}")
async def rider_websocket(websocket: WebSocket, rider_id: str):
    """Rider socket to watch driver"""
    await manager.connect(websocket, f"rider_{rider_id}")
    
    try:
        while True:
            data = await websocket.receive_text()
    
    except WebSocketDisconnect:
        manager.disconnect(f"rider_{rider_id}")
