from typing import Iterator
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from app.main import app
from app.db import get_db
from core.models import Base

DATABASE_URL = "sqlite:///./databases/test.db"


@pytest.fixture(scope="session")
def db_engine() -> Iterator[Engine]:
    engine = create_engine(DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine) -> Iterator[Session]:
    connection = db_engine.connect()

    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)

    yield db

    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db) -> Iterator[TestClient]:
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as test:
        yield test
