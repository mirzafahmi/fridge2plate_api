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
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe Lite is retrieved successfully"
    
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

def test_get_recipe_by_id_with_wrong_id(client: TestClient):
    recipe_id = "b4b165f6-a4f2-45f6-bda6-0a49092d3f01"
    response = client.get(f"{url_prefix}/{recipe_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "ID b4b165f6-a4f2-45f6-bda6-0a49092d3f01 as Recipe is not found"

def test_get_recipe_by_id_with_wrong_id_lite(client: TestClient):
    recipe_id = "b4b165f6-a4f2-45f6-bda6-0a49092d3f01"
    response = client.get(f"{url_prefix}/{recipe_id}/lite")

    assert response.status_code == 404
    assert response.json()["detail"] == "ID b4b165f6-a4f2-45f6-bda6-0a49092d3f01 as Recipe is not found"

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
    assert response.json()["detail"] == "test recipe as Recipe is created successfully"

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

def test_post_recipe_with_empty_name(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_recipe_without_name(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_with_wrong_serving_format(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "5-a",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "serving"]
    assert response_json["detail"][0]["msg"] == 'Value error, Serving must be a number or a valid range (e.g., "1-3")'

def test_post_recipe_with_empty_serving(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "serving"]
    assert response_json["detail"][0]["msg"] == "String should have at least 1 character"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_recipe_without_serving(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "serving"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_with_wrong_cooking_time_format(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-2",
            "cooking_time": "35 minu",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "cooking_time"]
    assert response_json["detail"][0]["msg"] == 'Value error, Cooking time must be in the format "X minute(s)" or "X hour(s)", where X is a number and "minute(s)" or "hour(s)" is the unit.'

def test_post_recipe_with_empty_cooking_time(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-2",
            "cooking_time": "",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "cooking_time"]
    assert response_json["detail"][0]["msg"] == "String should have at least 1 character"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_recipe_without_cooking_time(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-2",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "cooking_time"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_with_wrong_recipe_category_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-2",
            "cooking_time": "35 minutes",
            "recipe_category_id": "4053a7e8-9ae5-415d-9bed-e4d0a235f482",
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

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 4053a7e8-9ae5-415d-9bed-e4d0a235f482 as Recipe Category is not found"

def test_post_recipe_with_invalid_recipe_category_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-2",
            "cooking_time": "35 minutes",
            "recipe_category_id": "4053a7e8-9ae5-415d-9bed-e4d0a235f48z",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "recipe_category_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_with_empty_recipe_category_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-2",
            "cooking_time": "35 minutes",
            "recipe_category_id": "",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "recipe_category_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_without_recipe_category_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-2",
            "cooking_time": "35 minutes",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "recipe_category_id"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_with_wrong_recipe_origin_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-2",
            "cooking_time": "35 minutes",
            "recipe_category_id": "4053a7e8-9ae5-415d-9bed-e4d0a235f481",
            "recipe_origin_id": "92e80174-c259-480a-80b5-f5b0d32ca006",
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

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 92e80174-c259-480a-80b5-f5b0d32ca006 as Recipe Origin is not found"

def test_post_recipe_with_invalid_recipe_origin_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-2",
            "cooking_time": "35 minutes",
            "recipe_category_id": "4053a7e8-9ae5-415d-9bed-e4d0a235f481",
            "recipe_origin_id": "92e80174-c259-480a-80b5-f5b0d32ca00z",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "recipe_origin_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_with_empty_recipe_origin_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-2",
            "cooking_time": "35 minutes",
            "recipe_category_id": "4053a7e8-9ae5-415d-9bed-e4d0a235f481",
            "recipe_origin_id": "",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "recipe_origin_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_without_recipe_origin_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-2",
            "cooking_time": "35 minutes",
            "recipe_category_id": "4053a7e8-9ae5-415d-9bed-e4d0a235f481",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "recipe_origin_id"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_with_wrong_recipe_tags(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-3",
            "cooking_time": "35 minutes",
            "recipe_category_id": "4053a7e8-9ae5-415d-9bed-e4d0a235f481",
            "recipe_origin_id": "92e80174-c259-480a-80b5-f5b0d32ca005",
            "recipe_tags": [
                "8c935f60-2f3a-410a-9860-09bb2c270a38",
                "13444244-43b2-4d63-a080-604dd5088453"
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

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 13444244-43b2-4d63-a080-604dd5088453 as Recipe Tag is not found"

def test_post_recipe_with_invalid_recipe_tags(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-3",
            "cooking_time": "35 minutes",
            "recipe_category_id": "4053a7e8-9ae5-415d-9bed-e4d0a235f481",
            "recipe_origin_id": "92e80174-c259-480a-80b5-f5b0d32ca005",
            "recipe_tags": [
                "8c935f60-2f3a-410a-9860-09bb2c270a38",
                "13444244-43b2-4d63-a080-604dd508845z"
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", 'recipe_tags', 1]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_with_empty_recipe_tags(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-3",
            "cooking_time": "35 minutes",
            "recipe_category_id": "4053a7e8-9ae5-415d-9bed-e4d0a235f481",
            "recipe_origin_id": "92e80174-c259-480a-80b5-f5b0d32ca005",
            "recipe_tags": [],
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", 'recipe_tags']
    assert response_json["detail"][0]["msg"] == "Value error, At least one recipe tag (UUID) is required."

def test_post_recipe_without_recipe_tags(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
            "serving": "1-3",
            "cooking_time": "35 minutes",
            "recipe_category_id": "4053a7e8-9ae5-415d-9bed-e4d0a235f481",
            "recipe_origin_id": "92e80174-c259-480a-80b5-f5b0d32ca005",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "recipe_tags"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_with_wrong_ingredient_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
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
                "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea85",
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

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 423f2e0f-d5cc-48dc-8b06-e987a3d8ea85 as Ingredient is not found"

def test_post_recipe_with_invalid_ingredient_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
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
                "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea8z",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredients", 0, "ingredient_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_with_empty_ingredient_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
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
                "ingredient_id": "",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredients", 0, "ingredient_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_without_ingredient_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredients", 0, "ingredient_id"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_with_invalid_ingredient_quantity(client: TestClient):
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
                "quantity": -123,
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredients", 0, "quantity"]
    assert response_json["detail"][0]["msg"] == "Input should be greater than 0"

def test_post_recipe_with_not_integer_ingredient_quantity(client: TestClient):
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
                "quantity": "",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "ingredients", 0, "quantity"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid number, unable to parse string as a number"

def test_post_recipe_without_ingredient_quantity(client: TestClient):
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

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredients", 0, "quantity"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_with_wrong_uom_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
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
                "uom_id": "13444244-43b2-4d63-a080-604dd5088453",
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
    
    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 13444244-43b2-4d63-a080-604dd5088453 as UOM is not found"

def test_post_recipe_with_invalid_uom_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
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
                "uom_id": "13444244-43b2-4d63-a080-604dd508845z",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "ingredients", 0, "uom_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_with_empty_uom_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
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
                "uom_id": "",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredients", 0, "uom_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_without_uom_id(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredients", 0, "uom_id"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_with_non_boolean_is_essential(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
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
                "is_essential": "-true"
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredients", 0, "is_essential"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid boolean, unable to interpret input"
    assert response_json["detail"][0]["type"] == "bool_parsing"

def test_post_recipe_with_empty_is_essential(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
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
                "is_essential": ""
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
    
    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredients", 0, "is_essential"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid boolean, unable to interpret input"
    assert response_json["detail"][0]["type"] == "bool_parsing"

def test_post_recipe_without_is_essential(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "test recipe",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredients", 0, "is_essential"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_with_wrong_step_number(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "recipe name",
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
                "step_number": -1,
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "steps", 0, "step_number"]
    assert response_json["detail"][0]["msg"] == "Value error, step_number must be a positive integer"

def test_post_recipe_with_non_integer_step_number(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "recipe name",
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
                "step_number": "asd",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "steps", 0, "step_number"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"
    assert response_json["detail"][0]["type"] == "int_parsing"

def test_post_recipe_with_empty_step_description(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "recipe name",
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
                "description": ""
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "steps", 0, "description"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_recipe_without_step_description(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "recipe name",
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

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "steps", 0, "description"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_with_empty_steps(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "recipe name",
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
            "steps": [],
            "images": [
                {
                "image": "/string"
                }
            ],
            "created_by": "0c619092-817e-4f73-b25f-8e187e69dded"
        }
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "steps"]
    assert response_json["detail"][0]["msg"] == "Value error, Steps cannot be an empty list."
    assert response_json["detail"][0]["type"] == "value_error"

def test_post_recipe_without_steps(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "recipe name",
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
            "images": [
                {
                "image": "/string"
                }
            ],
            "created_by": "0c619092-817e-4f73-b25f-8e187e69dded"
        }
    )

    assert response.status_code == 422

    response_json = response.json()
    
    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "steps"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

#TODO! images test?
def test_post_recipe_with_wrong_created_by(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "recipe name",
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
            "created_by": "0c619092-817e-4f73-b25f-8e187e69ddee"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 0c619092-817e-4f73-b25f-8e187e69ddee as User is not found"

def test_post_recipe_with_invalid_created_by(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "recipe name",
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
            "created_by": "0c619092-817e-4f73-b25f-8e187e69ddez"
        }
    )

    assert response.status_code == 422

    response_json = response.json()
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_with_empty_created_by(client: TestClient):
    response = client.post(f"{url_prefix}",
        json={
            "name": "recipe name",
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
            "created_by": ""
        }
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_recipe_by_changing_name(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.put(f"{url_prefix}/{recipe_id}",
        json={
            "name": "updated reCIpe Name"
        }
    )
    
    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe is updated successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["name"] == "updated recipe name"
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

def test_put_recipe_by_changing_serving(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.put(f"{url_prefix}/{recipe_id}",
        json={
            "serving": "2-3"
        }
    )
    
    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe is updated successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["serving"] == "2-3"
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

def test_put_recipe_by_changing_cooking_time(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.put(f"{url_prefix}/{recipe_id}",
        json={
            "cooking_time": "27 minutes"
        }
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe is updated successfully"
    
    recipe = response.json()["recipe"]
    
    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "27 minutes"

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

def test_put_recipe_by_changing_cooking_time(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.put(f"{url_prefix}/{recipe_id}",
        json={
            "cooking_time": "27 minutes"
        }
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe is updated successfully"
    
    recipe = response.json()["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "27 minutes"

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

def test_put_recipe_by_changing_recipe_category_id(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.put(f"{url_prefix}/{recipe_id}",
        json={
            "recipe_category_id": "4053a7e8-9ae5-415d-9bed-e4d0a235f481"
        }
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe is updated successfully"
    
    recipe = response.json()["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["recipe_category"]["name"] == "breakfast"
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

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert recipe["images"] == []

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

def test_put_recipe_by_changing_recipe_origin_id(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.put(f"{url_prefix}/{recipe_id}",
        json={
            "recipe_origin_id": "c7048030-10ff-486c-9e78-7417212dd728"
        }
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe is updated successfully"
    
    recipe = response.json()["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "italian"
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

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert recipe["images"] == []

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

def test_put_recipe_by_changing_recipe_tags(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.put(f"{url_prefix}/{recipe_id}",
        json={
            "recipe_tags": ["13444244-43b2-4d63-a080-604dd5088452"]
        }
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe is updated successfully"
    
    recipe = response.json()["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"

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

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert recipe["images"] == []

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

def test_put_recipe_by_changing_ingredients(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.put(f"{url_prefix}/{recipe_id}",
        json={
            "ingredients": [
                {
                "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84",
                "quantity": 11,
                "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
                "is_essential": False
                },
            ]
        }
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe is updated successfully"
    
    recipe = response.json()["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"

    assert recipe["ingredient_data"][0]["ingredient"]["name"] == "chicken"
    assert recipe["ingredient_data"][0]["ingredient"]["brand"] == "chicken"
    assert recipe["ingredient_data"][0]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert recipe["ingredient_data"][0]["quantity"] == 11
    assert recipe["ingredient_data"][0]["uom"]["name"] == "piece"
    assert recipe["ingredient_data"][0]["is_essential"] == False

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert recipe["images"] == []

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

def test_put_recipe_by_changing_steps(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.put(f"{url_prefix}/{recipe_id}",
        json={
            "steps": [
                {
                    "step_number": 1,
                    "description": "test Steps"
                }
            ]
        }
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe is updated successfully"
    
    recipe = response.json()["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"

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

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "test steps"
    
    assert recipe["images"] == []

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

#TODO! convert images as list of str not as list of recipeimage obj
def test_put_recipe_by_changing_images(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.put(f"{url_prefix}/{recipe_id}",
        json={
            "images": [
                {
                    "image": "/test_url"
                },
                {
                    "image": "/image_url"
                },
            ]
        }
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe is updated successfully"
    
    recipe = response.json()["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"

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

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert recipe["images"][0]["image"] == "/image_url"
    assert recipe["images"][1]["image"] == "/test_url"

    assert recipe["creator"]["username"] == "testuser"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

def test_put_recipe_by_changing_created_by(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.put(f"{url_prefix}/{recipe_id}",
        json={
            "created_by": "0c619092-817e-4f73-b25f-8e187e69dded"
        }
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_id} as Recipe is updated successfully"
    
    recipe = response.json()["recipe"]

    assert recipe["id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe["name"] == "ayam masak lemak cili padi"
    assert recipe["serving"] == "4-5"
    assert recipe["cooking_time"] == "30 minutes"

    assert recipe["recipe_category"]["name"] == "lunch"
    assert recipe["recipe_origin"]["name"] == "malay"
    assert recipe["recipe_tags"][0]["name"] == "beginner"

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

    assert recipe["steps"][0]["step_number"] == 1
    assert recipe["steps"][0]["description"] == "potong ayam"
    assert recipe["steps"][1]["step_number"] == 2
    assert recipe["steps"][1]["description"] == "potong lobak"
    assert recipe["steps"][2]["step_number"] == 3
    assert recipe["steps"][2]["description"] == "masak"
    
    assert recipe["images"] == []

    assert recipe["creator"]["username"] == "second_user"
    
    assert "updated_date" in recipe
    assert "created_date" in recipe

def test_delete_recipe(client: TestClient):
    recipe_id = "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    response = client.delete(f"{url_prefix}/{recipe_id}")

    assert response.status_code == 200
    assert response.json()["detail"] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 as Recipe is deleted successfully"

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
    assert response.json()["detail"] == "ID db67b3f4-0e04-47bb-bc46-94826847ee4f as Recipe is not found"