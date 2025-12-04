from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI()

# In-memory storage
users_db = []
drivers_db = []
rides_db = []
payments_db = []

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BookCab(BaseModel):
    user_name: str
    cab_id: int
    pickup: str
    destination: str

class UserRegister(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    role: str

class UserLogin(BaseModel):
    email: str
    password: str

class RideRequest(BaseModel):
    pickup_lat: float
    pickup_lng: float
    drop_lat: float
    drop_lng: float
    pickup_address: str
    drop_address: str

@app.get("/")
def home():
    return {"msg": "Backend Working"}

# Auth endpoints
@app.post("/api/auth/register")
def register_user(user_data: UserRegister):
    # Add user to database
    user_id = len(users_db) + 1
    new_user = {
        "id": user_id,
        "name": user_data.name,
        "email": user_data.email,
        "phone": user_data.phone,
        "role": user_data.role,
        "status": "Active",
        "rides": 0,
        "created_at": datetime.now().strftime("%Y-%m-%d")
    }
    users_db.append(new_user)
    
    # If driver, add to drivers table
    if user_data.role == "driver":
        driver = {
            "id": len(drivers_db) + 1,
            "name": user_data.name,
            "phone": user_data.phone,
            "vehicle": "Not Set",
            "license": "Not Set",
            "status": "Pending",
            "rating": 0.0
        }
        drivers_db.append(driver)
    
    return {
        "message": "User registered successfully", 
        "user_id": user_id
    }

@app.post("/api/auth/login")
def login_user(credentials: UserLogin):
    # Determine role based on email for demo
    role = "admin" if "admin" in credentials.email else "rider"
    if "driver" in credentials.email:
        role = "driver"
    
    # Find user in database
    user = next((u for u in users_db if u["email"] == credentials.email), None)
    if not user:
        user = {
            "id": 123,
            "name": "Test User",
            "email": credentials.email,
            "role": role
        }
    
    return {
        "access_token": f"token_{user['id']}_{credentials.email}",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": credentials.email,
            "role": role
        }
    }

@app.get("/cabs")
def get_cabs():
    return [
        {"id": 1, "driver_name": "John Doe", "car_model": "Mini Cooper", "price": 10},
        {"id": 2, "driver_name": "Jane Smith", "car_model": "Honda Civic", "price": 15},
        {"id": 3, "driver_name": "Mike Johnson", "car_model": "Toyota SUV", "price": 20}
    ]

@app.post("/bookings")
def book_cab(data: BookCab):
    # Add ride to database
    ride_id = len(rides_db) + 1
    fare = random.randint(100, 500)
    
    new_ride = {
        "id": ride_id,
        "user": data.user_name,
        "driver": "Auto Assigned",
        "pickup": data.pickup,
        "destination": data.destination,
        "fare": fare,
        "status": "Booked",
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    rides_db.append(new_ride)
    
    # Add payment record
    payment = {
        "id": len(payments_db) + 1,
        "ride_id": ride_id,
        "user": data.user_name,
        "amount": fare,
        "method": "Pending",
        "status": "Pending",
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    payments_db.append(payment)
    
    return {
        "status": "success",
        "message": f"Cab booked for {data.user_name}",
        "ride_id": ride_id,
        "fare": fare,
        "pickup": data.pickup,
        "destination": data.destination
    }

# Ride API for frontend integration
@app.post("/api/rides/request")
def request_ride(ride_data: RideRequest):
    ride_id = len(rides_db) + 1
    fare = random.randint(150, 800)
    
    new_ride = {
        "id": ride_id,
        "user": "Current User",
        "driver": "Searching...",
        "pickup": ride_data.pickup_address,
        "destination": ride_data.drop_address,
        "fare": fare,
        "status": "Requested",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    rides_db.append(new_ride)
    
    # Add payment record
    payment = {
        "id": len(payments_db) + 1,
        "ride_id": ride_id,
        "user": "Current User",
        "amount": fare,
        "method": "Pending",
        "status": "Pending",
        "date": datetime.now().strftime("%Y-%m-%d")
    }
    payments_db.append(payment)
    
    return {
        "ride_id": ride_id,
        "fare_estimate": fare,
        "status": "requested"
    }
 
@app.get("/bookings")
def get_bookings():
    return [
        {"id": 1, "cab_id": 2, "user_name": "Test User", "pickup": "Location A", "destination": "Location B", "price": 15, "date": "2024-11-18"}
    ]

# Admin API endpoints
@app.get("/admin/stats")
def get_admin_stats():
    total_revenue = sum([p["amount"] for p in payments_db if p["status"] == "Success"])
    total_revenue = sum([p["amount"] for p in payments_db if p["status"] == "Success"])
    return {
        "total_users": len(users_db) if users_db else 0,
        "total_drivers": len(drivers_db) if drivers_db else 0,
        "total_rides": len(rides_db) if rides_db else 0,
        "total_revenue": total_revenue if total_revenue else 0
    }

@app.get("/admin/users")
def get_users():
    return users_db if users_db else [
        {"id": 1, "name": "Demo User", "email": "demo@example.com", "phone": "+91 9876543210", "status": "Active", "rides": 0}
    ]

@app.get("/admin/drivers")
def get_drivers():
    return drivers_db if drivers_db else [
        {"id": 1, "name": "Demo Driver", "phone": "+91 9876543220", "vehicle": "Demo Car", "license": "DL000000", "status": "Pending", "rating": 0.0}
    ]

@app.get("/admin/rides")
def get_rides():
    return rides_db if rides_db else [
        {"id": 1, "user": "Demo User", "driver": "Demo Driver", "pickup": "Demo Pickup", "destination": "Demo Destination", "fare": 0, "status": "Demo", "date": datetime.now().strftime("%Y-%m-%d")}
    ]

@app.get("/admin/payments")
def get_payments():
    return payments_db if payments_db else [
        {"id": 1, "ride_id": 1, "user": "Demo User", "amount": 0, "method": "Demo", "status": "Demo", "date": datetime.now().strftime("%Y-%m-%d")}
    ]