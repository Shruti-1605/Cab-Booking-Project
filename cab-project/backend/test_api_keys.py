import os
import googlemaps
import stripe
from dotenv import load_dotenv

load_dotenv()

def test_google_maps_api():
    """Test Google Maps API key"""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    
    if not api_key or api_key == "your_google_maps_api_key":
        print("FAIL: Google Maps API key not set properly")
        return False
    
    try:
        client = googlemaps.Client(key=api_key)
        # Test with a simple geocoding request
        result = client.geocode("New Delhi, India")
        if result:
            print("OK: Google Maps API key is working")
            return True
        else:
            print("FAIL: Google Maps API key invalid - no results")
            return False
    except Exception as e:
        print(f"FAIL: Google Maps API error: {e}")
        return False

def test_stripe_api():
    """Test Stripe API key"""
    api_key = os.getenv("STRIPE_SECRET_KEY")
    
    if not api_key or api_key == "sk_test_your_stripe_secret_key":
        print("FAIL: Stripe API key not set properly")
        return False
    
    try:
        stripe.api_key = api_key
        # Test with a simple API call
        stripe.Account.retrieve()
        print("OK: Stripe API key is working")
        return True
    except Exception as e:
        print(f"FAIL: Stripe API error: {e}")
        return False

def check_env_file():
    """Check if .env file exists and has required keys"""
    env_path = ".env"
    if not os.path.exists(env_path):
        print("FAIL: .env file not found")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    required_keys = [
        "DATABASE_URL",
        "SECRET_KEY", 
        "STRIPE_SECRET_KEY",
        "GOOGLE_MAPS_API_KEY"
    ]
    
    missing_keys = []
    for key in required_keys:
        if key not in content:
            missing_keys.append(key)
    
    if missing_keys:
        print(f"FAIL: Missing keys in .env: {missing_keys}")
        return False
    else:
        print("OK: All required keys found in .env")
        return True

if __name__ == "__main__":
    print("Checking API Keys Configuration...\n")
    
    env_ok = check_env_file()
    google_ok = test_google_maps_api()
    stripe_ok = test_stripe_api()
    
    print(f"\nResults:")
    print(f"Environment file: {'OK' if env_ok else 'FAIL'}")
    print(f"Google Maps API: {'OK' if google_ok else 'FAIL'}")
    print(f"Stripe API: {'OK' if stripe_ok else 'FAIL'}")
    
    if all([env_ok, google_ok, stripe_ok]):
        print("\nAll API keys are configured correctly!")
    else:
        print("\nSome API keys need configuration. Check .env file.")