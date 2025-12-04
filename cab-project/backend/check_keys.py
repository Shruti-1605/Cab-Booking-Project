import os
from dotenv import load_dotenv

load_dotenv()

print("Current API Keys:")
print(f"Google Maps: {os.getenv('GOOGLE_MAPS_API_KEY')}")
print(f"Stripe: {os.getenv('STRIPE_SECRET_KEY')}")
print(f"Secret: {os.getenv('SECRET_KEY')}")

# Check if keys are default values
google_key = os.getenv('GOOGLE_MAPS_API_KEY')
stripe_key = os.getenv('STRIPE_SECRET_KEY')

if google_key == "your_google_maps_api_key":
    print("\nGoogle Maps API key is still default placeholder")
else:
    print(f"\nGoogle Maps API key set: {google_key[:10]}...")

if stripe_key == "sk_test_your_stripe_secret_key":
    print("Stripe API key is still default placeholder")
else:
    print(f"Stripe API key set: {stripe_key[:15]}...")