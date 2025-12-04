from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from typing import Optional, Dict
import stripe
from stripe_integration import stripe_service, process_webhook_event
from payment_service import payment_service
from db import get_db
from sqlalchemy.orm import Session
import os

router = APIRouter(prefix="/api/payments", tags=["payments"])

class PaymentIntentRequest(BaseModel):
    amount: float
    currency: str = "inr"
    ride_id: Optional[int] = None
    user_id: Optional[int] = None

class CustomerRequest(BaseModel):
    email: str
    name: str
    phone: str

class RefundRequest(BaseModel):
    payment_intent_id: str
    amount: Optional[float] = None
    reason: Optional[str] = None

class RidePaymentRequest(BaseModel):
    ride_id: int
    user_id: int

@router.post("/intent")
async def create_payment_intent(request: PaymentIntentRequest):
    """Create payment intent for ride or wallet topup"""
    try:
        metadata = {}
        if request.ride_id:
            metadata["ride_id"] = str(request.ride_id)
        if request.user_id:
            metadata["user_id"] = str(request.user_id)
        
        result = await stripe_service.create_payment_intent(
            amount=request.amount,
            currency=request.currency,
            metadata=metadata
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/customer")
async def create_customer(request: CustomerRequest):
    """Create Stripe customer"""
    try:
        result = await stripe_service.create_customer(
            email=request.email,
            name=request.name,
            phone=request.phone
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/setup-intent/{customer_id}")
async def create_setup_intent(customer_id: str):
    """Create setup intent for saving payment methods"""
    try:
        result = await stripe_service.create_setup_intent(customer_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/methods/{customer_id}")
async def get_payment_methods(customer_id: str):
    """Get customer's saved payment methods"""
    try:
        result = await stripe_service.get_payment_methods(customer_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refund")
async def process_refund(request: RefundRequest):
    """Process refund"""
    try:
        result = await stripe_service.process_refund(
            payment_intent_id=request.payment_intent_id,
            amount=request.amount
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/ride")
async def create_ride_payment(request: RidePaymentRequest, db: Session = Depends(get_db)):
    """Create payment for a ride"""
    try:
        result = await payment_service.create_ride_payment(
            db=db,
            ride_id=request.ride_id,
            user_id=request.user_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/confirm/{payment_id}")
async def confirm_payment(payment_id: int, db: Session = Depends(get_db)):
    """Confirm payment completion"""
    try:
        result = await payment_service.confirm_payment(db=db, payment_id=payment_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status/{payment_id}")
async def get_payment_status(payment_id: int, db: Session = Depends(get_db)):
    """Get payment status"""
    try:
        result = await payment_service.get_payment_status(db=db, payment_id=payment_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refund/{payment_id}")
async def refund_payment(payment_id: int, amount: Optional[float] = None, db: Session = Depends(get_db)):
    """Process refund for a payment"""
    try:
        result = await payment_service.process_refund(
            db=db,
            payment_id=payment_id,
            amount=amount
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    try:
        payload = await request.body()
        signature = request.headers.get("stripe-signature")
        
        if not signature:
            raise HTTPException(status_code=400, detail="Missing signature")
        
        # Verify webhook signature
        event = stripe_service.verify_webhook_signature(payload, signature)
        
        # Process the event
        await process_webhook_event(event)
        
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))