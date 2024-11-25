from fastapi.testclient import TestClient


url_prefix = '/recipe_origins'
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

def test_get_recipe_origin_list(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Recipe Origin list is retrieved successfully"

    recipeorigins = response.json()["recipe_origins"]

    assert isinstance(recipeorigins, list)
    assert len(recipeorigins) == 2

    assert recipeorigins[0]['id'] == "c7048030-10ff-486c-9e78-7417212dd728"
    assert recipeorigins[0]['name'] == "italian"
    assert recipeorigins[0]["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipeorigins[0]
    assert "created_date" in recipeorigins[0]

    assert recipeorigins[1]['id'] == "92e80174-c259-480a-80b5-f5b0d32ca005"
    assert recipeorigins[1]['name'] == "malay"
    assert recipeorigins[1]["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipeorigins[1]
    assert "created_date" in recipeorigins[1]

def test_get_recipe_origin_list_with_invalid_token(client: TestClient):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_recipe_origin_list_without_token(client: TestClient):
    response = client.get(f"{url_prefix}/")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_recipe_origin_by_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"Id 92e80174-c259-480a-80b5-f5b0d32ca005 as Recipe Origin is retrieved successfully"

    recipe_origin = response.json()["recipe_origin"]
    
    assert recipe_origin['id'] == "92e80174-c259-480a-80b5-f5b0d32ca005"
    assert recipe_origin['name'] == "malay"
    assert recipe_origin["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_origin
    assert "created_date" in recipe_origin

def test_get_recipe_origin_by_id_with_invalid_token(client: TestClient):
    response = client.get(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_recipe_origin_by_id_without_token(client: TestClient):
    response = client.get(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_recipe_origin_by_wrong_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f01", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Id b4b165f6-a4f2-45f6-bda6-0a49092d3f01 as Recipe Origin is not found"

def test_post_recipe_origin(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test recipe origin",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["detail"] == f"test recipe origin as Recipe Origin is created successfully"

    recipe_origin = response.json()["recipe_origin"]

    assert recipe_origin["name"] == "test recipe origin"
    assert recipe_origin["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_origin
    assert "created_date" in recipe_origin

def test_post_recipe_origin_with_invalid_token(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test recipe origin",
        "created_by": ADMIN_ID
    }, 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_post_recipe_origin_without_token(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test recipe origin",
        "created_by": ADMIN_ID
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_post_recipe_origin_with_various_letter_case(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "tESt reCIPe orIGIn",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["detail"] == f"test recipe origin as Recipe Origin is created successfully"

    recipe_origin = response.json()["recipe_origin"]

    assert recipe_origin["name"] == "test recipe origin"
    assert recipe_origin["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_origin
    assert "created_date" in recipe_origin

def test_post_recipe_origin_with_duplicate_name(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "malay",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == f"malay as Recipe Origin is already registered"

def test_post_recipe_origin_with_empty_name(client: TestClient, token: str):
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

def test_post_recipe_origin_without_name(client: TestClient, token: str):
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

def test_post_recipe_origin_with_not_available_creator_id(client: TestClient, token: str): 
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test recipe origin",
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 3fa85f64-5717-4562-b3fc-2c963f66afa6 as User is not found"

def test_post_recipe_origin_with_invalid_creator_id(client: TestClient, token: str): 
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test recipe origin",
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

def test_post_recipe_origin_with_empty_creator_id(client: TestClient, token: str): 
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test recipe origin",
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

def test_put_recipe_origin_by_changing_name(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
        json={
            "name": "updated ingredient origin",
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 202
    assert response.json()["detail"] == "Id 92e80174-c259-480a-80b5-f5b0d32ca005 as Recipe Origin is updated successfully"

    recipe_origin = response.json()["recipe_origin"]

    assert recipe_origin['id'] == "92e80174-c259-480a-80b5-f5b0d32ca005"
    assert recipe_origin['name'] == "updated ingredient origin"
    assert recipe_origin["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_origin
    assert "created_date" in recipe_origin

def test_put_recipe_origin_by_changing_name_with_invalid_token(client: TestClient):
    response = client.put(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
        json={
            "name": "updated ingredient origin",
        }, 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_put_recipe_origin_by_changing_name_without_token(client: TestClient):
    response = client.put(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
        json={
            "name": "updated ingredient origin",
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_put_recipe_origin_by_changing_name_with_various_letter_case(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
        json={
            "name": "upDATed ingREDient orIGIn",
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 202
    assert response.json()["detail"] == "Id 92e80174-c259-480a-80b5-f5b0d32ca005 as Recipe Origin is updated successfully"

    recipe_origin = response.json()["recipe_origin"]

    assert recipe_origin['id'] == "92e80174-c259-480a-80b5-f5b0d32ca005"
    assert recipe_origin['name'] == "updated ingredient origin"
    assert recipe_origin["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_origin
    assert "created_date" in recipe_origin

def test_put_recipe_origin_by_changing_name_with_duplicate_name(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
        json={
            "name": "italian",
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == f"italian as Recipe Origin is already registered"

def test_put_recipe_origin_by_changing_name_with_empty_name(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
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

def test_put_recipe_origin_with_not_available_creator_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
        json={
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 3fa85f64-5717-4562-b3fc-2c963f66afa6 as User is not found"

def test_put_recipe_origin_with_invalid_creator_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
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

def test_put_recipe_origin_with_empty_creator_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
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

def test_delete_recipe_origin(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Id 92e80174-c259-480a-80b5-f5b0d32ca005 as Recipe Origin is deleted successfully"

def test_delete_recipe_origin_with_invalid_token(client: TestClient):
    response = client.delete(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_delete_recipe_origin_without_token(client: TestClient):
    response = client.delete(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_delete_recipe_origin_by_wrong_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/db67b3f4-0e04-47bb-bc46-94826847ee4f", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Id db67b3f4-0e04-47bb-bc46-94826847ee4f as Recipe Origin is not found"
