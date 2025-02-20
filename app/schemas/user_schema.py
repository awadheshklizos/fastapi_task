from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId
from typing import List, Optional


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
    id: PydanticObjectId
    created_at: datetime
    # updated_at: datetime
    role: str

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    users: List[UserOut]


class BatchDeleteRequest(BaseModel):
    user_ids: List[str]
    reason: Optional[str] = None


class TrashRecordResponse(BaseModel):
    id: str
    original_data: dict
    deletion_timestamp: datetime = Field(default_factory=datetime.utcnow)
    deleted_by: str
    reason: Optional[str] = None
    delete_status: Optional[bool]

    class Config:
        from_attributes = True


class TrashList(BaseModel):
    trash: List[TrashRecordResponse]


class RestoreUser(BaseModel):
    user_id: str
