from pydantic import BaseModel
from typing import Optional
import enum

class Priority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Project(BaseModel):
    name: str
    description: Optional[str]
    priority: Priority = Priority.MEDIUM

