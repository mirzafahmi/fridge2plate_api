import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from sqlalchemy import inspect 
import uuid
from passlib.context import CryptContext

from main import app  
from app.db.db_setup import get_db  
from app.db.models.user import User
from app.db.db_setup import Base

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Create and commit a dummy user for testing
    session = TestingSessionLocal()
    fixed_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")
    normalized_username = "Test User".lower().replace(" ", "")
    dummy_user = User(id=str(fixed_uuid), username=normalized_username, email="test@example.com", password=bcrypt_context.hash("test123"))
    session.add(dummy_user)
    session.commit()
    session.close()

    yield  # This is where the test will run

    # Teardown: Drop the database tables after the test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)
