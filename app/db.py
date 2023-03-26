from typing import Iterator

from sqlalchemy.orm import Session

from core.db_common import get_engine, get_session

DATABASE_URL = "sqlite:///./databases/data.db"


engine = get_engine(DATABASE_URL)
SessionLocal = get_session(engine)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
