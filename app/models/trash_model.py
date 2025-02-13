from beanie import Document
from datetime import datetime
from pydantic import Field
from typing import Optional
from beanie import PydanticObjectId

class Trash(Document):
    original_data: dict  # Required field
    deletion_timestamp: datetime = Field(default_factory=datetime.utcnow)  # Default value
    deleted_by: PydanticObjectId  # Required field
    reason: Optional[str] = None  # Optional field
    delete_status: Optional[bool] = False
    class Settings:
        name = "trash"

# class Trash(Document):
#     original_data: dict
#     deletion_timestamp: datetime = Field(default_factory=datetime.utcnow)
#     deleted_by: str
#     reason: Optional[str] = None

#     class Settings:
#         name = "trash"