from fastapi.testclient import TestClient


url_prefix = '/recipeorigins'
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

#TODO! make all list have message returned
def test_get_recipe_list(client: TestClient):
    response = client.get(f"{url_prefix}/")

    assert response.status_code == 200

    recipeorigins = response.json()

    assert isinstance(recipeorigins, list)
    assert len(recipeorigins) == 2

    assert recipeorigins[0]['id'] == "92e80174-c259-480a-80b5-f5b0d32ca005"
    assert recipeorigins[0]['name'] == "malay"
    assert recipeorigins[0]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipeorigins[0]
    assert "created_date" in recipeorigins[0]

    assert recipeorigins[1]['id'] == "c7048030-10ff-486c-9e78-7417212dd728"
    assert recipeorigins[1]['name'] == "italian"
    assert recipeorigins[1]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipeorigins[1]
    assert "created_date" in recipeorigins[1]

def test_get_recipe_origin_by_id(client: TestClient):
    response = client.get(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005")

    assert response.status_code == 200

    recipe_origin = response.json()
    
    assert recipe_origin["message"] == ""
    assert recipe_origin["data"]['id'] == "92e80174-c259-480a-80b5-f5b0d32ca005"
    assert recipe_origin["data"]['name'] == "malay"
    assert recipe_origin["data"]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_origin["data"]
    assert "created_date" in recipe_origin["data"]

def test_get_recipe_origin_by_wrong_id(clent: TestClient):
    response = client.get(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f01")

    assert response.status_code == 404
    assert response.json()['detail'] == ""

def test_post_recipe_origin(client: TestClient):
    response = client.post(f"{url_prefix}/", body={
        "id": "b4b165f6-a4f2-45f6-bda6-0a49092d3f03",
        "name": "test recipe origin",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 200

    recipe_origin = response.json()

    assert recipe_origin["message"] == ""
    assert recipe_origin["data"]['id'] == "b4b165f6-a4f2-45f6-bda6-0a49092d3f03"
    assert recipe_origin["data"]['name'] == "test recipe origin"
    assert recipe_origin["data"]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_origin["data"]
    assert "created_date" in recipe_origin["data"]

def test_post_recipe_origin_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/", body={
        "name": "",
        "created_by_id": ADMIN_ID
    })

    assert response.status_code == 400
    assert response.json()['detail'] == ""

def test_put_recipe_origin(client: TestClient):
    response = client.post(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", body={
        "name": "updated ingredient origin",
    })

    assert response.status_code == 202

    recipe_origin = response.json()

    assert recipe_origin["message"] == ""
    assert recipe_origin["data"]['id'] == "92e80174-c259-480a-80b5-f5b0d32ca005"
    assert recipe_origin["data"]['name'] == "updated ingredient origin"
    assert recipe_origin["data"]['created_by_id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_origin["data"]
    assert "created_date" in recipe_origin["data"]

def test_put_recipe_origin_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", body={
        "name": "",
    })

    assert response.status_code == 400
    assert response.json()['detail'] == ''

def test_delete_recipe_origin(client: TestClient):
    response = client.delete(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f03")

    assert response.status_code == 200
    assert response.json()['detail'] == ''

def test_delete_recipe_origin_by_wrong_id(client: TestClient):
    response = client.delete(f"{url_prefix}/db67b3f4-0e04-47bb-bc46-94826847ee4f")

    assert response.status_code == 404
    assert response.json()['detail'] == ''
