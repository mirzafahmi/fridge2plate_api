from fastapi.testclient import TestClient
import pytest
from uuid import UUID


url_prefix = '/recipe_tag_recipe_associations'

@pytest.fixture
def recipe_tag_recipe_association_id(client, token: str):
    recipe_tag_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        headers={"Authorization": f"Bearer {token}"}
    ).json()["recipe_tag_recipe_associations"][0]["id"]

    return recipe_tag_recipe_association_id

def test_get_recipe_tag_recipe_association_list(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["detail"] == "Recipe Tag Recipe Association list is retrieved successfully"

    recipe_tag_recipe_associations = response.json()['recipe_tag_recipe_associations']

    assert isinstance(recipe_tag_recipe_associations, list)
    assert len(recipe_tag_recipe_associations) == 4

    assert recipe_tag_recipe_associations[0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe_tag_recipe_associations[0]["recipe_tag"]["name"] == "beginner"

    assert recipe_tag_recipe_associations[1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe_tag_recipe_associations[1]["recipe_tag"]["name"] == "eid"

    assert recipe_tag_recipe_associations[2]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe_tag_recipe_associations[2]["recipe_tag"]["name"] == "beginner"

    assert recipe_tag_recipe_associations[3]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"
    assert recipe_tag_recipe_associations[3]["recipe_tag"]["name"] == "eid"

def test_get_recipe_tag_recipe_association_list_with_invalid_token(client: TestClient):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_recipe_tag_recipe_association_list_without_token(client: TestClient):
    response = client.get(f"{url_prefix}/"
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_recipe_tag_recipe_association_by_id(client: TestClient, token: str):
    recipe_tag_recipe_association_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        headers={"Authorization": f"Bearer {token}"}
        ).json()["recipe_tag_recipe_associations"][0]["id"]

    response = client.get(f"{url_prefix}/{recipe_tag_recipe_association_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )

    recipe_tag_recipe_association = response.json()['recipe_tag_recipe_association']

    assert recipe_tag_recipe_association["id"] == recipe_tag_recipe_association_id
    assert recipe_tag_recipe_association["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe_tag_recipe_association["recipe_tag"]["name"] == "beginner"

def test_get_recipe_tag_recipe_association_by_wrong_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()['detail'] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 as Recipe Tag Recipe Association is not found"

def test_post_recipe_tag_recipe_association(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8",
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    assert response.json()["detail"] == f"ID 3d460ec6-f369-4681-851d-78999ec3d2a8 of Recipe Tag as Recipe Tag Recipe Association is created successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    recipe_tag_recipe_association = response.json()["recipe_tag_recipe_association"]

    assert recipe_tag_recipe_association["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe_tag_recipe_association["recipe_tag"]["name"] == "quick & easy"

def test_post_recipe_tag_recipe_association(client: TestClient):
    response = client.post(f"{url_prefix}/", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8",
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_post_recipe_tag_recipe_association(client: TestClient):
    response = client.post(f"{url_prefix}/", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8",
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_post_recipe_tag_recipe_association_with_duplicate_recipe_tag_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "recipe_tag_id": "13444244-43b2-4d63-a080-604dd5088452",
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "ID 13444244-43b2-4d63-a080-604dd5088452 of Recipe Tag as Recipe Tag Recipe Association is already registered"

def test_post_recipe_tag_recipe_association_with_wrong_recipe_tag_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "recipe_tag_id": "13444244-43b2-4d63-a080-604dd5088453",
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ID 13444244-43b2-4d63-a080-604dd5088453 as Recipe Tag is not found"

def test_post_recipe_tag_recipe_association_with_invalid_recipe_tag_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "recipe_tag_id": "13444244-43b2-4d63-a080-604dd508845z",
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "recipe_tag_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_tag_recipe_association_with_empty_recipe_tag_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "recipe_tag_id": "",
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff71"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "recipe_tag_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_tag_recipe_association_without_recipe_tag_id(client: TestClient, token: str):
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

    assert response_json["detail"][0]["loc"] == ["body", "recipe_tag_id"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_recipe_tag_recipe_association_wrong_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8",
            "recipe_id": "2cdd1a37-9c45-4202-a38c-026686b0ff72"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff72 as Recipe is not found"

def test_post_recipe_tag_recipe_association_invalid_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8",
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

def test_post_recipe_tag_recipe_association_empty_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8",
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

def test_post_recipe_tag_recipe_association_without_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8"
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

def test_post_recipe_tag_recipe_association_without_data(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"][0]["loc"] == ["body", "recipe_tag_id"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

    assert response_json["detail"][1]["loc"] == ["body", "recipe_id"]
    assert response_json["detail"][1]["msg"] == "Field required"
    assert response_json["detail"][1]["type"] == "missing"

def test_put_recipe_tag_recipe_association_by_changing_recipe_tag_id(client: TestClient, recipe_tag_recipe_association_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tag_recipe_association_id}", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"ID 3d460ec6-f369-4681-851d-78999ec3d2a8 of Recipe Tag as Recipe Tag Recipe Association is updated successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    recipe_tag_recipe_association = response.json()["recipe_tag_recipe_association"]
    
    assert recipe_tag_recipe_association["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    assert recipe_tag_recipe_association["recipe_tag"]["name"] == "quick & easy"

def test_put_recipe_tag_recipe_association_by_changing_recipe_tag_id_with_invalid_token(client: TestClient, recipe_tag_recipe_association_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tag_recipe_association_id}", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8",
        },
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_put_recipe_tag_recipe_association_by_changing_recipe_tag_id_without_token(client: TestClient, recipe_tag_recipe_association_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tag_recipe_association_id}", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8",
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_put_recipe_tag_recipe_association_by_with_wrong_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/b3cceb34-9465-4020-9066-f7b5ce3c372c", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID b3cceb34-9465-4020-9066-f7b5ce3c372c as Recipe Tag Recipe Association is not found"

def test_put_recipe_tag_recipe_association_by_with_invalid_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/b3cceb34-9465-4020-9066-f7b5ce3c372z", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "recipe_tag_recipe_association_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_recipe_tag_recipe_association_by_without_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a8",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 405
    assert response.json()["detail"] == f"Method Not Allowed"

def test_put_recipe_tag_recipe_association_by_with_wrong_recipe_tag_id(client: TestClient, recipe_tag_recipe_association_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tag_recipe_association_id}", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2a9",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ID 3d460ec6-f369-4681-851d-78999ec3d2a9 as Recipe Tag is not found"

def test_put_recipe_tag_recipe_association_by_with_invalid_recipe_tag_id(client: TestClient, recipe_tag_recipe_association_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tag_recipe_association_id}", 
        json={
            "recipe_tag_id": "3d460ec6-f369-4681-851d-78999ec3d2az",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "recipe_tag_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_recipe_tag_recipe_association_by_with_empty_recipe_tag_id(client: TestClient, recipe_tag_recipe_association_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tag_recipe_association_id}", 
        json={
            "recipe_tag_id": "",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "recipe_tag_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_recipe_tag_recipe_association_by_without_data(client: TestClient, recipe_tag_recipe_association_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_tag_recipe_association_id}", 
        json={},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Request body must include at least one field to update"

def test_delete_recipe_tag_recipe_association(client: TestClient, recipe_tag_recipe_association_id: UUID, token: str):
    response = client.delete(f"{url_prefix}/{recipe_tag_recipe_association_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_tag_recipe_association_id} as Recipe Tag Recipe Association for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe is deleted successfully"

    recipe_tag_recipe_association_response = client.get(f"{url_prefix}/{recipe_tag_recipe_association_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert recipe_tag_recipe_association_response.status_code == 404
    assert recipe_tag_recipe_association_response.json()["detail"] == f"ID {recipe_tag_recipe_association_id} as Recipe Tag Recipe Association is not found"

def test_delete_recipe_tag_recipe_association_with_invalid_token(client: TestClient, recipe_tag_recipe_association_id: UUID, token: str):
    response = client.delete(f"{url_prefix}/{recipe_tag_recipe_association_id}",
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_delete_recipe_tag_recipe_association_without_token(client: TestClient, recipe_tag_recipe_association_id: UUID, token: str):
    response = client.delete(f"{url_prefix}/{recipe_tag_recipe_association_id}"
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
    
def test_delete_recipe_tag_recipe_association_with_wrong_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff71",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 as Recipe Tag Recipe Association is not found"

def test_delete_recipe_tag_recipe_association_with_invalid_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff7z",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "recipe_tag_recipe_association_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_delete_recipe_tag_recipe_association_without_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 405
    assert response.json()["detail"] == f"Method Not Allowed"