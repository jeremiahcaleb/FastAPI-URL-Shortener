from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas import UserDetails
from app.database.models import DBUser
from app.database.hash import Hash


def check_email_address(db: Session, email: str) -> bool:
    """
    Check if a user with the given email exists.
    """
    return db.query(DBUser).filter(DBUser.email == email).first() is not None


def check_username_exist(db: Session, username: str) -> bool:
    """
    Check if a user with the given username exists.
    """
    return db.query(DBUser).filter(DBUser.user_name == username).first() is not None


def create_user(db: Session, data: UserDetails) -> DBUser:
    """
    Create a new user if email and username are unique.
    """
    if check_email_address(db, data.email) or check_username_exist(db, data.user_name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already registered."
        )

    # 🔐 Hash password before storing
    hashed_password = Hash.encrypt(data.password)

    new_user = DBUser(
        user_name=data.user_name,  # ✅ fixed here
        email=data.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(user: DBUser, email: str, password: str, db: Session) -> DBUser:
    """
    Update user's email and/or password.
    """
    db_user = db.query(DBUser).filter(DBUser.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    if email:
        db_user.email = email
    if password:
        db_user.password = Hash.encrypt(password)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(user: DBUser, db: Session) -> dict:
    """
    Delete a user from the database.
    """
    db_user = db.query(DBUser).filter(DBUser.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted."}


def get_user(user_name: str, db: Session) -> DBUser:
    """
    Retrieve a user by username.
    """
    user = db.query(DBUser).filter(DBUser.user_name == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
