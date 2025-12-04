# Security middleware and rate limiting
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
import redis
import time
import hashlib
from typing import Dict, Optional

# Redis client for rate limiting
redis_client = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.window_size = 60  # 1 minute window
    
    def is_allowed(self, identifier: str, endpoint: str) -> bool:
        """Check if request is allowed based on rate limit"""
        key = f"rate_limit:{identifier}:{endpoint}"
        current_time = int(time.time())
        window_start = current_time - (current_time % self.window_size)
        
        try:
            # Get current count for this window
            current_count = redis_client.get(f"{key}:{window_start}")
            current_count = int(current_count) if current_count else 0
            
            if current_count >= self.requests_per_minute:
                return False
            
            # Increment counter
            redis_client.incr(f"{key}:{window_start}")
            redis_client.expire(f"{key}:{window_start}", self.window_size)
            
            return True
            
        except Exception:
            # If Redis is down, allow the request
            return True

# Rate limiter instances
general_limiter = RateLimiter(requests_per_minute=60)
auth_limiter = RateLimiter(requests_per_minute=10)  # Stricter for auth endpoints
booking_limiter = RateLimiter(requests_per_minute=20)  # Moderate for bookings

def get_client_ip(request: Request) -> str:
    """Extract client IP from request"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host

def validate_input_security(data: str) -> bool:
    """Basic input validation for security"""
    # Check for common injection patterns
    dangerous_patterns = [
        "script>", "javascript:", "onload=", "onerror=",
        "SELECT", "INSERT", "UPDATE", "DELETE", "DROP",
        "../", "..\\", "<iframe", "eval("
    ]
    
    data_lower = data.lower()
    return not any(pattern.lower() in data_lower for pattern in dangerous_patterns)

def hash_sensitive_data(data: str) -> str:
    """Hash sensitive data for logging/storage"""
    return hashlib.sha256(data.encode()).hexdigest()[:16]

# CORS security headers
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
}

class SecurityMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Add security headers to response
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    headers = dict(message.get("headers", []))
                    for key, value in SECURITY_HEADERS.items():
                        headers[key.encode()] = value.encode()
                    message["headers"] = list(headers.items())
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)