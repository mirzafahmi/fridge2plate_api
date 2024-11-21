from fastapi.testclient import TestClient


url_prefix = '/recipe_categories'
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

#TODO! make all list have message returned
def test_get_recipe_category_list(client: TestClient):
    response = client.get(f"{url_prefix}/")

    assert response.status_code == 200

    recipe_categories = response.json()

    assert isinstance(recipe_categories, list)
    assert len(recipe_categories) == 2

    assert recipe_categories[0]['id'] == "4053a7e8-9ae5-415d-9bed-e4d0a235f481"
    assert recipe_categories[0]['name'] == "breakfast"
    assert recipe_categories[0]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_categories[0]
    assert "created_date" in recipe_categories[0]

    assert recipe_categories[1]['id'] == "5ce3381f-2298-44bd-b41c-a19d4b69e7a1"
    assert recipe_categories[1]['name'] == "lunch"
    assert recipe_categories[1]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_categories[1]
    assert "created_date" in recipe_categories[1]

def test_get_recipe_category_by_id(client: TestClient):
    response = client.get(f"{url_prefix}/4053a7e8-9ae5-415d-9bed-e4d0a235f481")

    assert response.status_code == 200

    recipe_category = response.json()
    
    assert recipe_category["message"] == ""
    assert recipe_category["data"]['id'] == "4053a7e8-9ae5-415d-9bed-e4d0a235f481"
    assert recipe_category["data"]['name'] == "breakfast"
    assert recipe_category["data"]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_category["data"]
    assert "created_date" in recipe_category["data"]

def test_get_recipe_category_by_wrong_id(clent: TestClient):
    response = client.get(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f01")

    assert response.status_code == 404
    assert response.json()['detail'] == ""

def test_post_recipe_category(client: TestClient):
    response = client.post(f"{url_prefix}/", body={
        "id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "name": "test recipe category",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 200

    recipe_category = response.json()

    assert recipe_category["message"] == ""
    assert recipe_category["data"]['id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert recipe_category["data"]['name'] == "testrecipecategory"
    assert recipe_category["data"]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_category["data"]
    assert "created_date" in recipe_category["data"]

def test_post_recipe_category_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/", body={
        "name": "",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 400
    assert response.json()['detail'] == ""

def test_put_recipe_category(client: TestClient):
    response = client.post(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", body={
        "name": "updated ingredient category",
    })

    assert response.status_code == 202

    recipe_category = response.json()

    assert recipe_category["message"] == ""
    assert recipe_category["data"]['id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert recipe_category["data"]['name'] == "updatedingredientcategory"
    assert recipe_category["data"]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_category["data"]
    assert "created_date" in recipe_category["data"]

def test_put_recipe_category_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", body={
        "name": "",
    })

    assert response.status_code == 400
    assert response.json()['detail'] == ''

def test_delete_recipe_category(client: TestClient):
    response = client.delete(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03")

    assert response.status_code == 200
    assert response.json()['detail'] == ''

def test_delete_recipe_category_by_wrong_id(client: TestClient):
    response = client.delete(f"{url_prefix}/db67b3f4-0e04-47bb-bc46-94826847ee4f")

    assert response.status_code == 404
    assert response.json()['detail'] == ''
