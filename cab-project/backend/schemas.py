# Pydantic schemas for request/response validation
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RideRequest(BaseModel):
    pickup_lat: float
    pickup_lng: float
    drop_lat: float
    drop_lng: float
    pickup_address: str
    drop_address: str
    vehicle_type: str = "sedan"  # mini/sedan/suv/luxury/auto

class RideResponse(BaseModel):
    ride_id: int
    status: str
    fare_estimate: float
    driver_id: Optional[int] = None
    driver_eta: Optional[int] = None

class FareEstimate(BaseModel):
    pickup_lat: float
    pickup_lng: float
    drop_lat: float
    drop_lng: float

class FareResponse(BaseModel):
    fare_estimate: float
    distance_meters: int
    duration_seconds: int

class DriverLocation(BaseModel):
    lat: float
    lng: float
    heading: Optional[float] = None

class PaymentIntent(BaseModel):
    ride_id: int
    amount: float
    currency: str = "inr"