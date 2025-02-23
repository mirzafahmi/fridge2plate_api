import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from sqlalchemy import inspect , func
import uuid
from passlib.context import CryptContext
from datetime import datetime

from main import app
from db.db_setup import get_db  
from db.models.user import User, Badge, Follower
from db.models.recipe import IngredientCategory, Ingredient, UOM, RecipeCategory, RecipeOrigin, RecipeTag, RecipeUserAssociation
from db.models.timestamp_mixin import TimestampMixin
from db.db_setup import Base
from utils.recipe import post_recipe
from tests.integration.recipe_data import recipes
from pydantic_schemas.recipe import RecipeCreateSeeder

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
        ),
        User(
            id=uuid.UUID("799bb766-8ebe-4f51-a153-6e3c5530c3c2"), 
            username="third_user", 
            email="test2@example.com", 
            password=bcrypt_context.hash("test123")
        )
    ]

    dummy_badges = [
        Badge(
            id=uuid.UUID("3afb1e3d-617e-41f8-b140-b6a5fd876446"),
            name="getting started",
            description="created at least 1 recipe",
            image="/static/badges/getting_started.png",
            created_by=test_admin_id
        ),
        Badge(
            id=uuid.UUID("52518fea-cae4-4a79-abf4-65cb8a122f16"),
            name="veteran",
            description="created at least 5 recipe",
            image="/static/badges/veteran.png",
            created_by=test_admin_id
        )
        ,
        Badge(
            id=uuid.UUID("6446f1e0-fd4a-455e-a9d0-e77c8c059140"),
            name="community leader",
            description="reached at least 5 follower",
            image="/static/badges/community_leader.png",
            created_by=test_admin_id
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
            ingredient_category_id=uuid.UUID("b4b165f6-a4f2-45f6-bda6-0a49092d3f03"),
            created_by=test_admin_id
        ),
        Ingredient(
            id=uuid.UUID("b3cceb34-9465-4020-9066-f7b5ce3c372c"),
            name="carrot",
            brand="carrot",
            ingredient_category_id=uuid.UUID("6722eb62-884a-4208-8596-ed82d310e832"),
            created_by=test_admin_id
        ),
        Ingredient(
            id=uuid.UUID("c282fc9e-dfbd-46ff-8ee0-87463c63a51e"),
            name="fish",
            brand="fish",
            ingredient_category_id=uuid.UUID("b4b165f6-a4f2-45f6-bda6-0a49092d3f03"),
            created_by=test_admin_id
        ),
    ]

    dummy_uoms = [
        UOM(
            id=uuid.UUID("8c935f60-2f3a-410a-9860-09bb2c270a38"),
            name="clove",
            unit="clove",
            weightage=1,
            created_by=test_admin_id
        ),
        UOM(
            id=uuid.UUID("13444244-43b2-4d63-a080-604dd5088452"),
            name="piece",
            unit="piece",
            weightage="1",
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
        RecipeTag(
            id=uuid.UUID("3d460ec6-f369-4681-851d-78999ec3d2a8"),
            name="quick & easy",
            created_by=test_admin_id
        )
    ]
    
    dummy_user_recipe_assoc = [
        RecipeUserAssociation(
            user_id=test_admin_id,
            recipe_id=uuid.UUID("6b86885b-a613-4ca6-a9b7-584c3d376337"),
            cooked=True,
            cooked_date=func.now(),
            bookmarked=True,
            bookmarked_date=func.now(),
            liked=True,
            liked_date=func.now(),
        )
    ]

    fixed_timestamp = datetime(2024, 2, 12, 12, 0, 0)


    dummy_follow = [
        Follower(user_id= uuid.UUID("799bb766-8ebe-4f51-a153-6e3c5530c3c2"), follower_id=test_admin_id, created_date=fixed_timestamp),
        Follower(user_id= test_admin_id, follower_id=uuid.UUID("799bb766-8ebe-4f51-a153-6e3c5530c3c2"), created_date=fixed_timestamp)
    ]

    TimestampMixin.override_timestamps(dummy_follow, created=fixed_timestamp, updated=fixed_timestamp)

    for recipe in recipes:
        recipe_data = RecipeCreateSeeder(**recipe)
        
        post_recipe(session, recipe_data)

    session.add_all(dummy_users + dummy_badges + dummy_ingredient_categories + dummy_ingredients + dummy_recipe_categories + dummy_recipe_origins + dummy_recipe_tags + dummy_uoms + dummy_user_recipe_assoc + dummy_follow)
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