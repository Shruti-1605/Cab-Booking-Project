# Authentication middleware for Clerk/Supabase integration
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
import jwt
import requests

security = HTTPBearer()

def verify_token(token: str = Depends(security)):
    """Verify JWT token - simplified for demo"""
    try:
        # Extract user ID from simple token format: token_userid_email
        if token.credentials.startswith('token_'):
            parts = token.credentials.split('_')
            if len(parts) >= 2:
                return int(parts[1])  # Return user ID
        
        # Fallback for demo
        return 1
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")