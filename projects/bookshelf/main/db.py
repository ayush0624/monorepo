import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, Session, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator

db_path = os.path.expanduser("~/Downloads/bookshelf.db")
engine = sa.create_engine(
    url = f"sqlite:///{db_path}",
    # allows connection to be used across multiple threads
    connect_args={"check_same_thread": False}
)

sess = sessionmaker(
    autoflush = False,
    autocommit = False,
    bind = engine
)

def get_db() -> Generator[Session]:
    db = sess()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

# Define Sqlit DB Models
Base = declarative_base()
class Bookshelf(Base):
    __tablename__ = "bookshelf"

    # id -> a unique identifier representing a single book
    id:Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    # name -> a name corresponding to each book
    name:Mapped[str]
    # author -> the author of the book
    author: Mapped[str]

# Create all of the DB schemas
def init_db():
    """Create tables if they don't exist."""
    Base.metadata.create_all(bind=engine)















