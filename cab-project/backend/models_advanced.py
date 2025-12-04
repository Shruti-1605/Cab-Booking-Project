# Week 2 Advanced Models - Promo codes, Wallet, Receipts
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

# ------------------------
# 8. Wallet Table
# ------------------------
class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="INR")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", backref="wallet")

# ------------------------
# 9. Wallet Transactions Table
# ------------------------
class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    type = Column(String, nullable=False)  # credit/debit/refund
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    reference_id = Column(String, nullable=True)  # ride_id, payment_id, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    wallet = relationship("Wallet", backref="transactions")

# ------------------------
# 10. Promo Codes Table
# ------------------------
class PromoCode(Base):
    __tablename__ = "promo_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=False)
    discount_type = Column(String, nullable=False)  # percentage/fixed
    discount_value = Column(Float, nullable=False)
    min_ride_amount = Column(Float, default=0.0)
    max_discount = Column(Float, nullable=True)
    usage_limit = Column(Integer, nullable=True)
    used_count = Column(Integer, default=0)
    valid_from = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# ------------------------
# 11. Promo Usage Table
# ------------------------
class PromoUsage(Base):
    __tablename__ = "promo_usage"

    id = Column(Integer, primary_key=True, index=True)
    promo_id = Column(Integer, ForeignKey("promo_codes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False)
    discount_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    promo = relationship("PromoCode", backref="usage_history")
    user = relationship("User", backref="promo_usage")
    ride = relationship("Ride", backref="promo_applied")

# ------------------------
# 12. Receipts Table
# ------------------------
class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False, unique=True)
    receipt_number = Column(String, unique=True, nullable=False)
    pdf_path = Column(String, nullable=True)
    email_sent = Column(Boolean, default=False)
    generated_at = Column(DateTime, default=datetime.utcnow)
    
    ride = relationship("Ride", backref="receipt")

# ------------------------
# 13. Rate Limiting Table
# ------------------------
class RateLimit(Base):
    __tablename__ = "rate_limits"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, nullable=False, index=True)  # IP or user_id
    endpoint = Column(String, nullable=False)
    request_count = Column(Integer, default=1)
    window_start = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)