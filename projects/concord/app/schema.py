import enum
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class Priority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProjectBase(BaseModel):
    name: str
    description: Optional[str]
    priority: Priority = Priority.MEDIUM


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    model_config = ConfigDict(
        from_attributes=True,  # replaces orm_mode=True
        extra="ignore",
    )


class ProjectCreateResponse(ProjectResponse):
    id: int
    created_at: datetime
