from fastapi.testclient import TestClient


url_prefix = '/ingredient_recipe_association'

def test_get_ingredient_recipe_association_list(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Ingredient Recipe Association list is retrieved successfully"

    ingredient_recipe_associations = response.json()['ingredient_recipe_associations']

    assert isinstance(ingredient_recipe_associations, list)
    assert len(ingredient_recipe_associations) == 4

    assert ingredient_recipe_associations[0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert ingredient_recipe_associations[0]["ingredient"]["name"] == "carrot"
    assert ingredient_recipe_associations[0]["ingredient"]["brand"] == "carrot"
    assert ingredient_recipe_associations[0]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert ingredient_recipe_associations[0]["quantity"] == 3
    assert ingredient_recipe_associations[0]["uom"]["name"] == "piece"
    assert ingredient_recipe_associations[0]["is_essential"] == False

    assert ingredient_recipe_associations[1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert ingredient_recipe_associations[1]["ingredient"]["name"] == "chicken"
    assert ingredient_recipe_associations[1]["ingredient"]["brand"] == "chicken"
    assert ingredient_recipe_associations[1]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert ingredient_recipe_associations[1]["quantity"] == 3
    assert ingredient_recipe_associations[1]["uom"]["name"] == "piece"
    assert ingredient_recipe_associations[1]["is_essential"] == True

    assert ingredient_recipe_associations[2]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert ingredient_recipe_associations[2]["ingredient"]["name"] == "carrot"
    assert ingredient_recipe_associations[2]["ingredient"]["brand"] == "carrot"
    assert ingredient_recipe_associations[2]["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert ingredient_recipe_associations[2]["quantity"] == 1
    assert ingredient_recipe_associations[2]["uom"]["name"] == "piece"
    assert ingredient_recipe_associations[2]["is_essential"] ==True

    assert ingredient_recipe_associations[3]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert ingredient_recipe_associations[3]["ingredient"]["name"] == "chicken"
    assert ingredient_recipe_associations[3]["ingredient"]["brand"] == "chicken"
    assert ingredient_recipe_associations[3]["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert ingredient_recipe_associations[3]["quantity"] == 2
    assert ingredient_recipe_associations[3]["uom"]["name"] == "piece"
    assert ingredient_recipe_associations[3]["is_essential"] == True

def test_get_ingredient_recipe_association_by_id(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.get(f"{url_prefix}/{ingredient_recipe_association_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {ingredient_recipe_association_id} as Ingredient Recipe Association is retrieved successfully"

    ingredient_recipe_association = response.json()["ingredient_recipe_association"]
    
    assert ingredient_recipe_association["id"] == ingredient_recipe_association_id
    assert ingredient_recipe_association["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert ingredient_recipe_association["ingredient"]["name"] == "carrot"
    assert ingredient_recipe_association["ingredient"]["brand"] == "carrot"
    assert ingredient_recipe_association["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert ingredient_recipe_association["quantity"] == 3
    assert ingredient_recipe_association["uom"]["name"] == "piece"
    assert ingredient_recipe_association["is_essential"] == False

def test_get_ingredient_recipe_association_by_wrong_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 as Ingredient Recipe Association is not found"

def test_post_ingredient_recipe_association(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "c282fc9e-dfbd-46ff-8ee0-87463c63a51e",
            "quantity": 2,
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["detail"] == f"ID c282fc9e-dfbd-46ff-8ee0-87463c63a51e of Ingredient as Ingredient Recipe Association is created successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    ingredient_recipe_association = response.json()["ingredient_recipe_association"]

    assert ingredient_recipe_association["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert ingredient_recipe_association["ingredient"]["name"] == "fish"
    assert ingredient_recipe_association["ingredient"]["brand"] == "fish"
    assert ingredient_recipe_association["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert ingredient_recipe_association["quantity"] == 2
    assert ingredient_recipe_association["uom"]["name"] == "piece"
    assert ingredient_recipe_association["is_essential"] == False

    ingredient_recipe_associations_by_recipe_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()

    assert len(ingredient_recipe_associations_by_recipe_id["ingredient_recipe_associations"]) == 3

def test_post_ingredient_recipe_association_with_duplicate_ingredient_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84",
            "quantity": 2,
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "ID 423f2e0f-d5cc-48dc-8b06-e987a3d8ea84 of Ingredient as Ingredient Recipe Association is already registered"

def test_post_ingredient_recipe_association_with_wrong_ingredient_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "13444244-43b2-4d63-a080-604dd5088452",
            "quantity": 2,
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ID 13444244-43b2-4d63-a080-604dd5088452 as Ingredient is not found"

def test_post_ingredient_recipe_association_with_invalid_ingredient_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "13444244-43b2-4d63-a080-604dd508845z",
            "quantity": 2,
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "ingredient_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_ingredient_recipe_association_with_empty_ingredient_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "",
            "quantity": 2,
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "ingredient_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_ingredient_recipe_association_without_ingredient_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "quantity": 2,
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredient_id"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_ingredient_recipe_association_with_invalid_quantity(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84",
            "quantity": -2,
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "quantity"]
    assert response_json["detail"][0]["msg"] == "Input should be greater than 0"

def test_post_ingredient_recipe_association_with_not_integer_quantity(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84",
            "quantity": "",
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "quantity"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid number, unable to parse string as a number"

def test_post_ingredient_recipe_association_without_quantity(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84",
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "quantity"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_ingredient_recipe_association_with_wrong_uom_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "c282fc9e-dfbd-46ff-8ee0-87463c63a51e",
            "quantity": 2,
            "uom_id": "13444244-43b2-4d63-a080-604dd5088453",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ID 13444244-43b2-4d63-a080-604dd5088453 as UOM is not found"

def test_post_ingredient_recipe_association_with_invalid_uom_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84",
            "quantity": 2,
            "uom_id": "13444244-43b2-4d63-a080-604dd508845z",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "uom_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_ingredient_recipe_association_with_empty_uom_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84",
            "quantity": 2,
            "uom_id": "",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "uom_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_ingredient_recipe_association_without_uom_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea84",
            "quantity": 2,
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "uom_id"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_ingredient_recipe_association_with_wrong_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "c282fc9e-dfbd-46ff-8ee0-87463c63a51e",
            "quantity": 2,
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff72"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 2cdd1a37-9c45-4202-a38c-026686b0ff72 as Recipe is not found"

def test_post_ingredient_recipe_association_with_invalid_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "c282fc9e-dfbd-46ff-8ee0-87463c63a51e",
            "quantity": 2,
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff7z"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "recipe_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_ingredient_recipe_association_with_empty_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "c282fc9e-dfbd-46ff-8ee0-87463c63a51e",
            "quantity": 2,
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
            "recipe_id": ""
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "recipe_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_ingredient_recipe_association_without_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "ingredient_id": "c282fc9e-dfbd-46ff-8ee0-87463c63a51e",
            "quantity": 2,
            "uom_id": "13444244-43b2-4d63-a080-604dd5088452",
            "is_essential": False,
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "recipe_id"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_put_ingredient_recipe_association_by_multiple_field(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "ingredient_id": "b3cceb34-9465-4020-9066-f7b5ce3c372c",
            "quantity": 7,
            "uom_id": "8c935f60-2f3a-410a-9860-09bb2c270a38",
            "is_essential": True,
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 202
    assert response.json()["detail"] == f"ID b3cceb34-9465-4020-9066-f7b5ce3c372c of Ingredient as Ingredient Recipe Association is updated successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    ingredient_recipe_association = response.json()["ingredient_recipe_association"]

    assert ingredient_recipe_association["id"] == ingredient_recipe_association_id
    assert ingredient_recipe_association["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert ingredient_recipe_association["ingredient"]["name"] == "carrot"
    assert ingredient_recipe_association["ingredient"]["brand"] == "carrot"
    assert ingredient_recipe_association["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert ingredient_recipe_association["quantity"] == 7
    assert ingredient_recipe_association["uom"]["name"] == "clove"
    assert ingredient_recipe_association["is_essential"] == True

def test_put_ingredient_recipe_association_with_wrong_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/b3cceb34-9465-4020-9066-f7b5ce3c372c", 
        json={
            "ingredient_id": "b3cceb34-9465-4020-9066-f7b5ce3c372c",
            "quantity": 7,
            "uom_id": "8c935f60-2f3a-410a-9860-09bb2c270a38",
            "is_essential": True,
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID b3cceb34-9465-4020-9066-f7b5ce3c372c as Ingredient Recipe Association is not found"

def test_put_ingredient_recipe_association_with_invalid_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/b3cceb34-9465-4020-9066-f7b5ce3c372z", 
        json={
            "ingredient_id": "b3cceb34-9465-4020-9066-f7b5ce3c372c",
            "quantity": 7,
            "uom_id": "8c935f60-2f3a-410a-9860-09bb2c270a38",
            "is_essential": True,
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "ingredient_recipe_association_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_ingredient_recipe_association_without_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/", 
        json={
            "ingredient_id": "b3cceb34-9465-4020-9066-f7b5ce3c372c",
            "quantity": 7,
            "uom_id": "8c935f60-2f3a-410a-9860-09bb2c270a38",
            "is_essential": True,
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 405
    assert response.json()["detail"] == f"Method Not Allowed"

def test_put_ingredient_recipe_association_by_changing_ingredient_id(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "ingredient_id": "c282fc9e-dfbd-46ff-8ee0-87463c63a51e",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID c282fc9e-dfbd-46ff-8ee0-87463c63a51e of Ingredient as Ingredient Recipe Association is updated successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    ingredient_recipe_association = response.json()["ingredient_recipe_association"]
    
    assert ingredient_recipe_association["id"] == ingredient_recipe_association_id
    assert ingredient_recipe_association["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert ingredient_recipe_association["ingredient"]["name"] == "fish"
    assert ingredient_recipe_association["ingredient"]["brand"] == "fish"
    assert ingredient_recipe_association["ingredient"]["ingredient_category"]["name"] == "proteins"
    assert ingredient_recipe_association["quantity"] == 3
    assert ingredient_recipe_association["uom"]["name"] == "piece"
    assert ingredient_recipe_association["is_essential"] == False

def test_put_ingredient_recipe_association_with_wrong_ingredient_id(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea83",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 423f2e0f-d5cc-48dc-8b06-e987a3d8ea83 as Ingredient is not found"

def test_put_ingredient_recipe_association_with_invalid_ingredient_id(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "ingredient_id": "423f2e0f-d5cc-48dc-8b06-e987a3d8ea8z",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "ingredient_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_ingredient_recipe_association_with_empty_ingredient_id(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "ingredient_id": "",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "ingredient_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_ingredient_recipe_association_with_changing_quantity(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "quantity": 25,
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    ingredient_recipe_association = response.json()["ingredient_recipe_association"]
    
    assert ingredient_recipe_association["id"] == ingredient_recipe_association_id
    assert ingredient_recipe_association["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert ingredient_recipe_association["ingredient"]["name"] == "carrot"
    assert ingredient_recipe_association["ingredient"]["brand"] == "carrot"
    assert ingredient_recipe_association["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert ingredient_recipe_association["quantity"] == 25
    assert ingredient_recipe_association["uom"]["name"] == "piece"
    assert ingredient_recipe_association["is_essential"] == False

def test_put_ingredient_recipe_association_with_non_integer_quantity(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "quantity": -25,
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "quantity"]
    assert response_json["detail"][0]["msg"] == "Input should be greater than 0"

def test_put_ingredient_recipe_association_with_empty_quantity(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "quantity": "",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "quantity"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid number, unable to parse string as a number"

def test_put_ingredient_recipe_association_by_changing_uom_id(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "uom_id": "8c935f60-2f3a-410a-9860-09bb2c270a38",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    ingredient_recipe_association = response.json()["ingredient_recipe_association"]
    
    assert ingredient_recipe_association["id"] == ingredient_recipe_association_id
    assert ingredient_recipe_association["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert ingredient_recipe_association["ingredient"]["name"] == "carrot"
    assert ingredient_recipe_association["ingredient"]["brand"] == "carrot"
    assert ingredient_recipe_association["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert ingredient_recipe_association["quantity"] == 3
    assert ingredient_recipe_association["uom"]["name"] == "clove"
    assert ingredient_recipe_association["is_essential"] == False

def test_put_ingredient_recipe_association_with_wrong_uom_id(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "uom_id": "8c935f60-2f3a-410a-9860-09bb2c270a39",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 8c935f60-2f3a-410a-9860-09bb2c270a39 as UOM is not found"

def test_put_ingredient_recipe_association_with_invalid_uom_id(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "uom_id": "8c935f60-2f3a-410a-9860-09bb2c270a3z",
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 422
    
    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "uom_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_ingredient_recipe_association_with_empty_uom_id(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "uom_id": "",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "uom_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_ingredient_recipe_association_by_changing_is_essential(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "is_essential": True,
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    ingredient_recipe_association = response.json()["ingredient_recipe_association"]
    
    assert ingredient_recipe_association["id"] == ingredient_recipe_association_id
    assert ingredient_recipe_association["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert ingredient_recipe_association["ingredient"]["name"] == "carrot"
    assert ingredient_recipe_association["ingredient"]["brand"] == "carrot"
    assert ingredient_recipe_association["ingredient"]["ingredient_category"]["name"] == "vegetables"
    assert ingredient_recipe_association["quantity"] == 3
    assert ingredient_recipe_association["uom"]["name"] == "piece"
    assert ingredient_recipe_association["is_essential"] == True

def test_put_ingredient_recipe_association_with_non_boolean_is_essential(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "is_essential": "asd",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "is_essential"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid boolean, unable to interpret input"
    assert response_json["detail"][0]["type"] == "bool_parsing"

def test_put_ingredient_recipe_association_with_empty_is_essential(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={
            "is_essential": "",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "is_essential"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid boolean, unable to interpret input"
    assert response_json["detail"][0]["type"] == "bool_parsing"

def test_put_ingredient_recipe_association_with_empty_data(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.put(f"{url_prefix}/{ingredient_recipe_association_id}", 
        json={},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Request body must include at least one field to update"

def test_delete_ingredient_recipe_association(client: TestClient, token: str):
    ingredient_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["ingredient_recipe_associations"][0]["id"]

    response = client.delete(f"{url_prefix}/{ingredient_recipe_association_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {ingredient_recipe_association_id} as Ingredient Recipe Association for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of recipe is deleted successfully"

    ingredient_recipe_association_response = client.get(f"/ingredient_recipe_association/{ingredient_recipe_association_id}")

    assert ingredient_recipe_association_response.status_code == 404
    assert ingredient_recipe_association_response.json()["detail"] == f"ID {ingredient_recipe_association_id} as Ingredient Recipe Association is not found"

def test_delete_ingredient_recipe_association_with_wrong_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff71",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 as Ingredient Recipe Association is not found"

def test_delete_ingredient_recipe_association_with_invalid_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff7z",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "ingredient_recipe_association_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_delete_ingredient_recipe_association_without_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 405
    assert response.json()["detail"] == f"Method Not Allowed"