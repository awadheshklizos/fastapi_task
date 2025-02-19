from beanie import Document
from pydantic import Field, EmailStr
from datetime import datetime
from typing import Optional


class User(Document):
    username: str = Field(..., unique=True)
    email: EmailStr = Field(..., unique=True)
    hashed_password: str
    refresh_tokens: str = Field(default_factory=str) 
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    role:str
    profile_picture: Optional[str] = None
    
    class Settings:
        name = "users"

    def update_timestamp(self):
        self.updated_at = datetime.now()

