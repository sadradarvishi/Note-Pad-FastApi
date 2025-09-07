import pytest
from app import database
from app.database import Base
from app.dependency.auth import get_current_user
from app.main import app
from app.models.user_model import UserModel
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def test_engine():
    with PostgresContainer("postgres:16") as pg:
        engine = create_engine(pg.get_connection_url())
        Base.metadata.create_all(bind=engine)
        yield engine
        engine.dispose()


@pytest.fixture(scope="function")
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=connection, expire_on_commit=False
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[database.get_db] = _get_test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    user = UserModel(firstname="ali", lastname="tester", username="ali_tester", password="password")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def authed_client(db_session, test_user):
    def _get_db():
        try:
            yield db_session
        finally:
            pass

    def _current_user():
        return test_user

    app.dependency_overrides[database.get_db] = _get_db
    app.dependency_overrides[get_current_user] = _current_user
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
