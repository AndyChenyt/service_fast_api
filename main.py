# main.py
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas import UserBase, UserCreate, UserInDB, Token, Message, ForgotPasswordRequest
from database import get_db, create_db_and_tables, get_user_by_email, create_user as db_create_user
from models import User
from auth import get_password_hash, verify_password, create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI(
    title="FastAPI Auth Service",
    description="API service with Register, Login, and Forgot Password functionality.",
    version="1.0.0"
)

# Initialize database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- Endpoint: User Registration ---
@app.post("/register", response_model=Message, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    
    # Use the create_user function from database.py
    db_create_user(db, email=user.email, hashed_password=hashed_password)
    
    return {"message": "User successfully registered"}

# --- Endpoint: User Login (OAuth2PasswordRequestForm) ---
@app.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return an access token.
    """
    user = get_user_by_email(db, email=form_data.username)
    
    # Check if user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active (optional, but good practice)
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- Endpoint: Forgot Password (Simulation) ---
@app.post("/forgot-password", response_model=Message)
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Simulates sending a password reset link to the user's email.
    """
    user = get_user_by_email(db, email=request.email)
    
    # For security, we return a success message even if the user is not found
    # to prevent email enumeration attacks.
    if user:
        # In a real application, you would:
        # 1. Generate a secure, time-limited token.
        # 2. Store the token and its expiry time in the database associated with the user.
        # 3. Send an email to the user with a link containing the token.
        print(f"--- SIMULATION: Password reset link sent to {request.email} ---")
    
    return {"message": "If the email is registered, a password reset link has been sent."}

# --- Endpoint: Protected Route (Example) ---
@app.get("/users/me", response_model=UserBase)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Retrieve the current authenticated user's information.
    Requires a valid JWT in the Authorization header.
    """
    # current_user is a SQLAlchemy model instance, which Pydantic can read directly
    return current_user
