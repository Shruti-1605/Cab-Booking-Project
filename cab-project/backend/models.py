from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

# ------------------------
# 1. Users Table
# ------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=False)
    role = Column(String, nullable=False)  # rider/driver/admin
    profile_pic = Column(String, nullable=True)
    rating_avg = Column(Float, default=0.0)
    password = Column(String, nullable=False)
    auth_provider = Column(String, default="local")  # local/clerk/supabase
    external_id = Column(String, nullable=True)  # external auth provider ID
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ------------------------
# 2. Drivers Table
# ------------------------
class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_info = Column(JSON, nullable=False)  # vehicle details
    vehicle_type = Column(String, default="sedan")  # mini/sedan/suv/luxury/auto
    license_number = Column(String, nullable=False)
    verified = Column(Boolean, default=False)
    current_lat = Column(Float, nullable=True)
    current_lng = Column(Float, nullable=True)
    status = Column(String, default="offline")  # active/offline/busy
    socket_id = Column(String, nullable=True)  # for real-time updates
    
    user = relationship("User", backref="driver_profile")


# ------------------------
# 3. Rides Table
# ------------------------
class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    rider_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    pickup_lat = Column(Float, nullable=False)
    pickup_lng = Column(Float, nullable=False)
    drop_lat = Column(Float, nullable=False)
    drop_lng = Column(Float, nullable=False)
    status = Column(String, default="requested")  # requested/accepted/in_progress/completed/cancelled
    fare_estimate = Column(Float, nullable=False)
    fare_actual = Column(Float, nullable=True)
    distance_meters = Column(Integer, nullable=True)
    duration_secs = Column(Integer, nullable=True)
    pickup_address = Column(String, nullable=True)
    drop_address = Column(String, nullable=True)
    vehicle_type = Column(String, default="sedan")  # mini/sedan/suv/luxury/auto
    driver_eta = Column(Integer, nullable=True)  # seconds
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    rider = relationship("User", foreign_keys=[rider_id], backref="rides_as_rider")
    driver = relationship("User", foreign_keys=[driver_id], backref="rides_as_driver")


# ------------------------
# 4. Payments Table
# ------------------------
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False)
    stripe_payment_intent_id = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="usd")
    payment_method = Column(String, default="card")  # card/cash/wallet
    status = Column(String, default="pending")  # pending/completed/failed/refunded
    webhook_received = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    ride = relationship("Ride", backref="payment")


# ------------------------
# 5. Reviews Table
# ------------------------
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False)
    rater_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rated_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    ride = relationship("Ride", backref="reviews")
    rater = relationship("User", foreign_keys=[rater_id], backref="reviews_given")
    rated = relationship("User", foreign_keys=[rated_id], backref="reviews_received")


# ------------------------
# 6. Notifications Table
# ------------------------
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String, nullable=False)  # ride_request/ride_update/payment/system
    read = Column(Boolean, default=False)
    data = Column(JSON, nullable=True)  # additional data
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", backref="notifications")


# ------------------------
# 7. Ride Tracking Table
# ------------------------
class RideTracking(Base):
    __tablename__ = "ride_tracking"

    id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False)
    driver_lat = Column(Float, nullable=False)
    driver_lng = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    ride = relationship("Ride", backref="tracking_points")