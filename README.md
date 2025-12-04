# 🚕 Cab Booking System

A full-stack cab booking application with real-time features, built using **FastAPI** (Backend) and **React** (Frontend).

## 🌟 Features

### 👥 Multi-Role System
- **Rider Dashboard** - Book rides, track status, make payments
- **Driver Dashboard** - Accept rides, manage availability, track earnings
- **Admin Panel** - Manage users, drivers, rides, and payments

### 🚗 Core Functionality
- **User Registration & Authentication** - Secure login/signup system
- **Real-time Ride Booking** - Instant ride requests with fare estimation
- **Interactive Maps** - Leaflet integration with route calculation
- **Payment Processing** - Multiple payment methods (Card, UPI, Wallet, Cash)
- **Live Data Management** - Real-time updates in admin panel

### 📊 Admin Features
- **Dashboard Analytics** - Users, drivers, rides, and revenue stats
- **User Management** - View and manage registered users
- **Driver Management** - Verify drivers and track performance
- **Ride Monitoring** - Track all rides and their status
- **Payment Tracking** - Monitor all transactions

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **SQLAlchemy** - Database ORM
- **Stripe** - Payment processing
- **WebSocket** - Real-time communication

### Frontend
- **React** - UI library
- **Redux Toolkit** - State management
- **Tailwind CSS** - Styling
- **Leaflet** - Interactive maps
- **Axios** - HTTP client

### Database
- **SQLite** - Development database
- **PostgreSQL** - Production ready

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/cab-booking-system.git
cd cab-booking-system
```

2. **Backend Setup**
```bash
cd cab-project/backend
pip install fastapi uvicorn sqlalchemy pydantic python-multipart
python -m uvicorn main_simple:app --reload --port 8000
```

3. **Frontend Setup**
```bash
cd cab-project/frontend
npm install
npm start
```

### 🌐 Access URLs
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 👤 User Roles & Access

### 🚗 Rider
- Register with any email
- Book rides and make payments
- Track ride status

### 🚕 Driver
- Register with email containing "driver"
- Go online/offline
- Accept ride requests
- Track earnings

### 👨‍💼 Admin
- Register with email containing "admin"
- Access complete admin panel
- Manage all users and data

## 📱 Usage Examples

### Register as Admin
```
Email: admin@test.com
Password: 123456
Role: Admin
```

### Register as Driver
```
Email: driver@test.com
Password: 123456
Role: Driver
```

### Register as Rider
```
Email: rider@test.com
Password: 123456
Role: Rider
```

## 🗂️ Project Structure

```
cab-booking-system/
├── cab-project/
│   ├── backend/
│   │   ├── main_simple.py      # Main FastAPI application
│   │   ├── models.py           # Database models
│   │   ├── auth.py             # Authentication logic
│   │   └── requirements.txt    # Python dependencies
│   └── frontend/
│       ├── src/
│       │   ├── components/     # React components
│       │   ├── services/       # API services
│       │   └── store/          # Redux store
│       └── package.json        # Node dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login

### Rides
- `POST /api/rides/request` - Request a ride
- `GET /api/rides/history` - Get ride history

### Admin
- `GET /admin/stats` - Dashboard statistics
- `GET /admin/users` - All users
- `GET /admin/drivers` - All drivers
- `GET /admin/rides` - All rides
- `GET /admin/payments` - All payments

## 🎯 Key Features Implemented

✅ **User Authentication** - Secure login/register system  
✅ **Role-based Access** - Rider, Driver, Admin dashboards  
✅ **Real-time Booking** - Instant ride requests  
✅ **Map Integration** - Interactive maps with routing  
✅ **Payment System** - Multiple payment methods  
✅ **Admin Panel** - Complete management system  
✅ **Responsive Design** - Mobile-friendly interface  
✅ **Live Data** - Real-time updates across all modules  

## 🔮 Future Enhancements

- 🌍 **GPS Tracking** - Real-time driver location
- 📱 **Mobile App** - React Native implementation  
- 🔔 **Push Notifications** - Real-time alerts
- 📈 **Analytics Dashboard** - Advanced reporting
- 🤖 **AI Integration** - Smart route optimization
- 💬 **Chat System** - Driver-rider communication

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Developer

**Your Name**  
📧 Email: your.email@example.com  
🔗 LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)  
🐙 GitHub: [Your GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- FastAPI for the amazing backend framework
- React team for the powerful frontend library
- Leaflet for the interactive maps
- Stripe for payment processing
- All open-source contributors

---

⭐ **Star this repository if you found it helpful!**

🐛 **Found a bug?** [Create an issue](https://github.com/your-username/cab-booking-system/issues)

💡 **Have suggestions?** [Start a discussion](https://github.com/your-username/cab-booking-system/discussions)