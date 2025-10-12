from projects.concord.app.common.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, DateTime, UniqueConstraint


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("first_name", "last_name"),)

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("'now'"),
    )
