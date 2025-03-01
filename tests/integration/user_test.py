from fastapi.testclient import TestClient


url_prefix = '/users'

def test_get_users(client: TestClient, token: str):
    response = client.get(f"{url_prefix}", 
        headers={"Authorization": f"Bearer {token}"}
    )

    users = response.json()["users"]
    print(users)
    assert response.status_code == 200
    assert response.json()["detail"] == "Users data retrieved successfully"

    assert users[0]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert users[0]['username'] == "testuser"
    assert users[0]['email'] == "test@example.com"

    assert users[0]["cooked_count"] == 1
    assert users[0]["bookmarked_count"] == 1
    assert users[0]["liked_count"] == 1

    assert users[0]["is_following"] == False

    assert users[0]["followers_count"] == 1
    assert users[0]["followings_count"] == 1

    assert "created_date" in users[0]
    assert "updated_date" in users[0]


    assert users[1]['id'] == "0c619092-817e-4f73-b25f-8e187e69dded"
    assert users[1]['username'] == "second_user"
    assert users[1]['email'] == "test1@example.com"

    assert users[1]["cooked_count"] == 0
    assert users[1]["bookmarked_count"] == 0
    assert users[1]["liked_count"] == 0

    assert users[1]["is_following"] == False

    assert users[1]["followers_count"] == 0
    assert users[1]["followings_count"] == 0

    assert "created_date" in users[1]
    assert "updated_date" in users[1]


    assert users[2]['id'] == "799bb766-8ebe-4f51-a153-6e3c5530c3c2"
    assert users[2]['username'] == "third_user"
    assert users[2]['email'] == "test2@example.com"

    assert users[2]["cooked_count"] == 0
    assert users[2]["bookmarked_count"] == 0
    assert users[2]["liked_count"] == 0

    assert users[2]["is_following"] == True

    assert users[2]["followers_count"] == 1
    assert users[2]["followings_count"] == 1

    assert "created_date" in users[2]
    assert "updated_date" in users[2]

def test_get_user_with_invalid_token(client: TestClient):
    email_to_test = "test@example.com"
    response = client.get(f"{url_prefix}/users",
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}

def test_get_user_by_email(client: TestClient, token: str):
    email_to_test = "test@example.com"
    response = client.get(f"{url_prefix}/by_email/{email_to_test}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    user = response.json()["user"]
    
    assert response.status_code == 200
    assert response.json()["detail"] == f"{email_to_test} user data retrieved successfully"

    assert user['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert user['username'] == "testuser"
    assert user['email'] == email_to_test

    assert user["cooked_count"] == 1
    assert user["bookmarked_count"] == 1
    assert user["liked_count"] == 1

    #assert user["is_following"] == False

    #assert user["followers_count"] == 1
    #assert user["followings_count"] == 1

    assert "created_date" in user
    assert "updated_date" in user

def test_get_user_by_email_with_invalid_token(client: TestClient):
    email_to_test = "test@example.com"
    response = client.get(f"{url_prefix}/by_email/{email_to_test}",
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}

def test_get_user_by_wrong_email(client: TestClient, token: str):
    email_to_test = "wrongtest@example.com"
    response = client.get(f"{url_prefix}/by_email/{email_to_test}", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_get_user_data_by_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/0c619092-817e-4f73-b25f-8e187e69dded", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    user = response.json()["user"]
    
    assert response.status_code == 200
    assert response.json()["detail"] == f"ID 0c619092-817e-4f73-b25f-8e187e69dded of user data retrieved successfully"

    assert user['id'] == "0c619092-817e-4f73-b25f-8e187e69dded"
    assert user['username'] == "second_user"
    assert user['email'] == "test1@example.com"

    assert user["cooked_count"] == 0
    assert user["bookmarked_count"] == 0
    assert user["liked_count"] == 0

    assert user["is_following"] == False

    assert user["followers_count"] == 0
    assert user["followings_count"] == 0

    assert "created_date" in user
    assert "updated_date" in user