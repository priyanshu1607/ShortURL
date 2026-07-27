from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    
class URL(BaseModel):
    _id:int
    shortURL: str
    Longurl: HttpUrl
    alies : Optional[str] = None
    click : int = 0
    expires_at: datetime = None