# Cab Booking Project

A complete cab booking application with FastAPI backend and React frontend.

## Features

- User Authentication (JWT)
- Ride Booking System
- Real-time Driver Tracking
- Payment Integration (Stripe)
- Google Maps Integration
- Reviews & Ratings
- WebSocket Communication

## Tech Stack

**Backend:**
- FastAPI
- SQLAlchemy + PostgreSQL/SQLite
- JWT Authentication
- Stripe Payments
- Google Maps API
- Socket.IO
- Redis

**Frontend:**
- React
- Redux Toolkit
- Tailwind CSS
- Socket.IO Client
- Stripe Elements

## Quick Start

1. **Clone and Setup:**
   ```bash
   cd cab-project
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Update .env file with your API keys
   uvicorn main:app --reload
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Or use the batch script:**
   ```bash
   start_project.bat
   ```

## Environment Variables

Create `.env` file in backend directory:
```
DATABASE_URL=sqlite:///./database.db
SECRET_KEY=your-secret-key-here
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
REDIS_URL=redis://localhost:6379
```

## API Endpoints

- `POST /register` - User registration
- `POST /login` - User login
- `POST /rides/request` - Request a ride
- `GET /rides/nearby-drivers` - Find nearby drivers
- `POST /rides/{ride_id}/accept` - Accept ride (driver)
- `GET /rides/history` - Get ride history
- `POST /payments/create-intent` - Create payment
- `POST /reviews` - Submit review

## Usage

1. Register as rider or driver
2. Riders can book rides by setting pickup/destination
3. Drivers receive ride requests in real-time
4. Track ride progress and make payments
5. Rate and review after ride completion

## Project Structure

```
cab-project/
├── backend/
│   ├── models.py          # Database models
│   ├── main.py           # FastAPI app
│   ├── auth.py           # Authentication
│   ├── services.py       # Business logic
│   ├── schemas.py        # Pydantic models
│   └── websocket.py      # Real-time features
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── services/     # API calls
│   │   └── store/        # Redux store
│   └── package.json
└── README.md
```

## 📸 Project Screenshots

![Screenshot 75](cab-project/Images/Screenshot%20(75).png)
![Screenshot 76](cab-project/Images/Screenshot%20(76).png)
![Screenshot 77](cab-project/Images/Screenshot%20(77).png)
![Screenshot 78](cab-project/Images/Screenshot%20(78).png)
![Screenshot 79](cab-project/Images/Screenshot%20(79).png)
![Screenshot 80](cab-project/Images/Screenshot%20(80).png)
![Screenshot 82](cab-project/Images/Screenshot%20(82).png)
![Screenshot 83](cab-project/Images/Screenshot%20(83).png)
