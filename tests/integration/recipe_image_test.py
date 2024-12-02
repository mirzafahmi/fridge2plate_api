from fastapi.testclient import TestClient


url_prefix = '/recipe_image'

def test_get_recipe_images_list(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["detail"] == "Recipe Images list is retrieved successfully"

    recipe_images = response.json()['recipe_images']

    assert isinstance(recipe_images, list)
    assert len(recipe_images) == 4

    recipe_images[0]["image"] == "/string_test"
    recipe_images[0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    recipe_images[1]["image"] == "https://www.simplyrecipes.com/thmb/KRw_r32s4gQeOX-d07NWY1OlOFk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1c-c2b1885d27d4481c9cfe6f6286a64342.jpg"
    recipe_images[1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    recipe_images[2]["image"] == "/string_test"
    recipe_images[2]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    recipe_images[3]["image"] == "/test_recipe_image"
    recipe_images[3]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

def test_get_recipe_image_by_id(client: TestClient, token: str):
    recipe_image_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        headers={"Authorization": f"Bearer {token}"}
        ).json()["recipe_images"][1]["id"]
    
    response = client.get(f"{url_prefix}/{recipe_image_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_image_id} as Recipe Image is retrieved successfully"

    recipe_image = response.json()['recipe_image']

    recipe_image["image"] == "https://www.simplyrecipes.com/thmb/KRw_r32s4gQeOX-d07NWY1OlOFk=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Simply-Recipes-Homemade-Pizza-Dough-Lead-Shot-1c-c2b1885d27d4481c9cfe6f6286a64342.jpg"
    recipe_image["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

def test_get_recipe_image_with_wrong_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 as Recipe Image is not found"

def test_get_recipe_image_with_invalid_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff7z", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "recipe_image_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_image(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": [
                "/test_post_recipe_image", 
                "https://www.foodandwine.com/thmb/ppDgfqJYhMeDAxtArwoYEssEMkI=/750x0/filters:no_upscale():max_bytes(150000):strip_icc()/bucatini-with-mushroom-ragu-dandelion-greens-and-tarragon-FT-RECIPE0421-3a5f0d29f7264f5e9952d4a3a51f5f58.jpg"
                ],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        }
    )
    
    assert response.status_code == 201
    assert response.json()["detail"] == f"['/test_post_recipe_image', 'https://www.foodandwine.com/thmb/ppDgfqJYhMeDAxtArwoYEssEMkI=/750x0/filters:no_upscale():max_bytes(150000):strip_icc()/bucatini-with-mushroom-ragu-dandelion-greens-and-tarragon-FT-RECIPE0421-3a5f0d29f7264f5e9952d4a3a51f5f58.jpg'] of Recipe Image is created successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    recipe_image = response.json()["recipe_images"]

    assert recipe_image[0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe_image[0]["image"] == "/test_post_recipe_image"

    assert recipe_image[1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe_image[1]["image"] == "https://www.foodandwine.com/thmb/ppDgfqJYhMeDAxtArwoYEssEMkI=/750x0/filters:no_upscale():max_bytes(150000):strip_icc()/bucatini-with-mushroom-ragu-dandelion-greens-and-tarragon-FT-RECIPE0421-3a5f0d29f7264f5e9952d4a3a51f5f58.jpg"

def test_post_recipe_image_with_non_string(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": [2],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        }
    )
    
    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 2
    
    assert response_json["detail"][0]["loc"] == ["body", "image", 0,"url['http','https']"]
    assert response_json["detail"][0]["msg"] == "URL input should be a string or URL"
    assert response_json["detail"][0]["type"] == "url_type"

    assert response_json["detail"][1]["loc"] == ["body", "image", 0, "str"]
    assert response_json["detail"][1]["msg"] == "Input should be a valid string"
    assert response_json["detail"][1]["type"] == "string_type"

def test_post_recipe_image_with_empty_string(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": [""],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        }
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "image"]
    assert response_json["detail"][0]["msg"] == "Value error, Each image in the list must not be an empty string."
    assert response_json["detail"][0]["type"] == "value_error"

def test_post_recipe_image_with_wrong_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": [
                "/test_post_recipe_image", 
                "https://www.foodandwine.com/thmb/ppDgfqJYhMeDAxtArwoYEssEMkI=/750x0/filters:no_upscale():max_bytes(150000):strip_icc()/bucatini-with-mushroom-ragu-dandelion-greens-and-tarragon-FT-RECIPE0421-3a5f0d29f7264f5e9952d4a3a51f5f58.jpg"
                ],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff72"
        }
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff72 as Recipe is not found"

def test_post_recipe_image_with_invalid_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": [
                "/test_post_recipe_image", 
                "https://www.foodandwine.com/thmb/ppDgfqJYhMeDAxtArwoYEssEMkI=/750x0/filters:no_upscale():max_bytes(150000):strip_icc()/bucatini-with-mushroom-ragu-dandelion-greens-and-tarragon-FT-RECIPE0421-3a5f0d29f7264f5e9952d4a3a51f5f58.jpg"
                ],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff7z"
        }
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "recipe_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_image_with_empty_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": [
                "/test_post_recipe_image", 
                "https://www.foodandwine.com/thmb/ppDgfqJYhMeDAxtArwoYEssEMkI=/750x0/filters:no_upscale():max_bytes(150000):strip_icc()/bucatini-with-mushroom-ragu-dandelion-greens-and-tarragon-FT-RECIPE0421-3a5f0d29f7264f5e9952d4a3a51f5f58.jpg"
                ],
            "recipe_id": ""
        }
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "recipe_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_image_without_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": [
                "/test_post_recipe_image", 
                "https://www.foodandwine.com/thmb/ppDgfqJYhMeDAxtArwoYEssEMkI=/750x0/filters:no_upscale():max_bytes(150000):strip_icc()/bucatini-with-mushroom-ragu-dandelion-greens-and-tarragon-FT-RECIPE0421-3a5f0d29f7264f5e9952d4a3a51f5f58.jpg"
                ]
        }
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "recipe_id"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_image_with_empty_json(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"},
        json={}
    )
    
    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 2
    
    assert response_json["detail"][0]["loc"] == ["body", "image"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

    assert response_json["detail"][1]["loc"] == ["body", "recipe_id"]
    assert response_json["detail"][1]["msg"] == "Field required"
    assert response_json["detail"][1]["type"] == "missing"

def test_put_recipe_image(client: TestClient, token: str):
    recipe_image_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["recipe_images"][0]["id"]
    
    response = client.put(f"{url_prefix}/{recipe_image_id}", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": "/test_updated_recipe_image",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        }
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_image_id} of Recipe Image is updated successfully for ID 6b86885b-a613-4ca6-a9b7-584c3d376337 of Recipe"

    recipe_image = response.json()["recipe_image"]
    
    assert recipe_image["image"] == "/test_updated_recipe_image"
    assert recipe_image["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

def test_put_recipe_image_with_wrong_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/b3cceb34-9465-4020-9066-f7b5ce3c372c", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": "/test_updated_recipe_image",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID b3cceb34-9465-4020-9066-f7b5ce3c372c as Recipe Image is not found"

def test_put_recipe_image_with_invalid_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d37633z", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": "/test_updated_recipe_image",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        }
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "recipe_image_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_recipe_image_with_empty_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": "/test_updated_recipe_image",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        }
    )

    assert response.status_code == 405
    assert response.json()["detail"] == f"Method Not Allowed"

def test_put_recipe_image_by_changing_image_path(client: TestClient, token: str):
    recipe_image_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["recipe_images"][0]["id"]
    
    response = client.put(f"{url_prefix}/{recipe_image_id}", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": "/test_updated_recipe_image"
        }
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_image_id} of Recipe Image is updated successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    recipe_image = response.json()["recipe_image"]
    
    assert recipe_image["image"] == "/test_updated_recipe_image"
    assert recipe_image["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

def test_put_recipe_image_with_invalid_image_path(client: TestClient, token: str):
    recipe_image_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["recipe_images"][0]["id"]
    
    response = client.put(f"{url_prefix}/{recipe_image_id}", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": 2
        }
    )
    
    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 2
    
    assert response_json["detail"][0]["loc"] == ["body", "image", "url['http','https']"]
    assert response_json["detail"][0]["msg"] == "URL input should be a string or URL"
    assert response_json["detail"][0]["type"] == "url_type"

    assert response_json["detail"][1]["loc"] == ["body", "image", "str"]
    assert response_json["detail"][1]["msg"] == "Input should be a valid string"
    assert response_json["detail"][1]["type"] == "string_type"

def test_put_recipe_image_with_empty_image_path(client: TestClient, token: str):
    recipe_image_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["recipe_images"][0]["id"]
    
    response = client.put(f"{url_prefix}/{recipe_image_id}", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "image": ""
        }
    )
    
    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "image"]
    assert response_json["detail"][0]["msg"] == "Value error, Image must not be an empty string."
    assert response_json["detail"][0]["type"] == "value_error"

def test_put_recipe_image_by_changing_recipe_id(client: TestClient, token: str):
    recipe_image_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["recipe_images"][0]["id"]
    
    response = client.put(f"{url_prefix}/{recipe_image_id}", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        }
    )
    
    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_image_id} of Recipe Image is updated successfully for ID 6b86885b-a613-4ca6-a9b7-584c3d376337 of Recipe"

    recipe_image = response.json()["recipe_image"]
    
    assert recipe_image["image"] == "/string_test"
    assert recipe_image["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

def test_put_recipe_image_with_wrong_recipe_id(client: TestClient, token: str):
    recipe_image_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["recipe_images"][0]["id"]
    
    response = client.put(f"{url_prefix}/{recipe_image_id}", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376338"
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 6b86885b-a613-4ca6-a9b7-584c3d376338 as Recipe is not found"

def test_put_recipe_image_with_invalid_recipe_id(client: TestClient, token: str):
    recipe_image_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["recipe_images"][0]["id"]
    
    response = client.put(f"{url_prefix}/{recipe_image_id}", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d37633z"
        }
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ['body', "recipe_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_recipe_image_with_empty_recipe_id(client: TestClient, token: str):
    recipe_image_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["recipe_images"][0]["id"]
    
    response = client.put(f"{url_prefix}/{recipe_image_id}", 
        headers={"Authorization": f"Bearer {token}"},
        json={
            "recipe_id": ""
        }
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "recipe_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_recipe_image_with_empty_json(client: TestClient, token: str):
    recipe_image_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["recipe_images"][0]["id"]
    
    response = client.put(f"{url_prefix}/{recipe_image_id}", 
        headers={"Authorization": f"Bearer {token}"},
        json={}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Request body must include at least one field to update"

def test_delete_recipe_image(client: TestClient, token: str):
    recipe_image_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71").json()["recipe_images"][0]["id"]
    
    response = client.delete(f"{url_prefix}/{recipe_image_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_image_id} as Recipe Image for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe is deleted successfully"

    recipe_image_response = client.get(f"/recipe_image/{recipe_image_id}")

    assert recipe_image_response.status_code == 404
    assert recipe_image_response.json()["detail"] == f"ID {recipe_image_id} as Recipe Image is not found"

def test_delete_recipe_image_with_wrong_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff71",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 as Recipe Image is not found"

def test_delete_recipe_image_with_invalid_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff7z",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "recipe_image_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_delete_recipe_image_without_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 405
    assert response.json()["detail"] == f"Method Not Allowed"