# Database configuration with asyncpg and psycopg2 support
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Session
import asyncpg
import psycopg2

# Database URLs
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cab_booking.db")
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Sync engine for regular operations
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=300
)

# Async engine for high-performance operations
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True,
    pool_recycle=300
)

# Session makers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session

async def get_async_session():
    """Dependency to get async database session"""
    async with AsyncSessionLocal() as session:
        yield session

# Connection pool for direct asyncpg usage
class AsyncPGPool:
    def __init__(self):
        self.pool = None
    
    async def create_pool(self):
        """Create asyncpg connection pool"""
        if not self.pool:
            self.pool = await asyncpg.create_pool(
                DATABASE_URL,
                min_size=10,
                max_size=20,
                command_timeout=60
            )
        return self.pool
    
    async def close_pool(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()

# Global pool instance
pg_pool = AsyncPGPool()

# Health check function
async def check_database_health():
    """Check database connectivity"""
    try:
        pool = await pg_pool.create_pool()
        async with pool.acquire() as connection:
            await connection.fetchval("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# PostGIS helper functions
def enable_postgis():
    """Enable PostGIS extension"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
        conn.commit()
        cur.close()
        conn.close()
        print("PostGIS extension enabled")
    except Exception as e:
        print(f"Error enabling PostGIS: {e}")

# Geospatial query helpers
async def find_nearby_drivers_query(lat: float, lng: float, radius_km: float = 5.0):
    """Find nearby drivers using PostGIS"""
    query = """
    SELECT d.id, d.user_id, u.name, 
           ST_Distance(d.current_location, ST_Point($3, $2)) * 111.32 as distance_km
    FROM drivers d
    JOIN users u ON d.user_id = u.id
    WHERE d.status = 'active' 
    AND d.current_location IS NOT NULL
    AND ST_DWithin(d.current_location, ST_Point($3, $2), $1 / 111.32)
    ORDER BY distance_km
    LIMIT 10;
    """
    
    pool = await pg_pool.create_pool()
    async with pool.acquire() as connection:
        return await connection.fetch(query, radius_km, lat, lng)

async def update_driver_location(driver_id: int, lat: float, lng: float):
    """Update driver location using PostGIS"""
    query = """
    UPDATE drivers 
    SET current_location = ST_Point($2, $1), 
        updated_at = NOW()
    WHERE id = $3;
    """
    
    pool = await pg_pool.create_pool()
    async with pool.acquire() as connection:
        await connection.execute(query, lat, lng, driver_id)