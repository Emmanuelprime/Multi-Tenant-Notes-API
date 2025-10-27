import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models.user import User
from app.schemas.user import TokenData

pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=12,
    deprecated="auto"
)
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "JHCJzjhDSHWEYUYUYWEUYCJDHjkhCYscgyC89w8eyiucdksjs")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def get_password_hash(password: str) -> str:
    """Hash a password with automatic truncation for bcrypt"""
    if len(password.encode('utf-8')) > 72:
        # Truncate the password to 72 bytes
        password = password.encode('utf-8')[:72].decode('utf-8', 'ignore')
    
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Password hashing error: {e}")
        # Fallback to a simpler hashing method if bcrypt fails
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

async def authenticate_user(email: str, password: str, organization_id: str):
    """Authenticate user with email, password and organization"""
    try:
        user = await User.find_one({"email": email, "organization_id": organization_id})
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user
    except Exception as e:
        print(f"Authentication error: {e}")
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        org_id: str = payload.get("org_id")
        if user_id is None or org_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, org_id=org_id)
    except JWTError:
        raise credentials_exception
    
    user = await User.get(token_data.user_id)
    if user is None or user.organization_id != token_data.org_id:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user