from beanie import Document
from pydantic import Field, EmailStr
from datetime import datetime

class User(Document):
    username: str = Field(..., unique=True)
    email: EmailStr = Field(..., unique=True)
    hashed_password: str

    refresh_tokens: list[str] = Field(default_factory=list)  # Store valid refresh tokens

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()