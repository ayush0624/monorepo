import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

db_path = os.path.expanduser("~/Downloads/students.db")

engine = sa.create_engine(
    f"sqlite:///{db_path}", connect_args={"check_same_thread": False}
)

sess = sessionmaker(
    autocommit=False,  # prevents partial writes
    autoflush=False,  # reccomended for fastapi
    bind=engine,
)

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    age: Mapped[int] = mapped_column(nullable=False)
    year: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<Student(id={self.id}, name={self.name}, age={self.age}, year={self.year})"


Base.metadata.create_all(engine)


def get_db():
    db = sess()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
