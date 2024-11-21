from fastapi.testclient import TestClient


url_prefix = '/ingredients'
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

#TODO! sort all get list asc to avoid error
def test_get_list(client: TestClient):
    response = client.get(f"{url_prefix}/")

    assert response.status_code == 200

    ingredients = response.json()

    assert isinstance(ingredients, list)
    assert len(ingredients) == 2

    assert ingredients[0]['id'] == "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    assert ingredients[0]['name'] == "chicken"
    assert ingredients[0]['ingredient_category_id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredients[0]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredients[0]
    assert "created_date" in ingredients[0]

    assert ingredients[1]['id'] == "b3cceb34-9465-4020-9066-f7b5ce3c372c"
    assert ingredients[1]['name'] == "vegetables"
    assert ingredients[0]['ingredient_category_id'] == "6722eb62-884a-4208-8596-ed82d310e832"
    assert ingredients[1]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredients[1]
    assert "created_date" in ingredients[1]

def test_get_ingredient_by_id(client: TestClient):
    response = client.get(f"{url_prefix}/423f2e0f-d5cc-48dc-8b06-e987a3d8ea84")

    assert response.status_code == 200

    ingredient = response.json()
    
    assert ingredient["message"] == ""
    assert ingredient["data"]['id'] == "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84"
    assert ingredient["data"]['name'] == "chicken"
    assert ingredient["data"]['ingredient_category_id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient["data"]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient["data"]
    assert "created_date" in ingredient["data"]

def test_get_ingredient_by_wrong_id(clent: TestClient):
    response = client.get(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f01")

    assert response.status_code == 400
    assert response.json()['detail'] == 'Ingredients is not found'

def test_post_ingredient(client: TestClient):
    response = client.post(f"{url_prefix}/", body={
        "id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "name": "test ingredient",
        "ingredient_category_id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 200

    ingredient = response.json()

    assert ingredient["message"] == ""
    assert ingredient["data"]['id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient["data"]['name'] == "testingredient"
    assert ingredient["data"]['ingredient_category_id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient["data"]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient["data"]
    assert "created_date" in ingredient["data"]

def test_post_ingredient_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/", body={
        "id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "name": "",
        "ingredient_category_id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 400
    assert response.json()['detail'] == 'Ingredient category is not found'

def test_post_ingredient_without_ingredient_category_id(client: TestClient):
    pass

def test_post_ingredient_with_wrong_ingredient_category_id(client: TestClient):
    pass

def test_put_ingredient_by_changing_name(client: TestClient):
    response = client.post(f"{url_prefix}/423f2e0f-d5cc-48dc-8b06-e987a3d8ea84", body={
        "name": "updated ingredient",
    })

    assert response.status_code == 202

    ingredient = response.json()

    assert ingredient["message"] == ""
    assert ingredient["data"]['id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient["data"]['name'] == "updatedingredient"
    assert ingredient["data"]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient["data"]
    assert "created_date" in ingredient["data"]

def test_put_ingredient_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", body={
        "name": "",
    })

    assert response.status_code == 400
    assert response.json()['detail'] == ''

def test_put_ingredient_by_changing_ingredient_category_id(client: TestClient):
    pass

def test_put_ingredient_by_changing_created_by_id(client: TestClient):
    pass

def test_delete_ingredient(client: TestClient):
    response = client.delete(f"{url_prefix}/423f2e0f-d5cc-48dc-8b06-e987a3d8ea84")

    assert response.status_code == 200
    assert response.json()['detail'] == ''

def test_delete_ingredient_by_wrong_id(client: TestClient):
    response = client.delete(f"{url_prefix}/db67b3f4-0e04-47bb-bc46-94826847ee4f")

    assert response.status_code == 400
    assert response.json()['detail'] == ''
