# SQLModel implementation for better FastAPI integration
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from geoalchemy2 import Geometry
from sqlalchemy import Column, JSON

# ------------------------
# SQLModel Base Classes
# ------------------------
class UserBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)
    phone: str
    role: str  # rider/driver/admin
    profile_pic: Optional[str] = None
    rating_avg: float = Field(default=0.0)
    auth_provider: str = Field(default="local")
    external_id: Optional[str] = None
    is_active: bool = Field(default=True)

class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    driver_profile: Optional["Driver"] = Relationship(back_populates="user")
    rides_as_rider: List["Ride"] = Relationship(back_populates="rider", sa_relationship_kwargs={"foreign_keys": "Ride.rider_id"})
    rides_as_driver: List["Ride"] = Relationship(back_populates="driver", sa_relationship_kwargs={"foreign_keys": "Ride.driver_id"})
    wallet: Optional["Wallet"] = Relationship(back_populates="user")
    notifications: List["Notification"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    created_at: datetime

# ------------------------
# Driver Model
# ------------------------
class DriverBase(SQLModel):
    user_id: int = Field(foreign_key="users.id")
    license_number: str
    verified: bool = Field(default=False)
    status: str = Field(default="offline")  # active/offline/busy
    socket_id: Optional[str] = None

class Driver(DriverBase, table=True):
    __tablename__ = "drivers"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    vehicle_info: dict = Field(sa_column=Column(JSON))
    current_location: Optional[str] = Field(sa_column=Column(Geometry('POINT'), index=True))
    
    # Relationships
    user: User = Relationship(back_populates="driver_profile")

# ------------------------
# Ride Model
# ------------------------
class RideBase(SQLModel):
    rider_id: int = Field(foreign_key="users.id")
    pickup_address: str
    drop_address: str
    fare_estimate: float
    status: str = Field(default="requested")

class Ride(RideBase, table=True):
    __tablename__ = "rides"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    driver_id: Optional[int] = Field(foreign_key="users.id")
    pickup_point: Optional[str] = Field(sa_column=Column(Geometry('POINT'), index=True))
    drop_point: Optional[str] = Field(sa_column=Column(Geometry('POINT'), index=True))
    fare_actual: Optional[float] = None
    distance_meters: Optional[int] = None
    duration_secs: Optional[int] = None
    driver_eta: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    rider: User = Relationship(back_populates="rides_as_rider", sa_relationship_kwargs={"foreign_keys": "Ride.rider_id"})
    driver: Optional[User] = Relationship(back_populates="rides_as_driver", sa_relationship_kwargs={"foreign_keys": "Ride.driver_id"})
    payment: Optional["Payment"] = Relationship(back_populates="ride")
    reviews: List["Review"] = Relationship(back_populates="ride")

class RideCreate(RideBase):
    pickup_lat: float
    pickup_lng: float
    drop_lat: float
    drop_lng: float

class RideRead(RideBase):
    id: int
    driver_id: Optional[int]
    created_at: datetime

# ------------------------
# Payment Model
# ------------------------
class PaymentBase(SQLModel):
    ride_id: int = Field(foreign_key="rides.id")
    amount: float
    currency: str = Field(default="inr")
    payment_method: str = Field(default="card")
    status: str = Field(default="pending")

class Payment(PaymentBase, table=True):
    __tablename__ = "payments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    stripe_payment_intent_id: Optional[str] = None
    webhook_received: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    ride: Ride = Relationship(back_populates="payment")

# ------------------------
# Wallet Model
# ------------------------
class WalletBase(SQLModel):
    user_id: int = Field(foreign_key="users.id", unique=True)
    balance: float = Field(default=0.0)
    currency: str = Field(default="INR")

class Wallet(WalletBase, table=True):
    __tablename__ = "wallets"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: User = Relationship(back_populates="wallet")
    transactions: List["WalletTransaction"] = Relationship(back_populates="wallet")

# ------------------------
# Wallet Transaction Model
# ------------------------
class WalletTransactionBase(SQLModel):
    wallet_id: int = Field(foreign_key="wallets.id")
    type: str  # credit/debit/refund
    amount: float
    description: str
    reference_id: Optional[str] = None

class WalletTransaction(WalletTransactionBase, table=True):
    __tablename__ = "wallet_transactions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    wallet: Wallet = Relationship(back_populates="transactions")

# ------------------------
# Review Model
# ------------------------
class ReviewBase(SQLModel):
    ride_id: int = Field(foreign_key="rides.id")
    rater_id: int = Field(foreign_key="users.id")
    rated_id: int = Field(foreign_key="users.id")
    rating: int = Field(ge=1, le=5)  # 1-5 stars
    comment: Optional[str] = None

class Review(ReviewBase, table=True):
    __tablename__ = "reviews"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    ride: Ride = Relationship(back_populates="reviews")

# ------------------------
# Promo Code Model
# ------------------------
class PromoCodeBase(SQLModel):
    code: str = Field(unique=True, index=True)
    description: str
    discount_type: str  # percentage/fixed
    discount_value: float
    min_ride_amount: float = Field(default=0.0)
    max_discount: Optional[float] = None
    usage_limit: Optional[int] = None
    used_count: int = Field(default=0)
    valid_from: datetime
    valid_until: datetime
    is_active: bool = Field(default=True)

class PromoCode(PromoCodeBase, table=True):
    __tablename__ = "promo_codes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ------------------------
# Notification Model
# -------------------------
class NotificationBase(SQLModel):
    user_id: int = Field(foreign_key="users.id")
    title: str
    message: str
    type: str  # ride_request/ride_update/payment/system
    read: bool = Field(default=False)

class Notification(NotificationBase, table=True):
    __tablename__ = "notifications"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    data: Optional[dict] = Field(sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: User = Relationship(back_populates="notifications")

