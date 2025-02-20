from datetime import datetime

from beanie import Document
from pydantic import Field, BaseModel
from typing import Optional
from beanie import PydanticObjectId


class Trash(Document):
    original_data: dict
    deletion_timestamp: datetime = Field(default_factory=datetime.utcnow)
    deleted_by: PydanticObjectId
    reason: Optional[str] = None
    delete_status: Optional[bool] = False

    class Settings:
        name = "trash"
