# Stripe payment integration
import stripe
import os
from typing import Dict, Optional
from fastapi import HTTPException
import asyncio
import aiohttp

# Configure Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

class StripePaymentService:
    def __init__(self):
        self.api_key = stripe.api_key
    
    async def create_payment_intent(
        self, 
        amount: float, 
        currency: str = "inr",
        metadata: Optional[Dict] = None
    ) -> Dict:
        """Create Stripe PaymentIntent"""
        try:
            # Convert to smallest currency unit (paise for INR)
            amount_in_paise = int(amount * 100)
            
            payment_intent = stripe.PaymentIntent.create(
                amount=amount_in_paise,
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            
            return {
                "client_secret": payment_intent.client_secret,
                "payment_intent_id": payment_intent.id,
                "amount": amount,
                "currency": currency,
                "status": payment_intent.status
            }
            
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")
    
    async def confirm_payment_intent(self, payment_intent_id: str) -> Dict:
        """Confirm payment intent"""
        try:
            payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)
            return {
                "id": payment_intent.id,
                "status": payment_intent.status,
                "amount": payment_intent.amount / 100,  # Convert back to rupees
                "currency": payment_intent.currency
            }
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=f"Payment confirmation failed: {str(e)}")
    
    async def create_customer(self, email: str, name: str, phone: str) -> Dict:
        """Create Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                phone=phone,
                metadata={
                    'platform': 'cab_booking'
                }
            )
            
            return {
                "customer_id": customer.id,
                "email": customer.email,
                "name": customer.name
            }
            
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=f"Customer creation failed: {str(e)}")
    
    async def create_setup_intent(self, customer_id: str) -> Dict:
        """Create SetupIntent for saving payment methods"""
        try:
            setup_intent = stripe.SetupIntent.create(
                customer=customer_id,
                payment_method_types=['card'],
            )
            
            return {
                "client_secret": setup_intent.client_secret,
                "setup_intent_id": setup_intent.id
            }
            
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=f"Setup intent creation failed: {str(e)}")
    
    async def get_payment_methods(self, customer_id: str) -> Dict:
        """Get customer's saved payment methods"""
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type="card",
            )
            
            return {
                "payment_methods": [
                    {
                        "id": pm.id,
                        "card": {
                            "brand": pm.card.brand,
                            "last4": pm.card.last4,
                            "exp_month": pm.card.exp_month,
                            "exp_year": pm.card.exp_year
                        }
                    }
                    for pm in payment_methods.data
                ]
            }
            
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch payment methods: {str(e)}")
    
    async def process_refund(self, payment_intent_id: str, amount: Optional[float] = None) -> Dict:
        """Process refund for a payment"""
        try:
            refund_data = {"payment_intent": payment_intent_id}
            
            if amount:
                refund_data["amount"] = int(amount * 100)  # Convert to paise
            
            refund = stripe.Refund.create(**refund_data)
            
            return {
                "refund_id": refund.id,
                "amount": refund.amount / 100,  # Convert back to rupees
                "status": refund.status,
                "reason": refund.reason
            }
            
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=f"Refund failed: {str(e)}")
    
    async def create_transfer(self, amount: float, destination_account: str, metadata: Dict = None) -> Dict:
        """Create transfer to driver's account (for marketplace model)"""
        try:
            transfer = stripe.Transfer.create(
                amount=int(amount * 100),  # Convert to paise
                currency="inr",
                destination=destination_account,
                metadata=metadata or {}
            )
            
            return {
                "transfer_id": transfer.id,
                "amount": transfer.amount / 100,
                "destination": transfer.destination,
                "status": "succeeded"
            }
            
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=f"Transfer failed: {str(e)}")
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> Dict:
        """Verify Stripe webhook signature"""
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, STRIPE_WEBHOOK_SECRET
            )
            return event
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")

# Global service instance
stripe_service = StripePaymentService()

# Webhook event handlers
async def handle_payment_succeeded(event_data: Dict):
    """Handle successful payment"""
    payment_intent = event_data['object']
    
    # Update payment status in database
    # Send confirmation to user
    # Update ride status
    # Trigger receipt generation
    
    print(f"Payment succeeded: {payment_intent['id']}")

async def handle_payment_failed(event_data: Dict):
    """Handle failed payment"""
    payment_intent = event_data['object']
    
    # Update payment status in database
    # Notify user of failure
    # Cancel ride if applicable
    
    print(f"Payment failed: {payment_intent['id']}")

# Webhook event mapping
WEBHOOK_HANDLERS = {
    'payment_intent.succeeded': handle_payment_succeeded,
    'payment_intent.payment_failed': handle_payment_failed,
}

async def process_webhook_event(event: Dict):
    """Process incoming webhook event"""
    event_type = event['type']
    
    if event_type in WEBHOOK_HANDLERS:
        await WEBHOOK_HANDLERS[event_type](event['data'])
    else:
        print(f"Unhandled webhook event: {event_type}")

# Utility functions for common payment flows
async def process_ride_payment(ride_id: int, amount: float, customer_id: str) -> Dict:
    """Complete payment flow for a ride"""
    metadata = {
        "ride_id": str(ride_id),
        "service": "cab_booking"
    }
    
    return await stripe_service.create_payment_intent(
        amount=amount,
        metadata=metadata
    )

async def process_wallet_topup(user_id: int, amount: float, customer_id: str) -> Dict:
    """Process wallet top-up payment"""
    metadata = {
        "user_id": str(user_id),
        "type": "wallet_topup"
    }
    
    return await stripe_service.create_payment_intent(
        amount=amount,
        metadata=metadata
    )