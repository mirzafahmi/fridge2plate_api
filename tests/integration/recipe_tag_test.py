from fastapi.testclient import TestClient


url_prefix = '/recipe_tags'
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

def test_get_recipe_tag_list(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Recipe Tag list is retrieved successfully"

    recipe_tags = response.json()["recipe_tags"]

    assert isinstance(recipe_tags, list)
    assert len(recipe_tags) == 3

    assert recipe_tags[0]['id'] == "13444244-43b2-4d63-a080-604dd5088452"
    assert recipe_tags[0]['name'] == "beginner"
    assert recipe_tags[0]["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_tags[0]
    assert "created_date" in recipe_tags[0]

    assert recipe_tags[1]['id'] == "8c935f60-2f3a-410a-9860-09bb2c270a38"
    assert recipe_tags[1]['name'] == "eid"
    assert recipe_tags[1]["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_tags[1]
    assert "created_date" in recipe_tags[1]

def test_get_recipe_tag_list_with_invalid_token(client: TestClient):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_recipe_tag_list_without_token(client: TestClient):
    response = client.get(f"{url_prefix}/")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_recipe_tag_by_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"Id 13444244-43b2-4d63-a080-604dd5088452 as Recipe Tag is retrieved successfully"

    recipe_tag = response.json()["recipe_tag"]
    
    assert recipe_tag['id'] == "13444244-43b2-4d63-a080-604dd5088452"
    assert recipe_tag['name'] == "beginner"
    assert recipe_tag["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_tag
    assert "created_date" in recipe_tag

def test_get_recipe_tag_by_id_with_invalid_token(client: TestClient):
    response = client.get(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_recipe_tag_by_id_without_token(client: TestClient):
    response = client.get(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_recipe_tag_by_wrong_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f01", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Id b4b165f6-a4f2-45f6-bda6-0a49092d3f01 as Recipe Tag is not found"

def test_post_recipe_tag(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test recipe tag",
            "created_by": ADMIN_ID
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["detail"] == f"test recipe tag as Recipe Tag is created successfully"

    recipe_tag = response.json()["recipe_tag"]

    assert recipe_tag["name"] == "test recipe tag"
    assert recipe_tag["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_tag
    assert "created_date" in recipe_tag

def test_post_recipe_tag_with_invalid_token(client: TestClient):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test recipe tag",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_post_recipe_tag_without_token(client: TestClient):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test recipe tag",
            "created_by": ADMIN_ID
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_post_recipe_tag_with_various_letter_case(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "tESt rECIpe TAG",
            "created_by": ADMIN_ID
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["detail"] == f"test recipe tag as Recipe Tag is created successfully"

    recipe_tag = response.json()["recipe_tag"]

    assert recipe_tag["name"] == "test recipe tag"
    assert recipe_tag["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_tag
    assert "created_date" in recipe_tag

def test_post_recipe_tag_with_duplicate_name(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "eid",
            "created_by": ADMIN_ID
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == f"eid as Recipe Tag is already registered"

def test_post_recipe_tag_with_empty_name(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "",
            "created_by": ADMIN_ID
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_recipe_tag_without_name(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "created_by": ADMIN_ID
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_tag_with_not_available_creator_id(client: TestClient, token: str): 
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test recipe tag",
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 3fa85f64-5717-4562-b3fc-2c963f66afa6 as User is not found"

def test_post_recipe_tag_with_invalid_creator_id(client: TestClient, token: str): 
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test recipe tag",
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afaz"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_tag_with_empty_creator_id(client: TestClient, token: str): 
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test recipe tag",
            "created_by": ""
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_recipe_tag_by_changing_name(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        json={
            "name": "updated ingredient tag",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 202
    assert response.json()["detail"] == "Id 13444244-43b2-4d63-a080-604dd5088452 as Recipe Tag is updated successfully"

    recipe_tag = response.json()["recipe_tag"]

    assert recipe_tag['id'] == "13444244-43b2-4d63-a080-604dd5088452"
    assert recipe_tag['name'] == "updated ingredient tag"
    assert recipe_tag["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_tag
    assert "created_date" in recipe_tag

def test_put_recipe_tag_by_changing_name_with_invalid_token(client: TestClient):
    response = client.put(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        json={
            "name": "updated ingredient tag",
        }, 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_put_recipe_tag_by_changing_name_without_token(client: TestClient):
    response = client.put(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        json={
            "name": "updated ingredient tag",
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_put_recipe_tag_by_changing_name_with_various_letter_case(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        json={
            "name": "upDATed inGREdient TAG",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 202
    assert response.json()["detail"] == "Id 13444244-43b2-4d63-a080-604dd5088452 as Recipe Tag is updated successfully"

    recipe_tag = response.json()["recipe_tag"]

    assert recipe_tag['id'] == "13444244-43b2-4d63-a080-604dd5088452"
    assert recipe_tag['name'] == "updated ingredient tag"
    assert recipe_tag["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_tag
    assert "created_date" in recipe_tag

def test_put_recipe_tag_by_changing_name_with_duplicate_name(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        json={
            "name": "eid",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == f"eid as Recipe Tag is already registered"

def test_put_recipe_tag_by_changing_name_with_empty_name(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        json={
            "name": "",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422
    
    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_put_recipe_tag_with_not_available_creator_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        json={
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 3fa85f64-5717-4562-b3fc-2c963f66afa6 as User is not found"

def test_put_recipe_tag_with_invalid_creator_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        json={
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afaz"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_recipe_tag_with_empty_creator_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        json={
            "created_by": ""
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_delete_recipe_tag(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Id 13444244-43b2-4d63-a080-604dd5088452 as Recipe Tag is deleted successfully"

def test_delete_recipe_tag_with_invalid_token(client: TestClient):
    response = client.delete(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_delete_recipe_tag_without_token(client: TestClient):
    response = client.delete(f"{url_prefix}/13444244-43b2-4d63-a080-604dd5088452")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_delete_recipe_tag_by_wrong_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/db67b3f4-0e04-47bb-bc46-94826847ee4f",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Id db67b3f4-0e04-47bb-bc46-94826847ee4f as Recipe Tag is not found"
