from fastapi.testclient import TestClient
from dotenv import load_dotenv
import os


load_dotenv()
JWT_SECRET = os.getenv("SECRET_KEY")

def test_index(client: TestClient):
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == "Fridge2plate API server is running"

def test_register_user(client: TestClient):
    response = client.post("/auth/register", 
        json={
            "username": "Test User 2",
            "email": "test2@example.com",
            "password": "test123"
        }
    )

    user = response.json()["user"]
    print(user)
    assert response.status_code == 201
    assert response.json()["detail"] == "User created successfully"

    assert "id" in user
    assert user['username'] == "testuser2"
    assert user['email'] == "test2@example.com"

    assert "created_date" in user
    assert "updated_date" in user

def test_register_user_by_various_letter_case(client: TestClient):
    response = client.post("/auth/register", 
        json={
            "username": "tEsT UseR 2",
            "email": "tESt2@example.com",
            "password": "test123"
        }
    )

    user = response.json()["user"]

    assert response.status_code == 201
    assert response.json()["detail"] == "User created successfully"

    assert "id" in user
    assert user['username'] == "testuser2"
    assert user['email'] == "tESt2@example.com"

    assert "created_date" in user
    assert "updated_date" in user

def test_register_existed_email(client: TestClient):
    test_email = "test@example.com"
    
    response = client.post("/auth/register", 
        json={
            "username": "Test User",
            "email": test_email,
            "password": "test123"
        }
    )

    assert response.status_code == 400

    assert response.json() == {"detail": f"{test_email} is already registered"}

def test_register_existed_username(client: TestClient):
    test_username = "Test User"
    
    response = client.post("/auth/register", 
        json={
            "username": test_username,
            "email": "tests@example.com",
            "password": "test123"
        }
    )

    assert response.status_code == 400

    assert response.json() == {"detail": f"{test_username.lower().replace(" ", "")} is already registered"}

def test_register_empty_user_data(client: TestClient):
    response = client.post("/auth/register", 
        json={
            "username": "",
            "email": "",
            "password": ""
        }
    )

    response_json = response.json()

    assert response.status_code == 422

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 3

    assert response_json["detail"][0]["loc"] == ["body", "username"]
    assert response_json["detail"][0]["msg"] == "String should have at least 5 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

    assert response_json["detail"][1]["loc"] == ["body", "email"]
    assert response_json["detail"][1]["msg"] == "value is not a valid email address: An email address must have an @-sign."
    assert response_json["detail"][1]["type"] == "value_error"

    assert response_json["detail"][2]["loc"] == ["body", "password"]
    assert response_json["detail"][2]["msg"] == "String should have at least 5 characters"
    assert response_json["detail"][2]["type"] == "string_too_short"

def test_register_empty_username(client: TestClient):
    response = client.post("/auth/register", 
        json={
            "username": "",
            "email": "test7@example.com",
            "password": "test123"
        }
    )

    response_json = response.json()

    assert response.status_code == 422

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "username"]
    assert response_json["detail"][0]["msg"] == "String should have at least 5 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_register_empty_email(client: TestClient):
    response = client.post("/auth/register", 
        json={
            "username": "Test User 7",
            "email": "",
            "password": "test123"
        }
    )

    response_json = response.json()

    assert response.status_code == 422

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "email"]
    assert response_json["detail"][0]["msg"] == "value is not a valid email address: An email address must have an @-sign."
    assert response_json["detail"][0]["type"] == "value_error"

def test_register_not_email(client: TestClient):
    response = client.post("/auth/register", 
        json={
            "username": "Test User 7",
            "email": "username",
            "password": "test123"
        }
    )

    response_json = response.json()

    assert response.status_code == 422

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "email"]
    assert response_json["detail"][0]["msg"] == "value is not a valid email address: An email address must have an @-sign."
    assert response_json["detail"][0]["type"] == "value_error"

def test_register_empty_password(client: TestClient):
    response = client.post("/auth/register", 
        json={
            "username": "Test User 7",
            "email": "test7@example.com",
            "password": ""
        }
    )

    response_json = response.json()

    assert response.status_code == 422

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "password"]
    assert response_json["detail"][0]["msg"] == "String should have at least 5 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_get_user(client: TestClient, token: str):
    response = client.get("/auth/users", 
        headers={"Authorization": f"Bearer {token}"}
    )

    users = response.json()["users"]

    assert response.status_code == 200
    assert response.json()["detail"] == "Users data retrieved successfully"

    assert users[0]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert users[0]['username'] == "testuser"
    assert users[0]['email'] == "test@example.com"

    assert "created_date" in users[0]
    assert "updated_date" in users[0]

def test_get_user_with_invalid_token(client: TestClient):
    email_to_test = "test@example.com"
    response = client.get(f"/auth/users",
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}

def test_get_user_by_email(client: TestClient, token: str):
    email_to_test = "test@example.com"
    response = client.get(f"/auth/users/{email_to_test}",
        headers={"Authorization": f"Bearer {token}"}
    )

    user = response.json()["user"]
    
    assert response.status_code == 200
    assert response.json()["detail"] == f"{email_to_test} user data retrieved successfully"

    assert user['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert user['username'] == "testuser"
    assert user['email'] == email_to_test

    assert "created_date" in user
    assert "updated_date" in user

def test_get_user_by_email_with_invalid_token(client: TestClient):
    email_to_test = "test@example.com"
    response = client.get(f"/auth/users/{email_to_test}",
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}

def test_get_user_by_wrong_email(client: TestClient, token: str):
    email_to_test = "wrongtest@example.com"
    response = client.get(f"/auth/users/{email_to_test}", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_login_user(client: TestClient):
    response = client.post("/auth/login",
        data={
            "username": "test@example.com",
            "password": "test123"
        }
    )
    assert response.status_code == 200

    assert "access_token" in response.json()

def test_login_not_exist_user(client: TestClient):
    response = client.post("/auth/login", 
        data={
            "username": "wrongtest@example.com",
            "password": "test123"
        }
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_login_wrong_password(client: TestClient):
    response = client.post("/auth/login",
        data={
            "username": "test@example.com",
            "password": "test1234"
        }
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_validate_with_valid_token(client: TestClient):
    login_response = client.post("/auth/login", 
        data={
            "username": "test@example.com",
            "password": "test123"
        }
    )

    assert login_response.status_code == 200

    assert "access_token" in login_response.json()

    token = login_response.json()["access_token"]

    profile_response = client.get(
        "/auth/validate", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert profile_response.status_code == 200
    assert profile_response.json()["detail"] == "User data retrieved successfully"

    profile_data = profile_response.json()["user"]

    assert profile_data["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert profile_data["email"] == "test@example.com"
    assert profile_data["username"] == "testuser"

    assert "created_date" in profile_data
    assert "updated_date" in profile_data
    
def test_validate_with_invalid_token(client: TestClient):
    response = client.get(
        "/auth/validate", 
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}
