from fastapi.testclient import TestClient
from datetime import datetime


url_prefix = '/recipes'
recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"

def test_post_assoc_by_cooked_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "cooked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    assoc = response.json()["recipe_user_association"]

    assert assoc["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert assoc["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    recipe = assoc["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["cooked_count"] == 1
    assert recipe["bookmarked_count"] == 0
    assert recipe["liked_count"] == 0

    assert assoc["cooked"] == True
    assert assoc["bookmarked"] == False
    assert assoc["bookmarked_date"] == None
    assert assoc["liked"] == False
    assert assoc["liked_date"] == None

    cooked_date_str = assoc["cooked_date"]
    cooked_date = datetime.fromisoformat(cooked_date_str)

    assert cooked_date_str is not None 
    assert isinstance(cooked_date, datetime)

def test_post_assoc_by_cooked_action_with_toggle_original_state(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "cooked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    assoc = response.json()["recipe_user_association"]

    assert assoc["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert assoc["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    recipe = assoc["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["cooked_count"] == 1
    assert recipe["bookmarked_count"] == 0
    assert recipe["liked_count"] == 0

    assert assoc["cooked"] == True
    assert assoc["bookmarked"] == False
    assert assoc["bookmarked_date"] == None
    assert assoc["liked"] == False
    assert assoc["liked_date"] == None

    cooked_date_str = assoc["cooked_date"]
    cooked_date = datetime.fromisoformat(cooked_date_str)

    assert cooked_date_str is not None 
    assert isinstance(cooked_date, datetime)

    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "cooked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    assoc = response.json()["recipe_user_association"]

    assert assoc["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert assoc["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    recipe = assoc["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["cooked_count"] == 0
    assert recipe["bookmarked_count"] == 0
    assert recipe["liked_count"] == 0

    assert assoc["cooked"] == False
    assert assoc["cooked_date"] == None
    assert assoc["bookmarked"] == False
    assert assoc["bookmarked_date"] == None
    assert assoc["liked"] == False
    assert assoc["liked_date"] == None

def test_post_assoc_by_uncooked_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d376337/toggle",
        json={
            "action": "cooked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    assoc = response.json()["recipe_user_association"]

    assert assoc["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert assoc["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

    recipe = assoc["recipe"]

    assert recipe["id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe["cooked_count"] == 0
    assert recipe["bookmarked_count"] == 1
    assert recipe["liked_count"] == 1

    assert assoc["cooked"] == False
    assert assoc["cooked_date"] == None
    assert assoc["bookmarked"] == True
    assert assoc["liked"] == True

    bookmarked_date_str = assoc["bookmarked_date"]
    bookmarked_date = datetime.fromisoformat(bookmarked_date_str)

    assert bookmarked_date_str is not None 
    assert isinstance(bookmarked_date, datetime)

    liked_date_str = assoc["liked_date"]
    liked_date = datetime.fromisoformat(liked_date_str)

    assert liked_date_str is not None 
    assert isinstance(liked_date, datetime)

def test_post_assoc_by_bookmarked_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "bookmarked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    assoc = response.json()["recipe_user_association"]

    assert assoc["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert assoc["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    recipe = assoc["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["cooked_count"] == 0
    assert recipe["bookmarked_count"] == 1
    assert recipe["liked_count"] == 0

    assert assoc["cooked"] == False
    assert assoc["cooked_date"] == None
    assert assoc["bookmarked"] == True
    assert assoc["liked"] == False
    assert assoc["liked_date"] == None

    bookmarked_date_str = assoc["bookmarked_date"]
    bookmarked_date = datetime.fromisoformat(bookmarked_date_str)

    assert bookmarked_date_str is not None 
    assert isinstance(bookmarked_date, datetime)

def test_post_assoc_by_bookmarked_action_with_toggle_to_original_state(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "bookmarked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    assoc = response.json()["recipe_user_association"]

    assert assoc["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert assoc["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    recipe = assoc["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["cooked_count"] == 0
    assert recipe["bookmarked_count"] == 1
    assert recipe["liked_count"] == 0

    assert assoc["cooked"] == False
    assert assoc["cooked_date"] == None
    assert assoc["bookmarked"] == True
    assert assoc["liked"] == False
    assert assoc["liked_date"] == None

    bookmarked_date_str = assoc["bookmarked_date"]
    bookmarked_date = datetime.fromisoformat(bookmarked_date_str)

    assert bookmarked_date_str is not None 
    assert isinstance(bookmarked_date, datetime)

    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "bookmarked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    assoc = response.json()["recipe_user_association"]

    assert assoc["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert assoc["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    recipe = assoc["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["cooked_count"] == 0
    assert recipe["bookmarked_count"] == 0
    assert recipe["liked_count"] == 0

    assert assoc["cooked"] == False
    assert assoc["cooked_date"] == None
    assert assoc["bookmarked"] == False
    assert assoc["bookmarked_date"] == None
    assert assoc["liked"] == False
    assert assoc["liked_date"] == None

def test_post_assoc_by_unbookmarked_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d376337/toggle",
        json={
            "action": "bookmarked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    assoc = response.json()["recipe_user_association"]

    assert assoc["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert assoc["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

    recipe = assoc["recipe"]

    assert recipe["id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe["cooked_count"] == 1
    assert recipe["bookmarked_count"] == 0
    assert recipe["liked_count"] == 1

    assert assoc["cooked"] == True
    assert assoc["bookmarked"] == False
    assert assoc["bookmarked_date"] == None
    assert assoc["liked"] == True

    cooked_date_str = assoc["cooked_date"]
    cooked_date = datetime.fromisoformat(cooked_date_str)

    assert cooked_date_str is not None 
    assert isinstance(cooked_date, datetime)

    liked_date_str = assoc["liked_date"]
    liked_date = datetime.fromisoformat(liked_date_str)

    assert liked_date_str is not None 
    assert isinstance(liked_date, datetime)

def test_post_assoc_by_liked_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "liked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    assoc = response.json()["recipe_user_association"]

    assert assoc["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert assoc["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    recipe = assoc["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["cooked_count"] == 0
    assert recipe["bookmarked_count"] == 0
    assert recipe["liked_count"] == 1

    assert assoc["cooked"] == False
    assert assoc["cooked_date"] == None
    assert assoc["bookmarked"] == False
    assert assoc["bookmarked_date"] == None
    assert assoc["liked"] == True

    liked_date_str = assoc["liked_date"]
    liked_date = datetime.fromisoformat(liked_date_str)

    assert liked_date_str is not None 
    assert isinstance(liked_date, datetime)

def test_post_assoc_by_liked_action_with_toggle_to_original_state(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "liked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    assoc = response.json()["recipe_user_association"]

    assert assoc["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert assoc["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    recipe = assoc["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["cooked_count"] == 0
    assert recipe["bookmarked_count"] == 0
    assert recipe["liked_count"] == 1

    assert assoc["cooked"] == False
    assert assoc["cooked_date"] == None
    assert assoc["bookmarked"] == False
    assert assoc["bookmarked_date"] == None
    assert assoc["liked"] == True

    liked_date_str = assoc["liked_date"]
    liked_date = datetime.fromisoformat(liked_date_str)

    assert liked_date_str is not None 
    assert isinstance(liked_date, datetime)

    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "liked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    assoc = response.json()["recipe_user_association"]

    assert assoc["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert assoc["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    recipe = assoc["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["cooked_count"] == 0
    assert recipe["bookmarked_count"] == 0
    assert recipe["liked_count"] == 0

    assert assoc["cooked"] == False
    assert assoc["cooked_date"] == None
    assert assoc["bookmarked"] == False
    assert assoc["bookmarked_date"] == None
    assert assoc["liked"] == False
    assert assoc["liked_date"] == None

def test_post_assoc_by_unliked_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d376337/toggle",
        json={
            "action": "liked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    assoc = response.json()["recipe_user_association"]

    assert assoc["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert assoc["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

    recipe = assoc["recipe"]

    assert recipe["id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe["cooked_count"] == 1
    assert recipe["bookmarked_count"] == 1
    assert recipe["liked_count"] == 0

    assert assoc["cooked"] == True
    assert assoc["bookmarked"] == True
    assert assoc["liked"] == False
    assert assoc["liked_date"] == None

    cooked_date_str = assoc["cooked_date"]
    cooked_date = datetime.fromisoformat(cooked_date_str)

    assert cooked_date_str is not None 
    assert isinstance(cooked_date, datetime)

    bookmarked_date_str = assoc["bookmarked_date"]
    bookmarked_date = datetime.fromisoformat(bookmarked_date_str)

    assert bookmarked_date_str is not None 
    assert isinstance(bookmarked_date, datetime)

def test_post_assoc_with_wrong_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "cook"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "action"]
    assert response_json["detail"][0]["msg"] == "Input should be 'liked', 'bookmarked' or 'cooked'"

def test_post_assoc_with_invalid_token(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "cook"
        }, 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_post_assoc_without_token(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "cook"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_post_assoc_with_wrong_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d376338/toggle",
        json={
            "action": "liked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 6b86885b-a613-4ca6-a9b7-584c3d376338 as Recipe is not found"