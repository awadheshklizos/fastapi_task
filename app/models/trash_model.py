from beanie import Document
from datetime import datetime
from pydantic import Field,BaseModel
from typing import List,Optional
from beanie import PydanticObjectId

class Trash(Document):
    original_data: dict  # Required field
    deletion_timestamp: datetime = Field(default_factory=datetime.utcnow)  # Default value
    deleted_by: PydanticObjectId  # Required field
    reason: Optional[str] = None  # Optional field
    delete_status: Optional[bool] = False
    class Settings:
        name = "trash"

