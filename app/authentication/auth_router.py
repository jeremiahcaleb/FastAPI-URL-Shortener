from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db  # ✅ Fixed import path
from app.database.models import DBUser
from app.database.hash import Hash
from app.authentication.authentication import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/token", name="token")
def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticates user and returns a JWT access token.
    """
    user = db.query(DBUser).filter(DBUser.user_name == form_data.username).first()
    
    if not user or not Hash.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )

    access_token = create_access_token(data={"sub": user.user_name})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_name": user.user_name
    }
