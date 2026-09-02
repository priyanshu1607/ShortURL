from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class URL(BaseModel):
    _id:int
    shortURL: str 
    Longurl: HttpUrl
    alies : Optional[str] = None
    click : int = 0
    expires_at: Optional[datetime] = None