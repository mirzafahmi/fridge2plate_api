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
from db.db_setup import get_db  
from db.models.user import User
from db.models.recipe import IngredientCategory
from db.db_setup import Base

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
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    test_admin_id = uuid.UUID("db67b3f4-0e04-47bb-bc46-94826847ee4f")
    normalized_username = "Test user".lower().replace(" ", "")
    dummy_user = User(
        id=test_admin_id, 
        username=normalized_username, 
        email="test@example.com", 
        password=bcrypt_context.hash("test123")
    )

    dummy_ingredient_categories = [
        IngredientCategory(
            id=uuid.UUID("b4b165f6-a4f2-45f6-bda6-0a49092d3f03"),
            name="protein",
            created_by=test_admin_id
        ),
        IngredientCategory(
            id=uuid.UUID("6722eb62-884a-4208-8596-ed82d310e832"),
            name="vegetables",
            created_by=test_admin_id
        ),
    ]

    session.add(dummy_user)
    session.add_all(dummy_ingredient_categories)
    session.commit()
    session.close()

    yield

    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)
