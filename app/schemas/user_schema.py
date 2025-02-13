from datetime import datetime
from pydantic import BaseModel, EmailStr,Field
from beanie import PydanticObjectId
from typing import List,Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None, min_length=6)

    
class BatchDeleteRequest(BaseModel):
    user_ids: List[str]
    reason: Optional[str] = None

class UserOut(UserBase):
    id:PydanticObjectId
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    users: List[UserOut]


    