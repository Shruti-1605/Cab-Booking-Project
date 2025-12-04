from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import json
from datetime import datetime
from googlemaps_service import maps_service
from stripe_integration import stripe_service, process_webhook_event

app = FastAPI(title="Advanced Cab Booking API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class BookCab(BaseModel):
    user_name: str
    cab_id: int
    pickup: str
    destination: str

class PromoCode(BaseModel):
    code: str
    discount_percent: float

class WalletTopup(BaseModel):
    user_id: int
    amount: float

class RideReview(BaseModel):
    ride_id: int
    rating: int
    comment: str

# In-memory storage (replace with database)
rides_db = []
wallet_db = {}
promo_codes = {
    "FIRST50": {"discount": 50, "type": "percentage"},
    "SAVE20": {"discount": 20, "type": "fixed"},
    "NEWUSER": {"discount": 30, "type": "percentage"}
}
reviews_db = []

@app.get("/")
def home():
    return {"msg": "Advanced Cab Booking Backend", "version": "2.0"}

@app.get("/cabs")
def get_cabs():
    return [
        {
            "id": 1, 
            "driver_name": "John Doe", 
            "car_model": "Mini Cooper", 
            "price": 10,
            "rating": 4.8,
            "trips": 1250,
            "eta": "3 mins",
            "distance": "0.5 km"
        },
        {
            "id": 2, 
            "driver_name": "Jane Smith", 
            "car_model": "Honda Civic", 
            "price": 15,
            "rating": 4.9,
            "trips": 890,
            "eta": "5 mins", 
            "distance": "1.2 km"
        },
        {
            "id": 3, 
            "driver_name": "Mike Johnson", 
            "car_model": "Toyota SUV", 
            "price": 20,
            "rating": 4.7,
            "trips": 2100,
            "eta": "7 mins",
            "distance": "2.1 km"
        }
    ]

@app.post("/bookings")
def book_cab(data: BookCab):
    # Calculate fare with surge pricing
    base_fare = get_cab_price(data.cab_id)
    surge_multiplier = get_surge_multiplier()
    final_fare = base_fare * surge_multiplier
    
    # Create booking
    booking = {
        "id": len(rides_db) + 1,
        "user_name": data.user_name,
        "cab_id": data.cab_id,
        "pickup": data.pickup,
        "destination": data.destination,
        "fare": final_fare,
        "surge_multiplier": surge_multiplier,
        "status": "confirmed",
        "booking_time": datetime.now().isoformat(),
        "otp": "1234"
    }
    
    rides_db.append(booking)
    
    return {
        "status": "success",
        "message": f"Cab booked successfully for {data.user_name}",
        "booking_id": booking["id"],
        "fare": final_fare,
        "surge_multiplier": surge_multiplier,
        "otp": "1234",
        "driver_eta": "5 mins"
    }

@app.get("/bookings")
def get_bookings():
    return rides_db

@app.get("/bookings/{booking_id}")
def get_booking_details(booking_id: int):
    booking = next((b for b in rides_db if b["id"] == booking_id), None)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return {
        **booking,
        "driver_location": {"lat": 28.6139, "lng": 77.2090},
        "estimated_arrival": "3 mins",
        "trip_status": "driver_assigned"
    }

@app.post("/promo/validate")
def validate_promo(promo: PromoCode):
    if promo.code not in promo_codes:
        raise HTTPException(status_code=400, detail="Invalid promo code")
    
    promo_data = promo_codes[promo.code]
    return {
        "valid": True,
        "discount": promo_data["discount"],
        "type": promo_data["type"],
        "message": f"Promo applied! {promo_data['discount']}% off"
    }

@app.get("/wallet/{user_id}")
def get_wallet_balance(user_id: int):
    balance = wallet_db.get(user_id, 0.0)
    return {
        "user_id": user_id,
        "balance": balance,
        "currency": "INR"
    }

@app.post("/wallet/topup")
def topup_wallet(topup: WalletTopup):
    current_balance = wallet_db.get(topup.user_id, 0.0)
    new_balance = current_balance + topup.amount
    wallet_db[topup.user_id] = new_balance
    
    return {
        "status": "success",
        "message": "Wallet topped up successfully",
        "new_balance": new_balance,
        "transaction_id": f"TXN{len(wallet_db) + 1000}"
    }

@app.post("/reviews")
def submit_review(review: RideReview):
    review_data = {
        "id": len(reviews_db) + 1,
        "ride_id": review.ride_id,
        "rating": review.rating,
        "comment": review.comment,
        "timestamp": datetime.now().isoformat()
    }
    
    reviews_db.append(review_data)
    
    return {
        "status": "success",
        "message": "Review submitted successfully",
        "review_id": review_data["id"]
    }

@app.get("/reviews/{driver_id}")
def get_driver_reviews(driver_id: int):
    # Mock reviews for driver
    return [
        {"rating": 5, "comment": "Excellent service!", "date": "2024-01-15"},
        {"rating": 4, "comment": "Good driver, safe ride", "date": "2024-01-10"},
        {"rating": 5, "comment": "Very punctual", "date": "2024-01-05"}
    ]

@app.get("/fare/estimate")
def get_fare_estimate(pickup: str, destination: str, cab_type: str = "mini", 
                     pickup_lat: float = None, pickup_lng: float = None,
                     drop_lat: float = None, drop_lng: float = None):
    # Use Google Maps for real distance calculation
    if pickup_lat and pickup_lng and drop_lat and drop_lng:
        # Use coordinates if provided
        pickup_coords = f"{pickup_lat},{pickup_lng}"
        destination_coords = f"{drop_lat},{drop_lng}"
        route_data = maps_service.calculate_distance_duration(pickup_coords, destination_coords)
    else:
        # Use addresses
        route_data = maps_service.calculate_distance_duration(pickup, destination)
    
    if route_data:
        distance_km = route_data['distance_meters'] / 1000
        time_minutes = route_data['duration_seconds'] / 60
    else:
        # Fallback to mock data
        distance_km = 8.5
        time_minutes = 25
    
    # Calculate fare using Google Maps service
    base_rates = {"mini": 50, "sedan": 70, "suv": 90}
    base_rate = base_rates.get(cab_type, 50)
    surge_multiplier = get_surge_multiplier()
    
    fare_data = maps_service.calculate_fare(
        distance_km, time_minutes, base_rate, 
        per_km_rate=12, per_minute_rate=2, surge_multiplier=surge_multiplier
    )
    
    return {
        "pickup": pickup,
        "destination": destination,
        "distance_km": round(distance_km, 2),
        "estimated_time": f"{int(time_minutes)} mins",
        "base_fare": fare_data['base_fare'],
        "surge_multiplier": surge_multiplier,
        "final_fare": fare_data['total_fare'],
        "breakdown": {
            "base": fare_data['base_fare'],
            "distance": fare_data['distance_fare'],
            "time": fare_data['time_fare'],
            "surge": fare_data['surge_amount']
        }
    }

@app.get("/notifications/{user_id}")
def get_notifications(user_id: int):
    return [
        {
            "id": 1,
            "title": "Ride Completed",
            "message": "Your ride to Pune has been completed. Rate your driver!",
            "type": "ride_update",
            "timestamp": "2024-01-20T10:30:00",
            "read": False
        },
        {
            "id": 2,
            "title": "Promo Code Available",
            "message": "Use code SAVE20 for ₹20 off on your next ride",
            "type": "promotion",
            "timestamp": "2024-01-19T15:45:00",
            "read": True
        }
    ]

@app.get("/driver/location/{driver_id}")
def get_driver_location(driver_id: int):
    # Mock real-time location
    return {
        "driver_id": driver_id,
        "location": {
            "lat": 28.6139 + (driver_id * 0.001),
            "lng": 77.2090 + (driver_id * 0.001)
        },
        "heading": 45,
        "speed": 35,
        "last_updated": datetime.now().isoformat()
    }

@app.get("/ride/track/{ride_id}")
def track_ride(ride_id: int):
    return {
        "ride_id": ride_id,
        "status": "in_progress",
        "driver_location": {"lat": 28.6139, "lng": 77.2090},
        "pickup_location": {"lat": 28.6129, "lng": 77.2080},
        "destination": {"lat": 28.7041, "lng": 77.1025},
        "estimated_arrival": "12 mins",
        "distance_remaining": "5.2 km"
    }

# Stripe Payment Endpoints
@app.post("/payments/create-intent")
async def create_payment_intent(request: dict):
    """Create Stripe PaymentIntent for ride payment"""
    try:
        payment_intent = await stripe_service.create_payment_intent(
            amount=request['amount'],
            metadata={
                'ride_id': str(request.get('ride_id')),
                'user_id': str(request.get('user_id'))
            }
        )
        return payment_intent
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/payments/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    payload = await request.body()
    signature = request.headers.get('stripe-signature')
    
    try:
        event = stripe_service.verify_webhook_signature(payload, signature)
        await process_webhook_event(event)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/payments/refund")
async def process_refund(request: dict):
    """Process payment refund"""
    try:
        refund = await stripe_service.process_refund(
            payment_intent_id=request['payment_intent_id'],
            amount=request.get('amount')
        )
        return refund
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/payments/methods/{customer_id}")
async def get_payment_methods(customer_id: str):
    """Get customer's saved payment methods"""
    try:
        methods = await stripe_service.get_payment_methods(customer_id)
        return methods
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Helper functions
def get_cab_price(cab_id: int) -> float:
    prices = {1: 10, 2: 15, 3: 20}
    return prices.get(cab_id, 10)

def get_surge_multiplier() -> float:
    # Simple surge logic based on time
    hour = datetime.now().hour
    if 8 <= hour <= 10 or 18 <= hour <= 20:  # Peak hours
        return 1.5
    elif 22 <= hour <= 6:  # Late night
        return 1.3
    return 1.0