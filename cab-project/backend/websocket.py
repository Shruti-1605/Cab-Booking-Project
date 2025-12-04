import socketio
import redis
from fastapi import FastAPI
from sqlalchemy.orm import Session
from db import get_db
from models import Driver, Ride

# Create Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins="*")
redis_client = redis.Redis.from_url("redis://localhost:6379")

@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")
    # Update driver status to offline
    db = next(get_db())
    driver = db.query(Driver).filter(Driver.socket_id == sid).first()
    if driver:
        driver.status = "offline"
        driver.socket_id = None
        db.commit()

@sio.event
async def driver_online(sid, data):
    """Driver comes online"""
    db = next(get_db())
    driver = db.query(Driver).filter(Driver.user_id == data['user_id']).first()
    if driver:
        driver.status = "active"
        driver.socket_id = sid
        db.commit()
        await sio.emit('status_updated', {'status': 'online'}, room=sid)

@sio.event
async def update_location(sid, data):
    """Update driver location"""
    db = next(get_db())
    driver = db.query(Driver).filter(Driver.socket_id == sid).first()
    if driver:
        from geoalchemy2.functions import ST_Point
        driver.current_location = ST_Point(data['lng'], data['lat'])
        db.commit()

@sio.event
async def ride_request(sid, data):
    """Send ride request to nearby drivers"""
    # Find nearby drivers and send ride request
    await sio.emit('new_ride_request', data, room='drivers')

def mount_socketio(app: FastAPI):
    """Mount Socket.IO to FastAPI app"""
    socketio_app = socketio.ASGIApp(sio, app)
    return socketio_app