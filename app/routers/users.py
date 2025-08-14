from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas import UserDetails, UserDisplay
from app.database import get_db, db_user
from app.database.models import DBUser
from app.authentication.authentication import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post(
    "",
    response_model=UserDisplay,
    status_code=status.HTTP_201_CREATED,
    name="create_user",
    summary="Create a new user account",
    response_description="The created user details"
)
def create_new_user(
    data: UserDetails,
    db: Session = Depends(get_db)
) -> UserDisplay:
    """
    Creates a new user with the provided username, email, and password.
    """
    return db_user.create_user(db, data)


@router.get(
    "/me",
    response_model=UserDisplay,
    status_code=status.HTTP_200_OK,
    name="get_current_user_details",
    summary="Get current authenticated user details",
    response_description="The authenticated user's details"
)
def get_current_user_details(
    user: DBUser = Depends(get_current_user)
) -> UserDisplay:
    """
    Return the details of the currently authenticated user.
    """
    return user


@router.put(
    "/me",
    response_model=UserDisplay,
    name="update_current_user",
    summary="Update current user's details",
    response_description="Updated user details"
)
def update_user_details(
    email: Optional[str] = None,
    password: Optional[str] = None,
    db: Session = Depends(get_db),
    user: DBUser = Depends(get_current_user)
) -> UserDisplay:
    """
    Update the current user's email and/or password.
    """
    return db_user.update_user(user=user, email=email, password=password, db=db)


@router.delete(
    "/me",
    status_code=status.HTTP_200_OK,
    name="delete_current_user",
    summary="Delete current user account",
    response_description="Confirmation of deletion"
)
def delete_user_account(
    user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Permanently delete the current user's account.
    """
    return db_user.delete_user(user=user, db=db)
