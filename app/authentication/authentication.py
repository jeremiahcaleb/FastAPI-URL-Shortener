from typing import Optional
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from config import Config
from app.database.db_user import get_user
from app.database import get_db  # ✅ Correct import now

# OAuth2 token dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{Config.URL_PREFIX}/auth/token")


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token with optional expiration.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expire_delta or timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, key=Config.SECRET_KEY, algorithm=Config.ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Validates the access token and retrieves the authenticated user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        user_name: Optional[str] = payload.get("sub")
        if user_name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(user_name=user_name, db=db)
    if not user:
        raise credentials_exception
    return user
