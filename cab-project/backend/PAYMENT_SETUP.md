# Payment Setup Guide - Stripe Integration

## 1. Stripe Account Setup

1. **Create Stripe Account**: https://dashboard.stripe.com/register
2. **Get API Keys**:
   - Go to Developers > API Keys
   - Copy **Secret Key** (starts with `sk_test_` for test mode)
   - Copy **Publishable Key** (starts with `pk_test_` for test mode)

## 2. Environment Variables Setup

Create `.env` file in backend folder:

```env
# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Other configs...
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
DATABASE_URL=sqlite:///./cab_booking.db
```

## 3. Webhook Setup (Optional for testing)

1. **Install Stripe CLI**: https://stripe.com/docs/stripe-cli
2. **Login**: `stripe login`
3. **Forward webhooks**: `stripe listen --forward-to localhost:8000/api/payments/webhooks/stripe`
4. **Copy webhook secret** from CLI output to `.env` file

## 4. Payment Flow

### Create Payment for Ride:
```bash
POST /api/payments/ride
{
    "ride_id": 1,
    "user_id": 1
}
```

### Response:
```json
{
    "payment_id": 1,
    "client_secret": "pi_xxx_secret_xxx",
    "amount": 150.0,
    "currency": "inr"
}
```

### Frontend Integration:
```javascript
// Use client_secret with Stripe.js
const stripe = Stripe('pk_test_your_publishable_key');
const {error} = await stripe.confirmPayment({
    elements,
    clientSecret: 'pi_xxx_secret_xxx',
    confirmParams: {
        return_url: 'https://your-website.com/return'
    }
});
```

## 5. Available Endpoints

- `POST /api/payments/intent` - Create payment intent
- `POST /api/payments/ride` - Create ride payment
- `POST /api/payments/customer` - Create customer
- `GET /api/payments/status/{payment_id}` - Get payment status
- `POST /api/payments/refund/{payment_id}` - Process refund
- `POST /api/payments/webhooks/stripe` - Stripe webhooks

## 6. Test Cards (Stripe Test Mode)

- **Success**: 4242 4242 4242 4242
- **Decline**: 4000 0000 0000 0002
- **3D Secure**: 4000 0025 0000 3155

Use any future date for expiry and any 3-digit CVC.

## 7. Currency Support

Currently configured for INR (Indian Rupees). Amounts are handled in rupees and converted to paise for Stripe (multiply by 100).

## 8. Security Notes

- Never expose secret keys in frontend
- Use HTTPS in production
- Validate webhook signatures
- Store sensitive data securely