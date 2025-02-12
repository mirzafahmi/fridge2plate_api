from fastapi.testclient import TestClient
import pytest


url_prefix = '/recipe_form'
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

def test_get_recipe_form_list(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Recipe form field is retrieved successfully"

    fields = response.json()["recipe_form_fields"]


    recipe_categories = fields["recipe_categories"]

    assert isinstance(recipe_categories, list)
    assert len(recipe_categories) == 2

    assert recipe_categories[0]["id"] == "4053a7e8-9ae5-415d-9bed-e4d0a235f481"
    assert recipe_categories[0]["name"] == "breakfast"
    assert recipe_categories[0]["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_categories[0]
    assert "created_date" in recipe_categories[0]

    assert recipe_categories[1]["id"] == "5ce3381f-2298-44bd-b41c-a19d4b69e7a1"
    assert recipe_categories[1]["name"] == "lunch"
    assert recipe_categories[1]["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_categories[1]
    assert "created_date" in recipe_categories[1]


    recipe_origins = fields["recipe_origins"]

    assert isinstance(recipe_origins, list)
    assert len(recipe_origins) == 2

    assert recipe_origins[0]['id'] == "c7048030-10ff-486c-9e78-7417212dd728"
    assert recipe_origins[0]['name'] == "italian"
    assert recipe_origins[0]["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_origins[0]
    assert "created_date" in recipe_origins[0]

    assert recipe_origins[1]['id'] == "92e80174-c259-480a-80b5-f5b0d32ca005"
    assert recipe_origins[1]['name'] == "malay"
    assert recipe_origins[1]["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in recipe_origins[1]
    assert "created_date" in recipe_origins[1]


    recipe_tags = fields["recipe_tags"]

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


    ingredients = fields["ingredients"]

    assert isinstance(ingredients, list)
    assert len(ingredients) == 3

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


    uoms = fields["uoms"]

    assert isinstance(uoms, list)
    assert len(uoms) == 2

    assert uoms[0]['id'] == "8c935f60-2f3a-410a-9860-09bb2c270a38"
    assert uoms[0]['name'] == "clove"
    assert uoms[0]['unit'] == "clove"
    assert uoms[0]['weightage'] == 1.0
    assert uoms[0]["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in uoms[0]
    assert "created_date" in uoms[0]

    assert uoms[1]['id'] == "13444244-43b2-4d63-a080-604dd5088452"
    assert uoms[1]['name'] == "piece"
    assert uoms[1]['name'] == "piece"
    assert uoms[1]['weightage'] == 1.0
    assert uoms[1]["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in uoms[1]
    assert "created_date" in uoms[1]

def test_get_recipe_form_list_with_invalid_token(client: TestClient):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_recipe_form_list_without_token(client: TestClient):
    response = client.get(f"{url_prefix}/")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"