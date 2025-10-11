from pydantic import BaseModel
from typing import Optional
import enum
import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Enum, text, DateTime



class Priority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# --------------------
# Pydantic Models
# --------------------


class ProjectBase(BaseModel):
    name: str
    description: Optional[str]
    priority: Priority = Priority.MEDIUM


# --------------------
# ORM Models
# --------------------


class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        default = "no description provided",
        server_default=text("'no description provided'"),
        nullable=False
    )
    priority: Mapped[Priority] = mapped_column(
        Enum(Priority, name="project_priority"), 
        nullable=False, 
        server_default=text("'MEDIUM'"),
        default=Priority.MEDIUM
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("'now'"),
    )
