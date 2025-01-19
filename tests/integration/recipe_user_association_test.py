from fastapi.testclient import TestClient
from datetime import datetime
from uuid import UUID

from utils.datetime_utils import DateTimeUtils

url_prefix = '/recipes'
recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"


def get_recipe_by_id(client: TestClient, token: str, recipe_id: UUID, toggle_action: str, expected_state: bool):
    response = client.get(f"{url_prefix}/{recipe_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe is retrieved successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["images"][1]["image"] == "https://www.simplyrecipes.com/thmb/KRw_r32s4gQeOX-d07NWY1OlOFk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1c-c2b1885d27d4481c9cfe6f6286a64342.jpg"
    assert recipe["images"][1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 3
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == False

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 3
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe["user_interactions"]["cooked"] == (expected_state if toggle_action == "cooked" else False)
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])

    assert recipe["user_interactions"]["bookmarked"] == (expected_state if toggle_action == "bookmarked" else False)
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])

    assert recipe["user_interactions"]["liked"] == (expected_state if toggle_action == "liked" else False)
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])

    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

def test_post_assoc_by_cooked_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "cooked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe has the cooked action enabled successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["images"][1]["image"] == "https://www.simplyrecipes.com/thmb/KRw_r32s4gQeOX-d07NWY1OlOFk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1c-c2b1885d27d4481c9cfe6f6286a64342.jpg"
    assert recipe["images"][1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 3
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == False

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 3
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["user_interactions"]["cooked"] == True
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])
    assert recipe["user_interactions"]["bookmarked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])
    assert recipe["user_interactions"]["liked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

    get_recipe_by_id(client, token, recipe_id, "cooked", True)

def test_post_assoc_by_cooked_action_with_toggle_original_state(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "cooked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe has the cooked action enabled successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["images"][1]["image"] == "https://www.simplyrecipes.com/thmb/KRw_r32s4gQeOX-d07NWY1OlOFk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1c-c2b1885d27d4481c9cfe6f6286a64342.jpg"
    assert recipe["images"][1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 3
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == False

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 3
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["user_interactions"]["cooked"] == True
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])
    assert recipe["user_interactions"]["bookmarked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])
    assert recipe["user_interactions"]["liked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

    get_recipe_by_id(client, token, recipe_id, "cooked", True)

    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "cooked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe has the cooked action disabled successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["images"][1]["image"] == "https://www.simplyrecipes.com/thmb/KRw_r32s4gQeOX-d07NWY1OlOFk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1c-c2b1885d27d4481c9cfe6f6286a64342.jpg"
    assert recipe["images"][1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 3
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == False

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 3
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["user_interactions"]["cooked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])
    assert recipe["user_interactions"]["bookmarked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])
    assert recipe["user_interactions"]["liked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

    get_recipe_by_id(client, token, recipe_id, "cooked", False)

def test_post_assoc_by_uncooked_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d376337/toggle",
        json={
            "action": "cooked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID 6b86885b-a613-4ca6-a9b7-584c3d376337 as Recipe has the cooked action disabled successfully"
    
    recipe = response.json()["recipe"]

    assert recipe["id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe["name"] == "test"
    assert recipe["serving"] == "1-2"
    assert recipe["cooking_time"] == "45 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe["images"][1]["image"] == "/test_recipe_image"
    assert recipe["images"][1]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 1
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == True

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 2
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"

    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe["user_interactions"]["cooked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])
    assert recipe["user_interactions"]["bookmarked"] == True
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])
    assert recipe["user_interactions"]["liked"] == True
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

    #get_recipe_by_id(client, token,"6b86885b-a613-4ca6-a9b7-584c3d376337", "cooked", False)

def test_post_assoc_by_bookmarked_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "bookmarked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe has the bookmarked action enabled successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["images"][1]["image"] == "https://www.simplyrecipes.com/thmb/KRw_r32s4gQeOX-d07NWY1OlOFk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1c-c2b1885d27d4481c9cfe6f6286a64342.jpg"
    assert recipe["images"][1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 3
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == False

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 3
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["user_interactions"]["cooked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])
    assert recipe["user_interactions"]["bookmarked"] == True
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])
    assert recipe["user_interactions"]["liked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

    get_recipe_by_id(client, token, recipe_id, "bookmarked", True)

def test_post_assoc_by_bookmarked_action_with_toggle_to_original_state(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "bookmarked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe has the bookmarked action enabled successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["images"][1]["image"] == "https://www.simplyrecipes.com/thmb/KRw_r32s4gQeOX-d07NWY1OlOFk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1c-c2b1885d27d4481c9cfe6f6286a64342.jpg"
    assert recipe["images"][1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 3
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == False

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 3
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["user_interactions"]["cooked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])
    assert recipe["user_interactions"]["bookmarked"] == True
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])
    assert recipe["user_interactions"]["liked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

    get_recipe_by_id(client, token, recipe_id, "bookmarked", True)

    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "bookmarked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe has the bookmarked action disabled successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["images"][1]["image"] == "https://www.simplyrecipes.com/thmb/KRw_r32s4gQeOX-d07NWY1OlOFk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1c-c2b1885d27d4481c9cfe6f6286a64342.jpg"
    assert recipe["images"][1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 3
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == False

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 3
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["user_interactions"]["cooked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])
    assert recipe["user_interactions"]["bookmarked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])
    assert recipe["user_interactions"]["liked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

    get_recipe_by_id(client, token, recipe_id, "bookmarked", False)

def test_post_assoc_by_unbookmarked_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d376337/toggle",
        json={
            "action": "bookmarked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID 6b86885b-a613-4ca6-a9b7-584c3d376337 as Recipe has the bookmarked action disabled successfully"
    
    recipe = response.json()["recipe"]

    assert recipe["id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe["name"] == "test"
    assert recipe["serving"] == "1-2"
    assert recipe["cooking_time"] == "45 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe["images"][1]["image"] == "/test_recipe_image"
    assert recipe["images"][1]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 1
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == True

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 2
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"

    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe["user_interactions"]["cooked"] == True
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])
    assert recipe["user_interactions"]["bookmarked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])
    assert recipe["user_interactions"]["liked"] == True
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

def test_post_assoc_by_liked_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "liked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe has the liked action enabled successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["images"][1]["image"] == "https://www.simplyrecipes.com/thmb/KRw_r32s4gQeOX-d07NWY1OlOFk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1c-c2b1885d27d4481c9cfe6f6286a64342.jpg"
    assert recipe["images"][1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 3
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == False

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 3
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["user_interactions"]["cooked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])
    assert recipe["user_interactions"]["bookmarked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])
    assert recipe["user_interactions"]["liked"] == True
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

    get_recipe_by_id(client, token, recipe_id, "liked", True)

def test_post_assoc_by_liked_action_with_toggle_to_original_state(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "liked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe has the liked action enabled successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["images"][1]["image"] == "https://www.simplyrecipes.com/thmb/KRw_r32s4gQeOX-d07NWY1OlOFk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1c-c2b1885d27d4481c9cfe6f6286a64342.jpg"
    assert recipe["images"][1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 3
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == False

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 3
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["user_interactions"]["cooked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])
    assert recipe["user_interactions"]["bookmarked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])
    assert recipe["user_interactions"]["liked"] == True
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

    get_recipe_by_id(client, token, recipe_id, "liked", True)

    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "liked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe has the liked action disabled successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["images"][1]["image"] == "https://www.simplyrecipes.com/thmb/KRw_r32s4gQeOX-d07NWY1OlOFk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1c-c2b1885d27d4481c9cfe6f6286a64342.jpg"
    assert recipe["images"][1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 3
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == False

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 3
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["user_interactions"]["cooked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])
    assert recipe["user_interactions"]["bookmarked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])
    assert recipe["user_interactions"]["liked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

    get_recipe_by_id(client, token, recipe_id, "liked", False)

def test_post_assoc_by_unliked_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d376337/toggle",
        json={
            "action": "liked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID 6b86885b-a613-4ca6-a9b7-584c3d376337 as Recipe has the liked action disabled successfully"
    
    recipe = response.json()["recipe"]

    assert recipe["id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe["name"] == "test"
    assert recipe["serving"] == "1-2"
    assert recipe["cooking_time"] == "45 minutes"

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    
    assert len(recipe["images"]) == 2
    assert recipe["images"][0]["image"] == "/string_test"
    assert recipe["images"][0]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe["images"][1]["image"] == "/test_recipe_image"
    assert recipe["images"][1]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"
    
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 1
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == True

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 2
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert recipe["creator"]["username"] == "testuser"

    assert "updated_date" in recipe
    assert "created_date" in recipe

    assert recipe["user_interactions"]["user_id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert recipe["user_interactions"]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe["user_interactions"]["cooked"] == True
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["cooked_date"])
    assert recipe["user_interactions"]["bookmarked"] == True
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["bookmarked_date"])
    assert recipe["user_interactions"]["liked"] == False
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["liked_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["created_date"])
    DateTimeUtils.assert_is_none_or_datetime(recipe["user_interactions"]["updated_date"])

def test_post_assoc_with_wrong_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "cook"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "action"]
    assert response_json["detail"][0]["msg"] == "Input should be 'liked', 'bookmarked' or 'cooked'"

def test_post_assoc_with_null_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": None
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "action"]
    assert response_json["detail"][0]["msg"] == "Input should be 'liked', 'bookmarked' or 'cooked'"

def test_post_assoc_with_invalid_token(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "cook"
        }, 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_post_assoc_without_token(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/{recipe_id}/toggle",
        json={
            "action": "cook"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_post_assoc_with_wrong_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d376338/toggle",
        json={
            "action": "liked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 6b86885b-a613-4ca6-a9b7-584c3d376338 as Recipe is not found"

def test_post_assoc_with_invalid_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d37633z/toggle",
        json={
            "action": "liked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "recipe_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_assoc_without_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/toggle",
        json={
            "action": "liked"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 405
    assert response.json()["detail"] == f"Method Not Allowed"