from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token:str
    token_type:str

class RegenerateToken(BaseModel):
    access_token:str


class TokenData(BaseModel):
    # username: str | None = None
    username: Optional[str] = None

class LoginForm(BaseModel):
    password: str