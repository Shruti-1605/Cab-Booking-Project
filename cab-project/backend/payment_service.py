from sqlalchemy.orm import Session
from models import Payment, Ride, User
from stripe_integration import stripe_service
from typing import Dict, Optional
import os
from datetime import datetime

class PaymentService:
    def __init__(self):
        self.stripe_service = stripe_service
    
    async def create_ride_payment(self, db: Session, ride_id: int, user_id: int) -> Dict:
        """Create payment for a ride"""
        # Get ride details
        ride = db.query(Ride).filter(Ride.id == ride_id).first()
        if not ride:
            raise ValueError("Ride not found")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Create payment record
        payment = Payment(
            ride_id=ride_id,
            user_id=user_id,
            amount=ride.fare_estimate,
            currency="inr",
            status="pending"
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        # Create Stripe payment intent
        metadata = {
            "ride_id": str(ride_id),
            "user_id": str(user_id),
            "payment_id": str(payment.id)
        }
        
        stripe_result = await self.stripe_service.create_payment_intent(
            amount=ride.fare_estimate,
            currency="inr",
            metadata=metadata
        )
        
        # Update payment with Stripe details
        payment.stripe_payment_intent_id = stripe_result["payment_intent_id"]
        payment.client_secret = stripe_result["client_secret"]
        db.commit()
        
        return {
            "payment_id": payment.id,
            "client_secret": stripe_result["client_secret"],
            "amount": ride.fare_estimate,
            "currency": "inr"
        }
    
    async def confirm_payment(self, db: Session, payment_id: int) -> Dict:
        """Confirm payment completion"""
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise ValueError("Payment not found")
        
        # Confirm with Stripe
        stripe_result = await self.stripe_service.confirm_payment_intent(
            payment.stripe_payment_intent_id
        )
        
        # Update payment status
        payment.status = "completed" if stripe_result["status"] == "succeeded" else "failed"
        payment.completed_at = datetime.utcnow()
        
        # Update ride status if payment successful
        if payment.status == "completed":
            ride = db.query(Ride).filter(Ride.id == payment.ride_id).first()
            if ride:
                ride.payment_status = "paid"
        
        db.commit()
        
        return {
            "payment_id": payment.id,
            "status": payment.status,
            "amount": payment.amount
        }
    
    async def process_refund(self, db: Session, payment_id: int, amount: Optional[float] = None) -> Dict:
        """Process refund for a payment"""
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise ValueError("Payment not found")
        
        if payment.status != "completed":
            raise ValueError("Can only refund completed payments")
        
        # Process refund with Stripe
        refund_result = await self.stripe_service.process_refund(
            payment_intent_id=payment.stripe_payment_intent_id,
            amount=amount
        )
        
        # Update payment status
        payment.status = "refunded"
        payment.refund_amount = refund_result["amount"]
        payment.refunded_at = datetime.utcnow()
        
        db.commit()
        
        return {
            "payment_id": payment.id,
            "refund_amount": refund_result["amount"],
            "status": "refunded"
        }
    
    async def get_payment_status(self, db: Session, payment_id: int) -> Dict:
        """Get payment status"""
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if not payment:
            raise ValueError("Payment not found")
        
        return {
            "payment_id": payment.id,
            "status": payment.status,
            "amount": payment.amount,
            "currency": payment.currency,
            "created_at": payment.created_at,
            "completed_at": payment.completed_at
        }

# Global service instance
payment_service = PaymentService()