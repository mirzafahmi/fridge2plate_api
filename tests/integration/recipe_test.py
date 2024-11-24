from fastapi.testclient import TestClient


url_prefix = "/recipes"

def test_get_recipe_list(client: TestClient):
    response = client.get(f"{url_prefix}")

    assert response.status_code == 200
    assert response.json()["detail"] == "Recipe list is retrieved successfully"

    recipes = response.json()["recipes"]

    assert isinstance(recipes, list)
    assert len(recipes) == 2

    assert recipes[0]["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipes[0]["name"] == "ayam masak lemak cili padi"
    assert recipes[0]["serving"] == "4-5"
    assert recipes[0]["cooking_time"] == "30 minutes"

    assert recipes[0]["steps"][0]["step_number"] == 1
    assert recipes[0]["steps"][0]["description"] == "potong ayam"
    assert recipes[0]["steps"][1]["step_number"] == 2
    assert recipes[0]["steps"][1]["description"] == "potong lobak"
    assert recipes[0]["steps"][2]["step_number"] == 3
    assert recipes[0]["steps"][2]["description"] == "masak"
    
    assert recipes[0]["images"] == []
    assert recipes[0]["recipe_category"]["name"] == "lunch"
    assert recipes[0]["recipe_origin"]["name"] == "malay"
    assert recipes[0]["recipe_tags"][0]["name"] == "beginner"
    assert recipes[0]["recipe_tags"][1]["name"] == "eid"
    
    assert recipes[0]["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipes[0]["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipes[0]["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipes[0]["ingredient_data"][0]["quantity"] == 3
    assert recipes[0]["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipes[0]["ingredient_data"][0]["is_essential"] == False

    assert recipes[0]["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipes[0]["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipes[0]["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipes[0]["ingredient_data"][1]["quantity"] == 3
    assert recipes[0]["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipes[0]["ingredient_data"][1]["is_essential"] == True

    assert recipes[0]["creator"]["username"] == "testuser"

    assert "updated_date" in recipes[0]
    assert "created_date" in recipes[0]


    assert recipes[1]["id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipes[1]["name"] == "test"
    assert recipes[1]["serving"] == "1-2"
    assert recipes[1]["cooking_time"] == "45 minutes"

    assert recipes[1]["steps"][0]["step_number"] == 1
    assert recipes[1]["steps"][0]["description"] == "potong ayam"
    assert recipes[1]["steps"][1]["step_number"] == 2
    assert recipes[1]["steps"][1]["description"] == "potong lobak"
    
    assert recipes[1]["images"] == []
    assert recipes[1]["recipe_category"]["name"] == "lunch"
    assert recipes[1]["recipe_origin"]["name"] == "malay"
    assert recipes[1]["recipe_tags"][0]["name"] == "beginner"
    assert recipes[1]["recipe_tags"][1]["name"] == "eid"
    
    assert recipes[1]["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipes[1]["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipes[1]["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipes[1]["ingredient_data"][0]["quantity"] == 1
    assert recipes[1]["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipes[1]["ingredient_data"][0]["is_essential"] == True

    assert recipes[1]["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipes[1]["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipes[1]["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipes[1]["ingredient_data"][1]["quantity"] == 2
    assert recipes[1]["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipes[1]["ingredient_data"][1]["is_essential"] == True

    assert recipes[1]["creator"]["username"] == "testuser"

    assert "updated_date" in recipes[1]
    assert "created_date" in recipes[1]

def test_get_recipe_list_lite(client: TestClient):
    response = client.get(f"{url_prefix}/lite")

    assert response.status_code == 200
    assert response.json()["detail"] == "Recipe list Lite is retrieved successfully"

    recipes = response.json()["recipes"]

    assert isinstance(recipes, list)
    assert len(recipes) == 2

    assert recipes[0]["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipes[0]["name"] == "ayam masak lemak cili padi"
    assert recipes[0]["serving"] == "4-5"
    assert recipes[0]["cooking_time"] == "30 minutes"

    assert recipes[0]["steps"][0]["step_number"] == 1
    assert recipes[0]["steps"][0]["description"] == "potong ayam"
    assert recipes[0]["steps"][1]["step_number"] == 2
    assert recipes[0]["steps"][1]["description"] == "potong lobak"
    assert recipes[0]["steps"][2]["step_number"] == 3
    assert recipes[0]["steps"][2]["description"] == "masak"
    
    assert recipes[0]["images"] == []
    assert recipes[0]["recipe_category"]["name"] == "lunch"
    assert recipes[0]["recipe_origin"]["name"] == "malay"
    assert recipes[0]["recipe_tags"][0]["name"] == "beginner"
    assert recipes[0]["recipe_tags"][1]["name"] == "eid"
    
    assert recipes[0]["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipes[0]["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipes[0]["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipes[0]["ingredient_data"][0]["quantity"] == 3
    assert recipes[0]["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipes[0]["ingredient_data"][0]["is_essential"] == False

    assert recipes[0]["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipes[0]["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipes[0]["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipes[0]["ingredient_data"][1]["quantity"] == 3
    assert recipes[0]["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipes[0]["ingredient_data"][1]["is_essential"] == True

    assert recipes[0]["creator"]["username"] == "testuser"

    assert "updated_date" in recipes[0]
    assert "created_date" in recipes[0]


    assert recipes[1]["id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipes[1]["name"] == "test"
    assert recipes[1]["serving"] == "1-2"
    assert recipes[1]["cooking_time"] == "45 minutes"

    assert recipes[1]["steps"][0]["step_number"] == 1
    assert recipes[1]["steps"][0]["description"] == "potong ayam"
    assert recipes[1]["steps"][1]["step_number"] == 2
    assert recipes[1]["steps"][1]["description"] == "potong lobak"
    
    assert recipes[1]["images"] == []
    assert recipes[1]["recipe_category"]["name"] == "lunch"
    assert recipes[1]["recipe_origin"]["name"] == "malay"
    assert recipes[1]["recipe_tags"][0]["name"] == "beginner"
    assert recipes[1]["recipe_tags"][1]["name"] == "eid"
    
    assert recipes[1]["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipes[1]["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipes[1]["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipes[1]["ingredient_data"][0]["quantity"] == 1
    assert recipes[1]["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipes[1]["ingredient_data"][0]["is_essential"] == True

    assert recipes[1]["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipes[1]["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipes[1]["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipes[1]["ingredient_data"][1]["quantity"] == 2
    assert recipes[1]["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipes[1]["ingredient_data"][1]["is_essential"] == True

    assert recipes[1]["creator"]["username"] == "testuser"

    assert "updated_date" in recipes[1]
    assert "created_date" in recipes[1]

def test_get_recipe_by_id(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.get(f"{url_prefix}/{recipe_id}")

    assert response.status_code == 200
    assert response.json()["detail"] == f"Id {recipe_id} as Recipe is retrieved successfully"
    
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
    
    assert recipe["images"] == []
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

def test_get_recipe_by_id_lite(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.get(f"{url_prefix}/{recipe_id}/lite")

    assert response.status_code == 200
    assert response.json()["detail"] == f"Id {recipe_id} as Recipe Lite is retrieved successfully"
    
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
    
    assert recipe["images"] == []
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


def test_post_recipe(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "Test recipe",
            "serving": "1-3",
            "cooking_time": "35 minutes",
            "recipe_category_id": "4053a7e8-9ae5-415d-9bed-e4d0a235f481",
            "recipe_origin_id": "92e80174-c259-480a-80b5-f5b0d32ca005",
            "recipe_tags": [
                "8c935f60-2f3a-410a-9860-09bb2c270a38",
                "13444244-43b2-4d63-a080-604dd5088452"
            ],
            "ingredients": [
                {
                "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84",
                "quantity": 1,
                "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
                "is_essential": True
                },
                {
                "ingredient_id": "b3cceb34-9465-4020-9066-f7b5ce3c372c",
                "quantity": 7,
                "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
                "is_essential": True
                }
            ],
            "steps": [
                {
                "step_number": 1,
                "description": "wash chicken"
                },
                {
                "step_number": 2,
                "description": "eat chicken"
                }
            ],
            "images": [
                {
                "image": "/string"
                }
            ],
            "created_by": "0c619092-817e-4f73-b25f-8e187e69dded"
        }
    )

    assert response.status_code == 201
    assert response.json()["detail"] == "test recipe as Recipe is successfully created"

    recipe = response.json()["recipe"]

    assert recipe["name"] == "test recipe"
    assert recipe["serving"] == "1-3"
    assert recipe["cooking_time"] == "35 minutes"

    assert recipe["recipe_category"]["name"] == "breakfast"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"
    assert recipe["recipe_tags"][1]["name"] == "eid"

    assert len(recipe["ingredient_data"]) == 2
    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "carrot"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert recipe["ingredient_data"][0]["quantity"] == 7
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == True

    assert recipe["ingredient_data"][1]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][1]["quantity"] == 1
    assert recipe["ingredient_data"][1]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][1]["is_essential"] == True

    assert len(recipe["steps"]) == 2
    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "wash chicken"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "eat chicken"
    
    assert len(recipe["images"]) == 1
    assert recipe["images"][0]["image"] == "/string"
    
    assert recipe["creator"]["username"] == "second_user"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

def test_get_recipe_by_id_with_wrong_id(client: TestClient):
    recipe_id = "b4b165f6-a4f2-45f6-bda6-0a49092d3f01"
    response = client.get(f"{url_prefix}/{recipe_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Id b4b165f6-a4f2-45f6-bda6-0a49092d3f01 as Recipe is not found"

def test_get_recipe_by_id_with_wrong_id_lite(client: TestClient):
    recipe_id = "b4b165f6-a4f2-45f6-bda6-0a49092d3f01"
    response = client.get(f"{url_prefix}/{recipe_id}/lite")

    assert response.status_code == 404
    assert response.json()["detail"] == "Id b4b165f6-a4f2-45f6-bda6-0a49092d3f01 as Recipe is not found"

def test_delete_recipe(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.delete(f"{url_prefix}/{recipe_id}")

    assert response.status_code == 200
    assert response.json()["detail"] == "Id 2cdd1a37-9c45-4202-a38c-026686b0ff71 as Recipe is successfully deleted"

    ingredient_recipe_association_response = client.get(f"/ingredient_recipe_association/by_recipe_id/{recipe_id}")

    assert ingredient_recipe_association_response.status_code == 404
    assert ingredient_recipe_association_response.json()["detail"] == "Ingredient recipe association list for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of recipe is empty"

    recipe_tag_recipe_association_response = client.get(f"/recipe_tag_recipe_association/by_recipe_id/{recipe_id}")

    assert recipe_tag_recipe_association_response.status_code == 404
    assert recipe_tag_recipe_association_response.json()["detail"] == "Recipe tag recipe association list for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of recipe is empty"

    instruction_response = client.get(f"/instruction/by_recipe_id/{recipe_id}")

    assert instruction_response.status_code == 404
    assert instruction_response.json()["detail"] == "Instruction list for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of recipe is empty"

    recipe_image_response = client.get(f"/recipe_image/by_recipe_id/{recipe_id}")

    assert recipe_image_response.status_code == 404
    assert recipe_image_response.json()["detail"] == "Recipe image list for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of recipe is empty"


def test_delete_recipe_with_wrong_id(client: TestClient):
    response = client.delete(f"{url_prefix}/db67b3f4-0e04-47bb-bc46-94826847ee4f")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Id db67b3f4-0e04-47bb-bc46-94826847ee4f as Recipe is not found"