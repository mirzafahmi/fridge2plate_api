from fastapi.testclient import TestClient


url_prefix = '/ingredient_categories'
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

def test_get_ingredient_category_list(client: TestClient):
    response = client.get(f"{url_prefix}/")

    assert response.status_code == 200

    ingredient_categories = response.json()

    assert isinstance(ingredient_categories, list)
    assert len(ingredient_categories) == 2

    assert ingredient_categories[0]['id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient_categories[0]['name'] == "protein"
    assert ingredient_categories[0]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient_categories[0]
    assert "created_date" in ingredient_categories[0]

    assert ingredient_categories[1]['id'] == "6722eb62-884a-4208-8596-ed82d310e832"
    assert ingredient_categories[1]['name'] == "vegetables"
    assert ingredient_categories[1]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient_categories[1]
    assert "created_date" in ingredient_categories[1]

def test_get_ingredient_category_by_id(client: TestClient):
    response = client.get(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03")

    assert response.status_code == 200

    ingredient_category = response.json()
    
    assert ingredient_category["message"] == ""
    assert ingredient_category["data"]['id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient_category["data"]['name'] == "protein"
    assert ingredient_category["data"]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient_category["data"]
    assert "created_date" in ingredient_category["data"]

def test_get_ingredient_category_by_wrong_id(clent: TestClient):
    response = client.get(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f01")

    assert response.status_code == 400
    assert response.json()['detail'] == 'Ingredient category is not found'

def test_post_ingredient_category(client: TestClient):
    response = client.post(f"{url_prefix}/", body={
        "id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "name": "test ingredient category",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 200

    ingredient_category = response.json()

    assert ingredient_category["message"] == ""
    assert ingredient_category["data"]['id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient_category["data"]['name'] == "testingredientcategory"
    assert ingredient_category["data"]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient_category["data"]
    assert "created_date" in ingredient_category["data"]

def test_post_ingredient_category_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/", body={
        "id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "name": "",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 400
    assert response.json()['detail'] == 'Ingredient category is not found'

def test_put_ingredient_category(client: TestClient):
    response = client.post(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", body={
        "name": "updated ingredient category",
    })

    assert response.status_code == 202

    ingredient_category = response.json()

    assert ingredient_category["message"] == ""
    assert ingredient_category["data"]['id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert ingredient_category["data"]['name'] == "updatedingredientcategory"
    assert ingredient_category["data"]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in ingredient_category["data"]
    assert "created_date" in ingredient_category["data"]

def test_put_ingredient_category_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", body={
        "name": "",
    })

    assert response.status_code == 400
    assert response.json()['detail'] == ''

def test_delete_ingredient_category(client: TestClient):
    response = client.delete(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03")

    assert response.status_code == 200
    assert response.json()['detail'] == ''

def test_delete_ingredient_category_by_wrong_id(client: TestClient):
    response = client.delete(f"{url_prefix}/db67b3f4-0e04-47bb-bc46-94826847ee4f")

    assert response.status_code == 200
    assert response.json()['detail'] == ''
