# Comprehensive API testing with pytest and HTTPX
import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool
import json
from datetime import datetime

# Import your app and models
from main import app
from database import get_session
from models_sqlmodel import User, Driver, Ride, Payment, Wallet

# Test database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

def get_test_session():
    with Session(engine) as session:
        yield session

# Override dependency
app.dependency_overrides[get_session] = get_test_session

@pytest.fixture(scope="session")
def setup_database():
    """Setup test database"""
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)

@pytest.fixture
async def async_client():
    """Async test client fixture"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "+1234567890",
        "role": "rider",
        "password": "testpassword123"
    }

@pytest.fixture
def sample_driver_data():
    """Sample driver data for testing"""
    return {
        "name": "Test Driver",
        "email": "driver@example.com",
        "phone": "+1234567891",
        "role": "driver",
        "password": "driverpassword123"
    }

@pytest.fixture
def sample_ride_data():
    """Sample ride data for testing"""
    return {
        "pickup_lat": 28.6139,
        "pickup_lng": 77.2090,
        "drop_lat": 28.7041,
        "drop_lng": 77.1025,
        "pickup_address": "Connaught Place, New Delhi",
        "drop_address": "Red Fort, New Delhi",
        "fare_estimate": 150.0
    }

class TestUserAPI:
    """Test user-related endpoints"""
    
    def test_create_user(self, client, sample_user_data):
        """Test user creation"""
        response = client.post("/api/users/", json=sample_user_data)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["name"] == sample_user_data["name"]
        assert "id" in data
    
    def test_create_duplicate_user(self, client, sample_user_data):
        """Test duplicate user creation fails"""
        # Create first user
        client.post("/api/users/", json=sample_user_data)
        
        # Try to create duplicate
        response = client.post("/api/users/", json=sample_user_data)
        assert response.status_code == 400
    
    def test_get_user(self, client, sample_user_data):
        """Test get user by ID"""
        # Create user
        create_response = client.post("/api/users/", json=sample_user_data)
        user_id = create_response.json()["id"]
        
        # Get user
        response = client.get(f"/api/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["email"] == sample_user_data["email"]
    
    def test_get_nonexistent_user(self, client):
        """Test get nonexistent user returns 404"""
        response = client.get("/api/users/99999")
        assert response.status_code == 404

class TestDriverAPI:
    """Test driver-related endpoints"""
    
    def test_create_driver_profile(self, client, sample_driver_data):
        """Test driver profile creation"""
        # Create user first
        user_response = client.post("/api/users/", json=sample_driver_data)
        user_id = user_response.json()["id"]
        
        # Create driver profile
        driver_data = {
            "user_id": user_id,
            "license_number": "DL123456789",
            "vehicle_info": {
                "make": "Toyota",
                "model": "Camry",
                "year": 2020,
                "license_plate": "ABC123"
            }
        }
        
        response = client.post("/api/drivers/", json=driver_data)
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == user_id
        assert data["license_number"] == "DL123456789"
    
    def test_update_driver_location(self, client, sample_driver_data):
        """Test driver location update"""
        # Create user and driver
        user_response = client.post("/api/users/", json=sample_driver_data)
        user_id = user_response.json()["id"]
        
        driver_data = {
            "user_id": user_id,
            "license_number": "DL123456789",
            "vehicle_info": {"make": "Toyota", "model": "Camry"}
        }
        driver_response = client.post("/api/drivers/", json=driver_data)
        driver_id = driver_response.json()["id"]
        
        # Update location
        location_data = {
            "lat": 28.6139,
            "lng": 77.2090
        }
        
        response = client.put(f"/api/drivers/{driver_id}/location", json=location_data)
        assert response.status_code == 200

class TestRideAPI:
    """Test ride-related endpoints"""
    
    @pytest.fixture
    def setup_ride_test_data(self, client, sample_user_data, sample_driver_data):
        """Setup test data for ride tests"""
        # Create rider
        rider_response = client.post("/api/users/", json=sample_user_data)
        rider_id = rider_response.json()["id"]
        
        # Create driver
        driver_user_data = sample_driver_data.copy()
        driver_user_data["email"] = "driver@test.com"
        driver_response = client.post("/api/users/", json=driver_user_data)
        driver_user_id = driver_response.json()["id"]
        
        # Create driver profile
        driver_profile_data = {
            "user_id": driver_user_id,
            "license_number": "DL987654321",
            "vehicle_info": {"make": "Honda", "model": "Civic"}
        }
        client.post("/api/drivers/", json=driver_profile_data)
        
        return {
            "rider_id": rider_id,
            "driver_user_id": driver_user_id
        }
    
    def test_create_ride_request(self, client, sample_ride_data, setup_ride_test_data):
        """Test ride request creation"""
        ride_data = sample_ride_data.copy()
        ride_data["rider_id"] = setup_ride_test_data["rider_id"]
        
        response = client.post("/api/rides/", json=ride_data)
        assert response.status_code == 201
        data = response.json()
        assert data["rider_id"] == setup_ride_test_data["rider_id"]
        assert data["status"] == "requested"
        assert "id" in data
    
    def test_get_fare_estimate(self, client, sample_ride_data):
        """Test fare estimation"""
        estimate_data = {
            "pickup_lat": sample_ride_data["pickup_lat"],
            "pickup_lng": sample_ride_data["pickup_lng"],
            "drop_lat": sample_ride_data["drop_lat"],
            "drop_lng": sample_ride_data["drop_lng"]
        }
        
        response = client.post("/api/rides/estimate", json=estimate_data)
        assert response.status_code == 200
        data = response.json()
        assert "fare_estimate" in data
        assert "distance_km" in data
        assert "duration_minutes" in data
    
    def test_accept_ride(self, client, sample_ride_data, setup_ride_test_data):
        """Test ride acceptance by driver"""
        # Create ride request
        ride_data = sample_ride_data.copy()
        ride_data["rider_id"] = setup_ride_test_data["rider_id"]
        ride_response = client.post("/api/rides/", json=ride_data)
        ride_id = ride_response.json()["id"]
        
        # Accept ride
        accept_data = {
            "driver_id": setup_ride_test_data["driver_user_id"]
        }
        
        response = client.put(f"/api/rides/{ride_id}/accept", json=accept_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "accepted"
        assert data["driver_id"] == setup_ride_test_data["driver_user_id"]

class TestPaymentAPI:
    """Test payment-related endpoints"""
    
    def test_create_payment_intent(self, client):
        """Test Stripe payment intent creation"""
        payment_data = {
            "amount": 150.0,
            "currency": "inr",
            "ride_id": 1
        }
        
        response = client.post("/api/payments/intent", json=payment_data)
        assert response.status_code == 200
        data = response.json()
        assert "client_secret" in data
        assert "payment_intent_id" in data
        assert data["amount"] == 150.0
    
    def test_webhook_processing(self, client):
        """Test Stripe webhook processing"""
        webhook_data = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "id": "pi_test123",
                    "amount": 15000,  # 150.00 in paise
                    "currency": "inr",
                    "status": "succeeded"
                }
            }
        }
        
        response = client.post("/api/webhooks/stripe", json=webhook_data)
        assert response.status_code == 200

class TestWalletAPI:
    """Test wallet-related endpoints"""
    
    def test_create_wallet(self, client, sample_user_data):
        """Test wallet creation"""
        # Create user
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        # Create wallet
        wallet_data = {
            "user_id": user_id,
            "balance": 100.0
        }
        
        response = client.post("/api/wallets/", json=wallet_data)
        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == user_id
        assert data["balance"] == 100.0
    
    def test_wallet_topup(self, client, sample_user_data):
        """Test wallet top-up"""
        # Create user and wallet
        user_response = client.post("/api/users/", json=sample_user_data)
        user_id = user_response.json()["id"]
        
        wallet_data = {"user_id": user_id, "balance": 50.0}
        wallet_response = client.post("/api/wallets/", json=wallet_data)
        wallet_id = wallet_response.json()["id"]
        
        # Top up wallet
        topup_data = {
            "amount": 100.0,
            "payment_method": "card"
        }
        
        response = client.post(f"/api/wallets/{wallet_id}/topup", json=topup_data)
        assert response.status_code == 200
        data = response.json()
        assert data["new_balance"] == 150.0

@pytest.mark.asyncio
class TestAsyncAPI:
    """Test async endpoints"""
    
    async def test_async_ride_matching(self, async_client):
        """Test async ride matching"""
        matching_data = {
            "pickup_lat": 28.6139,
            "pickup_lng": 77.2090,
            "radius_km": 5.0
        }
        
        response = await async_client.post("/api/rides/match", json=matching_data)
        assert response.status_code == 200
        data = response.json()
        assert "nearby_drivers" in data
    
    async def test_async_location_updates(self, async_client):
        """Test async location updates"""
        location_data = {
            "driver_id": 1,
            "lat": 28.6139,
            "lng": 77.2090,
            "heading": 45.0
        }
        
        response = await async_client.post("/api/drivers/location/bulk", json=[location_data])
        assert response.status_code == 200

class TestPerformance:
    """Performance and load testing"""
    
    def test_concurrent_ride_requests(self, client, sample_user_data, sample_ride_data):
        """Test handling concurrent ride requests"""
        import concurrent.futures
        import threading
        
        # Create multiple users
        users = []
        for i in range(10):
            user_data = sample_user_data.copy()
            user_data["email"] = f"user{i}@test.com"
            response = client.post("/api/users/", json=user_data)
            users.append(response.json()["id"])
        
        def create_ride(user_id):
            ride_data = sample_ride_data.copy()
            ride_data["rider_id"] = user_id
            return client.post("/api/rides/", json=ride_data)
        
        # Create rides concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_ride, user_id) for user_id in users]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        for result in results:
            assert result.status_code == 201

# Test configuration
pytest_plugins = ["pytest_asyncio"]

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])