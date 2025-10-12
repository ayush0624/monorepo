from typing import Optional
from pydantic import BaseModel, ConfigDict
from projects.concord.app.common.types import Priority
from projects.concord.app.users.schema import UserResponse
from datetime import datetime


class Base(BaseModel):
    name: str
    description: Optional[str]
    priority: Priority = Priority.MEDIUM


class ProjectCreate(Base):
    pass


class ProjectResponse(Base):
    owner: UserResponse

    model_config = ConfigDict(
        from_attributes=True,  # replaces orm_mode=True
        extra="ignore",
    )


class ProjectCreateResponse(ProjectResponse):
    id: int
    created_at: datetime
