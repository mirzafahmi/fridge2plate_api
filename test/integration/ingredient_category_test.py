from fastapi.testclient import TestClient


url_prefix = '/ingredient_categories'
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

def test_get_ingredient_category_list(client: TestClient):
    response = client.get(f"{url_prefix}/")

    assert response.status_code == 200
    assert response.json()["detail"] == "Ingredient Category list is retrieved successfully"

    ingredient_categories = response.json()['ingredient_categories']

    assert isinstance(ingredient_categories, list)
    assert len(ingredient_categories) == 2

    assert ingredient_categories[0]['id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient_categories[0]['name'] == "proteins"
    assert ingredient_categories[0]["creator"]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient_categories[0]
    assert "created_date" in ingredient_categories[0]

    assert ingredient_categories[1]['id'] == "6722eb62-884a-4208-8596-ed82d310e832"
    assert ingredient_categories[1]['name'] == "vegetables"
    assert ingredient_categories[1]["creator"]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient_categories[1]
    assert "created_date" in ingredient_categories[1]

def test_get_ingredient_category_by_id(client: TestClient):
    response = client.get(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03")

    assert response.status_code == 200
    assert response.json()["detail"] == f"Id b4b165f6-a4f2-45f6-bda6-0a49092d3f03 as Ingredient Category is retrieved successfully"

    ingredient_category = response.json()["ingredient_category"]
    
    assert ingredient_category['id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient_category['name'] == "proteins"
    assert ingredient_category["creator"]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient_category
    assert "created_date" in ingredient_category

def test_get_ingredient_category_by_wrong_id(client: TestClient):
    response = client.get(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f01")

    assert response.status_code == 404
    assert response.json()['detail'] == "Id b4b165f6-a4f2-45f6-bda6-0a49092d3f01 as Ingredient Category is not found"

def test_post_ingredient_category(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test ingredient category",
        "created_by": ADMIN_ID
    })

    assert response.status_code == 201
    assert response.json()["detail"] == f"test ingredient category as Ingredient Category is successfully created"

    ingredient_category = response.json()["ingredient_category"]

    assert ingredient_category["name"] == "test ingredient category"
    assert ingredient_category["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient_category
    assert "created_date" in ingredient_category

def test_post_ingredient_category_with_duplicate_name(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "proteins",
        "created_by": ADMIN_ID
    })

    assert response.status_code == 400
    assert response.json()["detail"] == f"proteins as Ingredient Category is already registered"

def test_post_ingredient_category_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "",
        "created_by": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_ingredient_category_with_not_available_creator_id(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test ingredient category",
        "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    })

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 3fa85f64-5717-4562-b3fc-2c963f66afa6 as User is not found"

def test_post_ingredient_category_with_invalid_creator_id(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test ingredient category",
        "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afaz"
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_ingredient_category_with_empty_creator_id(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test ingredient category",
        "created_by": ""
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_ingredient_category(client: TestClient):
    response = client.put(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", json={
        "name": "updated ingredient category",
    })

    assert response.status_code == 202
    assert response.json()["detail"] == "Id b4b165f6-a4f2-45f6-bda6-0a49092d3f03 as Ingredient Category is successfully updated"

    ingredient_category = response.json()["ingredient_category"]

    assert ingredient_category["id"] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient_category["name"] == "updated ingredient category"
    assert ingredient_category["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient_category
    assert "created_date" in ingredient_category

def test_put_ingredient_category_with_duplicate_name(client: TestClient):
    response = client.put(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", json={
        "name": "vegetables",
    })

    assert response.status_code == 400
    assert response.json()["detail"] == f"'vegetables' as Ingredient Category is already exists"

def test_put_ingredient_category_with_empty_name(client: TestClient):
    response = client.put(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", json={
        "name": "",
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_put_ingredient_category_with_not_available_creator_id(client: TestClient):
    response = client.put(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", json={
        "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    })

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 3fa85f64-5717-4562-b3fc-2c963f66afa6 as User is not found"

def test_put_ingredient_category_with_invalid_creator_id(client: TestClient):
    response = client.put(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", json={
        "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afaz"
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_ingredient_category_with_empty_creator_id(client: TestClient):
    response = client.put(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", json={
        "created_by": ""
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_delete_ingredient_category(client: TestClient):
    response = client.delete(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03")

    assert response.status_code == 200
    assert response.json()['detail'] == "Id b4b165f6-a4f2-45f6-bda6-0a49092d3f03 as Ingredient Category is successfully deleted"

def test_delete_ingredient_category_by_wrong_id(client: TestClient):
    response = client.delete(f"{url_prefix}/db67b3f4-0e04-47bb-bc46-94826847ee4f")

    assert response.status_code == 404
    assert response.json()['detail'] == "Id db67b3f4-0e04-47bb-bc46-94826847ee4f as Ingredient Category is not found"
