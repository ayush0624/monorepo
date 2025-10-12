from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from projects.concord.app.common.config import settings

SQLALCHEMY_DB_URL = settings.DB_URL

engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
