# Real-time Socket.IO server implementation
import socketio
import asyncio
import json
from typing import Dict, Set
import redis.asyncio as redis
from database import update_driver_location, find_nearby_drivers_query

# Create Socket.IO server
sio = socketio.AsyncServer(
    cors_allowed_origins="*",
    async_mode='asgi',
    logger=True,
    engineio_logger=True
)

# Redis client for pub/sub
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# In-memory storage for active connections
active_drivers: Dict[str, str] = {}  # driver_id -> socket_id
active_riders: Dict[str, str] = {}   # rider_id -> socket_id
driver_locations: Dict[str, Dict] = {}  # driver_id -> {lat, lng, timestamp}

class RealTimeManager:
    def __init__(self):
        self.rooms = {
            'drivers': set(),
            'riders': set(),
            'admins': set()
        }
    
    async def add_to_room(self, sid: str, room: str, user_id: str):
        """Add user to specific room"""
        await sio.enter_room(sid, room)
        self.rooms[room].add(user_id)
        
        if room == 'drivers':
            active_drivers[user_id] = sid
        elif room == 'riders':
            active_riders[user_id] = sid
    
    async def remove_from_room(self, sid: str, room: str, user_id: str):
        """Remove user from room"""
        await sio.leave_room(sid, room)
        if user_id in self.rooms[room]:
            self.rooms[room].remove(user_id)
        
        if room == 'drivers' and user_id in active_drivers:
            del active_drivers[user_id]
        elif room == 'riders' and user_id in active_riders:
            del active_riders[user_id]

rt_manager = RealTimeManager()

# Socket.IO Event Handlers
@sio.event
async def connect(sid, environ, auth):
    """Handle client connection"""
    print(f"Client {sid} connected")
    await sio.emit('connected', {'status': 'success'}, room=sid)

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    print(f"Client {sid} disconnected")
    
    # Remove from all rooms
    for user_id, socket_id in list(active_drivers.items()):
        if socket_id == sid:
            await rt_manager.remove_from_room(sid, 'drivers', user_id)
            # Update driver status to offline
            await redis_client.hset(f"driver:{user_id}", "status", "offline")
            break
    
    for user_id, socket_id in list(active_riders.items()):
        if socket_id == sid:
            await rt_manager.remove_from_room(sid, 'riders', user_id)
            break

@sio.event
async def join_as_driver(sid, data):
    """Driver joins the system"""
    driver_id = data.get('driver_id')
    if not driver_id:
        await sio.emit('error', {'message': 'Driver ID required'}, room=sid)
        return
    
    await rt_manager.add_to_room(sid, 'drivers', driver_id)
    
    # Update driver status
    await redis_client.hset(f"driver:{driver_id}", mapping={
        "status": "active",
        "socket_id": sid,
        "last_seen": asyncio.get_event_loop().time()
    })
    
    await sio.emit('driver_status', {
        'status': 'active',
        'message': 'Successfully joined as driver'
    }, room=sid)

@sio.event
async def join_as_rider(sid, data):
    """Rider joins the system"""
    rider_id = data.get('rider_id')
    if not rider_id:
        await sio.emit('error', {'message': 'Rider ID required'}, room=sid)
        return
    
    await rt_manager.add_to_room(sid, 'riders', rider_id)
    
    await sio.emit('rider_status', {
        'status': 'active',
        'message': 'Successfully joined as rider'
    }, room=sid)

@sio.event
async def update_location(sid, data):
    """Update driver location"""
    driver_id = data.get('driver_id')
    lat = data.get('lat')
    lng = data.get('lng')
    
    if not all([driver_id, lat, lng]):
        await sio.emit('error', {'message': 'Invalid location data'}, room=sid)
        return
    
    # Update location in database
    try:
        await update_driver_location(driver_id, lat, lng)
        
        # Store in Redis for quick access
        location_data = {
            'lat': lat,
            'lng': lng,
            'timestamp': asyncio.get_event_loop().time(),
            'driver_id': driver_id
        }
        
        await redis_client.hset(f"driver_location:{driver_id}", mapping=location_data)
        driver_locations[driver_id] = location_data
        
        # Publish location update
        await redis_client.publish('driver_locations', json.dumps(location_data))
        
        await sio.emit('location_updated', {'status': 'success'}, room=sid)
        
    except Exception as e:
        await sio.emit('error', {'message': f'Failed to update location: {str(e)}'}, room=sid)

@sio.event
async def request_ride(sid, data):
    """Handle ride request from rider"""
    rider_id = data.get('rider_id')
    pickup_lat = data.get('pickup_lat')
    pickup_lng = data.get('pickup_lng')
    
    if not all([rider_id, pickup_lat, pickup_lng]):
        await sio.emit('error', {'message': 'Invalid ride request data'}, room=sid)
        return
    
    try:
        # Find nearby drivers
        nearby_drivers = await find_nearby_drivers_query(pickup_lat, pickup_lng, 5.0)
        
        if not nearby_drivers:
            await sio.emit('no_drivers', {
                'message': 'No drivers available in your area'
            }, room=sid)
            return
        
        # Send ride request to nearby drivers
        ride_request = {
            'ride_id': data.get('ride_id'),
            'rider_id': rider_id,
            'pickup_lat': pickup_lat,
            'pickup_lng': pickup_lng,
            'pickup_address': data.get('pickup_address'),
            'drop_address': data.get('drop_address'),
            'fare_estimate': data.get('fare_estimate')
        }
        
        for driver in nearby_drivers:
            driver_id = str(driver['user_id'])
            if driver_id in active_drivers:
                driver_sid = active_drivers[driver_id]
                await sio.emit('ride_request', ride_request, room=driver_sid)
        
        await sio.emit('ride_request_sent', {
            'message': f'Ride request sent to {len(nearby_drivers)} nearby drivers'
        }, room=sid)
        
    except Exception as e:
        await sio.emit('error', {'message': f'Failed to process ride request: {str(e)}'}, room=sid)

@sio.event
async def accept_ride(sid, data):
    """Driver accepts ride request"""
    driver_id = data.get('driver_id')
    ride_id = data.get('ride_id')
    rider_id = data.get('rider_id')
    
    if not all([driver_id, ride_id, rider_id]):
        await sio.emit('error', {'message': 'Invalid ride acceptance data'}, room=sid)
        return
    
    # Notify rider about ride acceptance
    if rider_id in active_riders:
        rider_sid = active_riders[rider_id]
        await sio.emit('ride_accepted', {
            'ride_id': ride_id,
            'driver_id': driver_id,
            'driver_location': driver_locations.get(driver_id, {})
        }, room=rider_sid)
    
    # Notify other drivers that ride is taken
    for other_driver_id, other_sid in active_drivers.items():
        if other_driver_id != driver_id:
            await sio.emit('ride_taken', {'ride_id': ride_id}, room=other_sid)
    
    await sio.emit('ride_acceptance_confirmed', {
        'ride_id': ride_id,
        'status': 'accepted'
    }, room=sid)

@sio.event
async def ride_status_update(sid, data):
    """Update ride status (started, completed, etc.)"""
    ride_id = data.get('ride_id')
    status = data.get('status')
    rider_id = data.get('rider_id')
    driver_id = data.get('driver_id')
    
    # Notify both rider and driver
    status_update = {
        'ride_id': ride_id,
        'status': status,
        'timestamp': asyncio.get_event_loop().time()
    }
    
    if rider_id in active_riders:
        await sio.emit('ride_status', status_update, room=active_riders[rider_id])
    
    if driver_id in active_drivers:
        await sio.emit('ride_status', status_update, room=active_drivers[driver_id])

# Background task for cleanup
async def cleanup_inactive_connections():
    """Clean up inactive connections periodically"""
    while True:
        current_time = asyncio.get_event_loop().time()
        
        # Check for inactive drivers
        for driver_id in list(active_drivers.keys()):
            last_seen = await redis_client.hget(f"driver:{driver_id}", "last_seen")
            if last_seen and (current_time - float(last_seen)) > 300:  # 5 minutes
                # Mark as offline
                await redis_client.hset(f"driver:{driver_id}", "status", "offline")
        
        await asyncio.sleep(60)  # Run every minute

# Start cleanup task
asyncio.create_task(cleanup_inactive_connections())

# Create ASGI app
socket_app = socketio.ASGIApp(sio)