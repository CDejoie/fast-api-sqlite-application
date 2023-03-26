from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker


def get_engine(database_url: str) -> Engine:
    return create_engine(
        database_url, connect_args={"check_same_thread": False}, echo=True
    )


def get_session(engine: Engine) -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
