import hashlib
import base64
from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.database.models import DBUrl
from config import Config


def generate_short_code(original_url: str) -> str:
    """
    Generate a base64-encoded SHA-256 hash and truncate to the configured length.
    """
    sha256 = hashlib.sha256(original_url.encode()).digest()
    encoded = base64.urlsafe_b64encode(sha256).decode().rstrip("=")
    return encoded[:Config.SHORT_URL_LENGTH]


def create_url(long_url: str, db: Session, user_id: int, description: str = "") -> DBUrl:
    """
    Create a shortened URL entry in the database.
    """
    short_code = generate_short_code(long_url)
    new_url = DBUrl(
        long_url=long_url,
        short_url=short_code,
        description=description,
        user_id=user_id
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url


def get_url(short_url: str, db: Session) -> DBUrl:
    """
    Retrieve the original URL by its shortened code.
    """
    url = db.query(DBUrl).filter(DBUrl.short_url == short_url).first()
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found.")
    return url


def get_user_urls(user_id: int, skip: int, limit: int, db: Session) -> List[DBUrl]:
    """
    Return a paginated list of URLs created by a specific user.
    """
    return db.query(DBUrl).filter(DBUrl.user_id == user_id).offset(skip).limit(limit).all()


def update_url(
    short_url: str,
    new_long_url: str,
    new_description: str,
    user_id: int,
    db: Session
) -> DBUrl:
    """
    Update a URL's long_url and description by short_url and user_id.
    """
    url = db.query(DBUrl).filter(
        DBUrl.short_url == short_url,
        DBUrl.user_id == user_id
    ).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found.")

    url.long_url = new_long_url
    url.description = new_description
    db.commit()
    db.refresh(url)
    return url


def delete_url(short_url: str, user_id: int, db: Session) -> dict:
    """
    Delete a URL if it belongs to the given user.
    """
    url = db.query(DBUrl).filter(
        DBUrl.short_url == short_url,
        DBUrl.user_id == user_id
    ).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found or unauthorized")

    db.delete(url)
    db.commit()
    return {"message": "URL deleted."}
