# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, User
from typing import Generator
import os

# --- Configuration ---
# Use a default connection string for demonstration. 
# In a real application, use environment variables for security.
# Format: "postgresql://user:password@host:port/dbname"
# Example for local development: "postgresql://postgres:mysecretpassword@localhost/fastapi_db"
# We will use a SQLite in-memory database for testing simplicity in the sandbox, 
# but the structure is set up for PostgreSQL.
# For PostgreSQL, change the line below to the actual connection string.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {},
    pool_pre_ping=True
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Database Dependency ---
def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get a database session.
    It will close the session after the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Utility to create tables (for initial setup) ---
def create_db_and_tables():
    """Creates all tables defined in Base metadata."""
    Base.metadata.create_all(bind=engine)

# --- CRUD Operations (Simplified for FastAPI Dependency Injection) ---

def get_user_by_email(db: Session, email: str) -> User | None:
    """Retrieve a user by email."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, hashed_password: str) -> User:
    """Add a new user to the database."""
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(db: Session, user: User, new_hashed_password: str) -> User:
    """Update user's password."""
    user.hashed_password = new_hashed_password
    db.commit()
    db.refresh(user)
    return user
