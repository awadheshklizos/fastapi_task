from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    refresh_token:str
    token_type:str

class RegenerateToken(BaseModel):
    access_token:str


class TokenData(BaseModel):
    username: str | None = None

class LoginForm(BaseModel):
    password: str