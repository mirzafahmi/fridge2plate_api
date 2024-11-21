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
from db.models.recipe import IngredientCategory, Ingredient, RecipeCategory, RecipeOrigin, RecipeTag
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
    dummy_users = [
        User(
            id=test_admin_id, 
            username=normalized_username, 
            email="test@example.com", 
            password=bcrypt_context.hash("test123")
        ),
        User(
            id=uuid.UUID("0c619092-817e-4f73-b25f-8e187e69dded"), 
            username="second_user", 
            email="test1@example.com", 
            password=bcrypt_context.hash("test123")
        )
    ]
    dummy_ingredient_categories = [
        IngredientCategory(
            id=uuid.UUID("b4b165f6-a4f2-45f6-bda6-0a49092d3f03"),
            name="proteins",
            created_by=test_admin_id
        ),
        IngredientCategory(
            id=uuid.UUID("6722eb62-884a-4208-8596-ed82d310e832"),
            name="vegetables",
            created_by=test_admin_id
        ),
    ]

    dummy_ingredients = [
        Ingredient(
            id=uuid.UUID("423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"),
            name="chicken",
            brand="chicken",
            icon="/test1",
            ingredient_category_id=uuid.UUID("b4b165f6-a4f2-45f6-bda6-0a49092d3f03"),
            created_by=test_admin_id
        ),
        Ingredient(
            id=uuid.UUID("b3cceb34-9465-4020-9066-f7b5ce3c372c"),
            name="carrot",
            brand="carrot",
            icon="/test1",
            ingredient_category_id=uuid.UUID("6722eb62-884a-4208-8596-ed82d310e832"),
            created_by=test_admin_id
        ),
    ]

    dummy_recipe_categories = [
        RecipeCategory(
            id=uuid.UUID("4053a7e8-9ae5-415d-9bed-e4d0a235f481"),
            name="breakfast",
            created_by=test_admin_id
        ),
        RecipeCategory(
            id=uuid.UUID("5ce3381f-2298-44bd-b41c-a19d4b69e7a1"),
            name="lunch",
            created_by=test_admin_id
        ),
    ]

    dummy_recipe_origins = [
        RecipeOrigin(
            id=uuid.UUID("92e80174-c259-480a-80b5-f5b0d32ca005"),
            name="malay",
            created_by=test_admin_id
        ),
        RecipeOrigin(
            id=uuid.UUID("c7048030-10ff-486c-9e78-7417212dd728"),
            name="italian",
            created_by=test_admin_id
        ),
    ]

    dummy_recipe_tags = [
        RecipeTag(
            id=uuid.UUID("8c935f60-2f3a-410a-9860-09bb2c270a38"),
            name="eid",
            created_by=test_admin_id
        ),
        RecipeTag(
            id=uuid.UUID("13444244-43b2-4d63-a080-604dd5088452"),
            name="beginner",
            created_by=test_admin_id
        ),
    ]

    session.add_all(dummy_users + dummy_ingredient_categories + dummy_ingredients + dummy_recipe_categories)
    session.commit()
    session.close()

    yield

    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def token(client):
    response = client.post("/auth/login", 
        data={
            "username": "test@example.com", 
            "password": "test123"
        }
    )
    
    assert response.status_code == 200
    return response.json()["access_token"]