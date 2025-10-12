import enum
from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


class Priority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ------------------------------
# Project Models
# ------------------------------


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


# ------------------------------
# User Models
# ------------------------------


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    model_config = ConfigDict(
        from_attributes=True,  # replaces orm_mode=True
        extra="ignore",
    )


class UserCreateResponse(UserResponse):
    id: int
    created_at: datetime
