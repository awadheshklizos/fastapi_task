from beanie import Document
from datetime import datetime
from pydantic import Field
from typing import Optional

class Trash(Document):
    original_data: dict
    deletion_timestamp: datetime = Field(default_factory=datetime.utcnow)
    deleted_by: str
    reason: Optional[str] = None

    class Settings:
        name = "trash"