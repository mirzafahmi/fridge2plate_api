from fastapi.testclient import TestClient
import pytest
from uuid import UUID


url_prefix = '/recipe_tips'

@pytest.fixture
def recipe_tip_id(client, token: str):
    recipe_tip_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        headers={"Authorization": f"Bearer {token}"}
    ).json()["recipe_tips"][0]["id"]

    return recipe_tip_id

def test_get_recipe_tips_list(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Recipe Tip list is retrieved successfully"

    recipe_tips = response.json()['recipe_tips']
    
    assert isinstance(recipe_tips, list)
    assert len(recipe_tips) == 4

    assert recipe_tips[0]["description"] == "tumbuk bahan instead of blender"
    assert recipe_tips[0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe_tips[1]["description"] == "put belacan sedikit"
    assert recipe_tips[1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe_tips[2]["description"] == "test tip 1"
    assert recipe_tips[2]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe_tips[3]["description"] == "test tip 2"
    assert recipe_tips[3]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

def test_get_recipe_tips_list_with_invalid_token(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_recipe_tips_list_without_token(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_recipe_tip_by_id(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.get(f"{url_prefix}/{recipe_tip_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )

    recipe_tip = response.json()['recipe_tip']

    assert recipe_tip["description"] == "tumbuk bahan instead of blender"
    assert recipe_tip["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

def test_get_recipe_tip_by_id_with_invalid_token(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.get(f"{url_prefix}/{recipe_tip_id}", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_recipe_tip_by_id_without_token(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.get(f"{url_prefix}/{recipe_tip_id}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_recipe_tip_with_wrong_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 as Recipe Tip is not found"

def test_get_recipe_tip_by_invalid_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d37633z", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "recipe_tip_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

#test multi case char in post and put
def test_post_recipe_tip(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": ["tESt recipe TIP"],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    assert response.json()["detail"] == "1 of Recipe Tip is created successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    recipe_tips = response.json()['recipe_tips']

    assert recipe_tips[0]["description"] == "test recipe tip"
    assert recipe_tips[0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

def test_post_recipe_tip_with_list_of_tips(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": ["tESt recipe TIP", "second test TIP"],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    assert response.json()["detail"] == "2 of Recipe Tip is created successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    recipe_tips = response.json()['recipe_tips']

    assert recipe_tips[0]["description"] == "test recipe tip"
    assert recipe_tips[0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert recipe_tips[1]["description"] == "second test tip"
    assert recipe_tips[1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

#test with existing list of recipe tips

def test_post_recipe_tip_with_invalid_token(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": ["tESt recipe TIP"],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_post_recipe_tip_without_token(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": ["tESt recipe TIP"],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_post_recipe_tip_with_duplicate_description(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": ["tumbuk bahan instead of blender"],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 409
    assert response.json()["detail"] == "tumbuk bahan instead of blender of Recipe Tip for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe is already registered"

def test_post_recipe_tip_with_non_string_description(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": [2],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422
    
    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'description', 0]
    assert response_json["msg"]  == "Input should be a valid string"
    assert response_json["type"] == "string_type"

def test_post_recipe_tip_with_short_description(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": ["as"],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422
    
    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'description']
    assert response_json["msg"]  == "Value error, String should have at least 3 characters"
    assert response_json["type"] == "value_error"

def test_post_recipe_tip_with_empty_description(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": [""],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422
    
    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'description']
    assert response_json["msg"]  == "Value error, Each Recipe Tip Description must be a non-empty string."
    assert response_json["type"] == "value_error"

def test_post_recipe_tip_without_description_list(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": "",
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422
    
    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'description']
    assert response_json["msg"]  == "Input should be a valid list"
    assert response_json["type"] == "list_type"

def test_post_recipe_tip_without_description(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "description"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_tip_with_wrong_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": ["tESt recipe TIP"],
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff72"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff72 as Recipe is not found"

def test_post_recipe_tip_with_invalid_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": ["tESt recipe TIP"],
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

def test_post_recipe_tip_with_empty_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": ["tESt recipe TIP"],
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

def test_post_recipe_tip_without_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": ["tESt recipe TIP"]
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

def test_put_recipe_tip(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tip_id}", 
        json={
            "description": "tESt recipe TIP updated"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_tip_id} of Recipe Tip is updated successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    recipe_tip = response.json()['recipe_tip']

    assert recipe_tip["description"] == "test recipe tip updated"
    assert recipe_tip["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

def test_put_recipe_tip_with_invalid_token(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tip_id}", 
        json={
            "description": "tESt recipe TIP updated"
        },
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_put_recipe_tip_without_token(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tip_id}", 
        json={
            "description": "tESt recipe TIP updated"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_put_recipe_tip_with_wrong_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff72", 
        json={
            "description": "tESt recipe TIP updated"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff72 as Recipe Tip is not found"

def test_put_recipe_tip_with_invalid_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff7z", 
        json={
            "description": "tESt recipe TIP updated"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "recipe_tip_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_recipe_tip_without_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/", 
        json={
            "description": "tESt recipe TIP updated"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 405
    assert response.json()["detail"] == f"Method Not Allowed"

def test_put_recipe_tip_with_non_string_description(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tip_id}", 
        json={
            "description": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 422
    
    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'description']
    assert response_json["msg"]  == "Input should be a valid string"
    assert response_json["type"] == "string_type"

def test_put_recipe_tip_with_short_description(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tip_id}", 
        json={
            "description": "as"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422
    
    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'description']
    assert response_json["msg"]  == "String should have at least 3 characters"
    assert response_json["type"] == "string_too_short"

def test_put_recipe_tip_with_empty_description(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tip_id}", 
        json={
            "description": ""
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422
    
    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'description']
    assert response_json["msg"]  == "String should have at least 3 characters"
    assert response_json["type"] == "string_too_short"

def test_put_recipe_tip_without_description(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tip_id}", 
        json={},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 422

    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'description']
    assert response_json["msg"]  == "Field required"
    assert response_json["type"] == "missing"

def test_delete_recipe_tip(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.delete(f"{url_prefix}/{recipe_tip_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_tip_id} as Recipe Tip is deleted successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    recipe_tip_response = client.get(f"{url_prefix}/{recipe_tip_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert recipe_tip_response.status_code == 404
    assert recipe_tip_response.json()["detail"] == f"ID {recipe_tip_id} as Recipe Tip is not found"

def test_delete_recipe_tip_with_invalid_token(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.delete(f"{url_prefix}/{recipe_tip_id}", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_delete_recipe_tip_without_token(client: TestClient, recipe_tip_id: UUID, token: str):
    response = client.delete(f"{url_prefix}/{recipe_tip_id}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_delete_recipe_tip_with_wrong_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 as Recipe Tip is not found"

def test_delete_recipe_tip_with_invalid_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff7z", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "recipe_tip_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_delete_recipe_tip_without_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 405
    assert response.json()["detail"] == f"Method Not Allowed"
