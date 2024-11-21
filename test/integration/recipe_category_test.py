from fastapi.testclient import TestClient


url_prefix = '/recipe_categories'
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

def test_get_recipe_category_list(client: TestClient):
    response = client.get(f"{url_prefix}/")

    assert response.status_code == 200
    assert response.json()["detail"] == "Recipe Category list is retrieved successfully"

    recipe_categories = response.json()["recipe_categories"]

    assert isinstance(recipe_categories, list)
    assert len(recipe_categories) == 2

    assert recipe_categories[0]['id'] == "4053a7e8-9ae5-415d-9bed-e4d0a235f481"
    assert recipe_categories[0]['name'] == "breakfast"
    assert recipe_categories[0]["creator"]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_categories[0]
    assert "created_date" in recipe_categories[0]

    assert recipe_categories[1]['id'] == "5ce3381f-2298-44bd-b41c-a19d4b69e7a1"
    assert recipe_categories[1]['name'] == "lunch"
    assert recipe_categories[1]["creator"]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_categories[1]
    assert "created_date" in recipe_categories[1]

def test_get_recipe_category_by_id(client: TestClient):
    response = client.get(f"{url_prefix}/4053a7e8-9ae5-415d-9bed-e4d0a235f481")

    assert response.status_code == 200
    assert response.json()["detail"] == f"Id 4053a7e8-9ae5-415d-9bed-e4d0a235f481 as Recipe Category is retrieved successfully"

    recipe_category = response.json()["recipe_category"]
    
    assert recipe_category['id'] == "4053a7e8-9ae5-415d-9bed-e4d0a235f481"
    assert recipe_category["creator"]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe_category['name'] == "breakfast"
    assert "updated_date" in recipe_category
    assert "created_date" in recipe_category

def test_get_recipe_category_by_wrong_id(client: TestClient):
    response = client.get(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f01")

    assert response.status_code == 404
    assert response.json()['detail'] == "Id b4b165f6-a4f2-45f6-bda6-0a49092d3f01 as Recipe Category is not found"


#TODO! str hex error due to created_by_id 
def test_post_recipe_category(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test recipe category",
        "created_by": ADMIN_ID
    })

    assert response.status_code == 201
    assert response.json()["detail"] == f"test ingredient category as Recipe Category is successfully created"

    recipe_category = response.json()["recipe_category"]

    assert recipe_category['name'] == "test recipe category"
    assert recipe_category["creator"]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_category
    assert "created_date" in recipe_category

def test_post_recipe_category_with_duplicate_name(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "breakfast",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 400
    assert response.json()["detail"] == f"breakfast as Recipe Category is already registered"

def test_post_recipe_category_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 400
    assert response.json()['detail'] == ""

def test_put_recipe_category(client: TestClient):
    response = client.post(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", json={
        "name": "updated ingredient category",
    })

    assert response.status_code == 202

    recipe_category = response.json()

    assert recipe_category["message"] == ""
    assert recipe_category['id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert recipe_category['name'] == "updatedingredientcategory"
    assert recipe_category["creator"]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_category
    assert "created_date" in recipe_category

def test_put_recipe_category_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03", json={
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
