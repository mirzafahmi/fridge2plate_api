from fastapi.testclient import TestClient


url_prefix = "/ingredients"
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

#TODO!: test with unique constraint error like name field
def test_get_ingredient_list(client: TestClient):
    response = client.get(f"{url_prefix}/")
    print(response.json())
    assert response.status_code == 200
    assert response.json()["detail"] == "Ingredient list is retrieved successfully"

    ingredients = response.json()["ingredients"]

    assert isinstance(ingredients, list)
    assert len(ingredients) == 2

    assert ingredients[0]["id"] == "b3cceb34-9465-4020-9066-f7b5ce3c372c"
    assert ingredients[0]["name"] == "carrot"
    assert ingredients[0]["brand"] == "carrot"
    assert ingredients[0]["ingredient_category"]["id"] == "6722eb62-884a-4208-8596-ed82d310e832"
    assert ingredients[0]["ingredient_category"]["name"] == "vegetables"
    assert ingredients[0]["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredients[0]
    assert "created_date" in ingredients[0]

    assert ingredients[1]["id"] == "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    assert ingredients[1]["name"] == "chicken"
    assert ingredients[1]["brand"] == "chicken"
    assert ingredients[1]["ingredient_category"]["id"] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredients[1]["ingredient_category"]["name"] == "proteins"
    assert ingredients[1]["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredients[1]
    assert "created_date" in ingredients[1]

def test_get_ingredient_by_id(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.get(f"{url_prefix}/{ingredient_id}")

    assert response.status_code == 200
    assert response.json()["detail"] == f"Id {ingredient_id} as Ingredient Category is retrieved successfully"
    
    ingredient = response.json()["ingredient"]
    
    assert ingredient["id"] == "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    assert ingredient["name"] == "chicken"
    assert ingredient["brand"] == "chicken"
    assert ingredient["ingredient_category"]["id"] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient["ingredient_category"]["name"] == "proteins"
    assert ingredient["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient
    assert "created_date" in ingredient

def test_get_ingredient_by_wrong_id(client: TestClient):
    ingredient_id = "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    response = client.get(f"{url_prefix}/{ingredient_id}")
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == f"Id {ingredient_id} as Ingredient is not found"

def test_post_ingredient(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test ingredient",
        "brand": "test ingredient brand",
        "ingredient_category_id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "created_by": ADMIN_ID
    })

    assert response.status_code == 201
    assert response.json()["detail"] == f"test ingredient as Ingredient is successfully created"

    ingredient = response.json()["ingredient"]

    assert ingredient["name"] == "test ingredient"
    assert ingredient["brand"] == "test ingredient brand"
    assert ingredient["ingredient_category"]["id"] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient["ingredient_category"]["name"] == "proteins"
    assert ingredient["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient
    assert "created_date" in ingredient

def test_post_ingredient_with_various_letter_case(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "teST inGREdient",
        "brand": "tESt INgredient bRAnd",
        "ingredient_category_id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "created_by": ADMIN_ID
    })

    assert response.status_code == 201
    assert response.json()["detail"] == f"test ingredient as Ingredient is successfully created"

    ingredient = response.json()["ingredient"]

    assert ingredient["name"] == "test ingredient"
    assert ingredient["brand"] == "test ingredient brand"
    assert ingredient["ingredient_category"]["id"] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient["ingredient_category"]["name"] == "proteins"
    assert ingredient["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient
    assert "created_date" in ingredient

def test_post_ingredient_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "brand": "test ingredient brand",
        "ingredient_category_id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_ingredient_with_empty_name(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "name": "",
        "brand": "test ingredient brand",
        "ingredient_category_id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_ingredient_without_brand(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "name": "test ingredient",
        "ingredient_category_id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "brand"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_ingredient_with_empty_brand(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "name": "test ingredient",
        "brand": "",
        "ingredient_category_id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "brand"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_ingredient_with_wrong_ingredient_category_id(client: TestClient):
    ingredient_category_id = "b4b165f6-a4f2-45f6-bda6-0a49092d3f02"
    response = client.post(f"{url_prefix}/", json={
        "name": "test ingredient",
        "brand": "test ingredient brand",
        "ingredient_category_id": f"{ingredient_category_id}",
        "created_by": ADMIN_ID
    })

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id {ingredient_category_id} as Ingredient Category is not found"

def test_post_ingredient_with_invalid_category_id(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test ingredient",
        "brand": "test ingredient brand",
        "ingredient_category_id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f0z",
        "created_by": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "ingredient_category_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_ingredient_with_empty_ingredient_category_id(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "name": "test ingredient",
        "brand": "test ingredient brand",
        "ingredient_category_id": "", 
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredient_category_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_ingredient_without_ingredient_category_id(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "name": "test ingredient",
        "brand": "test ingredient brand",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredient_category_id"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_put_ingredient_by_changing_name(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "name": "updated ingredient",
    })

    assert response.status_code == 202
    assert response.json()["detail"] == f"Id {ingredient_id} as Ingredient is successfully updated"

    ingredient = response.json()["ingredient"]

    assert ingredient["id"] == "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    assert ingredient["name"] == "updated ingredient"
    assert ingredient["brand"] == "chicken"
    assert ingredient["ingredient_category"]["id"] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient["ingredient_category"]["name"] == "proteins"
    assert ingredient["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient
    assert "created_date" in ingredient

def test_put_ingredient_by_changing_name_with_various_letter_case(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "name": "upDAted inGREdient",
    })

    assert response.status_code == 202
    assert response.json()["detail"] == f"Id {ingredient_id} as Ingredient is successfully updated"

    ingredient = response.json()["ingredient"]

    assert ingredient["id"] == "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    assert ingredient["name"] == "updated ingredient"
    assert ingredient["brand"] == "chicken"
    assert ingredient["ingredient_category"]["id"] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient["ingredient_category"]["name"] == "proteins"
    assert ingredient["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient
    assert "created_date" in ingredient

def test_put_ingredient_by_changing_name_with_empty_name(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "name": "",
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_put_ingredient_by_changing_brand(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "brand": "updated ingredient brand",
    })

    assert response.status_code == 202
    assert response.json()["detail"] == f"Id {ingredient_id} as Ingredient is successfully updated"

    ingredient = response.json()["ingredient"]

    assert ingredient["id"] == "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    assert ingredient["name"] == "chicken"
    assert ingredient["brand"] == "updated ingredient brand"
    assert ingredient["ingredient_category"]["id"] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient["ingredient_category"]["name"] == "proteins"
    assert ingredient["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient
    assert "created_date" in ingredient

def test_put_ingredient_by_changing_brand_with_various_letter_case(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "brand": "upDAted ingREDient bRAnd",
    })

    assert response.status_code == 202
    assert response.json()["detail"] == f"Id {ingredient_id} as Ingredient is successfully updated"

    ingredient = response.json()["ingredient"]

    assert ingredient["id"] == "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    assert ingredient["name"] == "chicken"
    assert ingredient["brand"] == "updated ingredient brand"
    assert ingredient["ingredient_category"]["id"] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient["ingredient_category"]["name"] == "proteins"
    assert ingredient["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient
    assert "created_date" in ingredient

def test_put_ingredient_with_empty_brand(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "brand": "",
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "brand"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_put_ingredient_by_changing_ingredient_category_id(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "ingredient_category_id": "6722eb62-884a-4208-8596-ed82d310e832",
    })

    assert response.status_code == 202
    assert response.json()["detail"] == f"Id {ingredient_id} as Ingredient is successfully updated"

    ingredient = response.json()["ingredient"]

    assert ingredient["id"] == "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    assert ingredient["name"] == "chicken"
    assert ingredient["brand"] == "chicken"
    assert ingredient["ingredient_category"]["id"] == "6722eb62-884a-4208-8596-ed82d310e832"
    assert ingredient["ingredient_category"]["name"] == "vegetables"
    assert ingredient["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient
    assert "created_date" in ingredient

def test_put_ingredient_by_changing_ingredient_category_id_with_not_available_id(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "ingredient_category_id": "6722eb62-884a-4208-8596-ed82d310e833",
    })

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 6722eb62-884a-4208-8596-ed82d310e833 as Ingredient Category is not found"

def test_put_ingredient_by_changing_ingredient_category_id_with_invalid_id(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "ingredient_category_id": "6722eb62-884a-4208-8596-ed82d310e83z",
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "ingredient_category_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_ingredient_by_changing_ingredient_category_id_with_empty_id(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "ingredient_category_id": "",
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredient_category_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_ingredient_by_changing_created_by_id(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "created_by": "0c619092-817e-4f73-b25f-8e187e69dded",
    })

    assert response.status_code == 202
    assert response.json()["detail"] == f"Id {ingredient_id} as Ingredient is successfully updated"

    ingredient = response.json()["ingredient"]

    assert ingredient["id"] == "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    assert ingredient["name"] == "chicken"
    assert ingredient["brand"] == "chicken"
    assert ingredient["ingredient_category"]["id"] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient["ingredient_category"]["name"] == "proteins"
    assert ingredient["creator"]["id"] == "0c619092-817e-4f73-b25f-8e187e69dded"
    assert "updated_date" in ingredient
    assert "created_date" in ingredient

def test_put_ingredient_by_changing_created_by_id_with_not_available_id(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "created_by": "0c619092-817e-4f73-b25f-8e187e69ddee",
    })

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 0c619092-817e-4f73-b25f-8e187e69ddee as User is not found"

def test_put_ingredient_by_changing_created_by_id_with_invalid_uuid(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "created_by": "0c619092-817e-4f73-b25f-8e187e69ddez",
    })

    assert response.status_code == 422

    response_json = response.json()
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_ingredient_by_changing_created_by_id_with_empty_uuid(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.put(f"{url_prefix}/{ingredient_id}", json={
        "created_by": "",
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_delete_ingredient(client: TestClient):
    ingredient_id = "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    response = client.delete(f"{url_prefix}/{ingredient_id}")

    assert response.status_code == 200
    assert response.json()["detail"] == f"Id {ingredient_id} as Ingredient is successfully deleted"

def test_delete_ingredient_by_wrong_id(client: TestClient):
    ingredient_id = "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    response = client.delete(f"{url_prefix}/{ingredient_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id {ingredient_id} as Ingredient is not found"
