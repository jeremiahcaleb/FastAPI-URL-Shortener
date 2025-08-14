from pydantic import BaseModel, Field, EmailStr
from typing import Optional


# ------------------- User Schemas -------------------

class UserDetailsUpdatable(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserDetails(UserDetailsUpdatable):
    user_name: str

class UserDisplay(BaseModel):
    id: int
    user_name: str
    email: Optional[EmailStr] = None

    class Config:
        from_attributes = True


# ------------------- URL Schemas -------------------

class UrlData(BaseModel):
    long_url: str  # You can add extra validation with Pydantic's HttpUrl
    description: Optional[str] = Field(default=None, max_length=200)

class UrlDisplay(BaseModel):
    id: int
    short_url: str
    long_url: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class UrlDataUpdate(BaseModel):
    short_url: str
    long_url: Optional[str] = None
    description: Optional[str] = Field(default=None, max_length=200)
