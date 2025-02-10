from datetime import datetime
from pydantic import BaseModel, EmailStr
from beanie import PydanticObjectId
from typing import List


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None, min_length=6)

class UserOut(UserBase):
    id:PydanticObjectId
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserListResponse(BaseModel):
    users: List[UserOut]

