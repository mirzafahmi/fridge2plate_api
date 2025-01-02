from fastapi.testclient import TestClient
import pytest


url_prefix = '/badges'
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

def test_get_badge_list(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Badge list is retrieved successfully"

    badges = response.json()["badges"]

    assert isinstance(badges, list)
    assert len(badges) == 3

    assert badges[0]['id'] == "6446f1e0-fd4a-455e-a9d0-e77c8c059140"
    assert badges[0]['name'] == "community leader"
    assert badges[0]['description'] == "reached at least 5 follower"
    assert badges[0]['image'] == "/static/badges/community_leader.png"
    assert badges[0]["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in badges[0]
    assert "created_date" in badges[0]

    assert badges[1]['id'] == "3afb1e3d-617e-41f8-b140-b6a5fd876446"
    assert badges[1]['name'] == "getting started"
    assert badges[1]['description'] == "created at least 1 recipe"
    assert badges[1]['image'] == "/static/badges/getting_started.png"
    assert badges[1]["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in badges[1]
    assert "created_date" in badges[1]

    assert badges[2]['id'] == "52518fea-cae4-4a79-abf4-65cb8a122f16"
    assert badges[2]['name'] == "veteran"
    assert badges[2]['description'] == "created at least 5 recipe"
    assert badges[2]['image'] == "/static/badges/veteran.png"
    assert badges[2]["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in badges[2]
    assert "created_date" in badges[2]

def test_get_badge_list_with_invalid_token(client: TestClient):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_badge_list_without_token(client: TestClient):
    response = client.get(f"{url_prefix}/")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_badge_by_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"Id 6446f1e0-fd4a-455e-a9d0-e77c8c059140 as Badge is retrieved successfully"

    badge = response.json()["badge"]
    
    assert badge['id'] == "6446f1e0-fd4a-455e-a9d0-e77c8c059140"
    assert badge['name'] == "community leader"
    assert badge['description'] == "reached at least 5 follower"
    assert badge['image'] == "/static/badges/community_leader.png"
    assert badge["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in badge
    assert "created_date" in badge

def test_get_badge_by_id_with_invalid_token(client: TestClient):
    response = client.get(f"{url_prefix}/92e80174-c259-480a-80b5-f5b0d32ca005", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_badge_by_id_without_token(client: TestClient):
    response = client.get(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_badge_by_wrong_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f01", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Id b4b165f6-a4f2-45f6-bda6-0a49092d3f01 as Badge is not found"

def test_post_badge(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test badge",
            "description": "test badge description",
            "image": "/static/badges/test_badge.png",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["detail"] == f"test badge as Badge is created successfully"

    badge = response.json()["badge"]

    assert badge["name"] == "test badge"
    assert badge["description"] == "test badge description"
    assert badge["image"] == "/static/badges/test_badge.png"
    assert badge["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in badge
    assert "created_date" in badge

def test_post_badge_with_invalid_token(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test badge",
            "description": "test badge description",
            "image": "/static/badges/test_badge.png",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_post_badge(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test badge",
            "description": "test badge description",
            "image": "/static/badges/test_badge.png",
            "created_by": ADMIN_ID
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_post_badge_with_various_cases(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "teST Badge",
            "description": "test baDGe dEScription",
            "image": "/static/badges/teST_badge.png",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["detail"] == f"test badge as Badge is created successfully"

    badge = response.json()["badge"]

    assert badge["name"] == "test badge"
    assert badge["description"] == "test badge description"
    assert badge["image"] == "/static/badges/test_badge.png"
    assert badge["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in badge
    assert "created_date" in badge

def test_post_badge_with_duplicate_name(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "veteran",
            "description": "test baDGe dEScription",
            "image": "/static/badges/teST_badge.png",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == f"veteran as Badge is already registered"

def test_post_badge_with_empty_name(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "",
            "description": "test baDGe dEScription",
            "image": "/static/badges/teST_badge.png",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_badge_without_name(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": "test baDGe dEScription",
            "image": "/static/badges/teST_badge.png",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_badge_with_empty_description(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test badge",
            "description": "",
            "image": "/static/badges/test_badge.png",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "description"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_badge_without_description(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test badge",
            "image": "/static/badges/test_badge.png",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["detail"] == f"test badge as Badge is created successfully"

    badge = response.json()["badge"]

    assert badge["name"] == "test badge"
    assert badge["description"] == ""
    assert badge["image"] == "/static/badges/test_badge.png"
    assert badge["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in badge
    assert "created_date" in badge

def test_post_badge_with_empty_image(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test badge",
            "description": "test badge description",
            "image": "",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "image"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_badge_without_image(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test badge",
            "description": "test badge description",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "image"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_badge_with_not_available_creator_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test badge",
            "description": "test badge description",
            "image": "/static/badges/test_badge.png",
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 3fa85f64-5717-4562-b3fc-2c963f66afa6 as User is not found"

def test_post_badge_with_invalid_creator_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test badge",
            "description": "test badge description",
            "image": "/static/badges/test_badge.png",
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afaz"
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_badge_with_empty_creator_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test badge",
            "description": "test badge description",
            "image": "/static/badges/test_badge.png",
            "created_by": ""
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

@pytest.mark.xfail(reason="due to admin_id default of test env diff from prod")
def test_post_badge_without_creator_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "name": "test badge",
            "description": "test badge description",
            "image": "/static/badges/test_badge.png"
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_badge(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/3afb1e3d-617e-41f8-b140-b6a5fd876446", 
        json={
            "name": "test badge",
            "description": "test badge description",
            "image": "/static/badges/test_badge.png",
            "created_by": ADMIN_ID
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"Id 3afb1e3d-617e-41f8-b140-b6a5fd876446 as Badge is updated successfully"

    badge = response.json()["badge"]

    assert badge["name"] == "test badge"
    assert badge["description"] == "test badge description"
    assert badge["image"] == "/static/badges/test_badge.png"
    assert badge["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in badge
    assert "created_date" in badge

def test_put_badge_by_changing_name(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        json={
            "name": "test badge"
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"Id 6446f1e0-fd4a-455e-a9d0-e77c8c059140 as Badge is updated successfully"

    badge = response.json()["badge"]

    assert badge['id'] == "6446f1e0-fd4a-455e-a9d0-e77c8c059140"
    assert badge['name'] == "test badge"
    assert badge['description'] == "reached at least 5 follower"
    assert badge['image'] == "/static/badges/community_leader.png"
    assert badge["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in badge
    assert "created_date" in badge

def test_put_badge_with_empty_name(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        json={
            "name": ""
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_put_badge_by_changing_description(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        json={
            "description": "test badge description"
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"Id 6446f1e0-fd4a-455e-a9d0-e77c8c059140 as Badge is updated successfully"

    badge = response.json()["badge"]

    assert badge['id'] == "6446f1e0-fd4a-455e-a9d0-e77c8c059140"
    assert badge['name'] == "community leader"
    assert badge['description'] == "test badge description"
    assert badge['image'] == "/static/badges/community_leader.png"
    assert badge["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in badge
    assert "created_date" in badge

def test_put_badge_with_empty_description(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        json={
            "description": ""
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "description"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_put_badge_by_changing_image(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        json={
            "image": "/static/badges/test_badge.png"
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"Id 6446f1e0-fd4a-455e-a9d0-e77c8c059140 as Badge is updated successfully"

    badge = response.json()["badge"]

    assert badge['id'] == "6446f1e0-fd4a-455e-a9d0-e77c8c059140"
    assert badge['name'] == "community leader"
    assert badge['description'] == "reached at least 5 follower"
    assert badge['image'] == "/static/badges/test_badge.png"
    assert badge["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in badge
    assert "created_date" in badge

def test_put_badge_with_short_image(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        json={
            "image": ""
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "image"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_put_badge_by_changing_creator(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        json={
            "created_by": "0c619092-817e-4f73-b25f-8e187e69dded"
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 202
    assert response.json()["detail"] == f"Id 6446f1e0-fd4a-455e-a9d0-e77c8c059140 as Badge is updated successfully"

    badge = response.json()["badge"]

    assert badge['id'] == "6446f1e0-fd4a-455e-a9d0-e77c8c059140"
    assert badge['name'] == "community leader"
    assert badge['description'] == "reached at least 5 follower"
    assert badge['image'] == "/static/badges/community_leader.png"
    assert badge["creator"]["id"]== "0c619092-817e-4f73-b25f-8e187e69dded"
    assert "updated_date" in badge
    assert "created_date" in badge

def test_put_recipe_origin_with_not_available_creator_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        json={
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 3fa85f64-5717-4562-b3fc-2c963f66afa6 as User is not found"

def test_put_recipe_origin_with_invalid_creator_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        json={
            "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afaz"
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_recipe_origin_with_empty_creator_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        json={
            "created_by": ""
        }, 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_delete_badge(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Id 6446f1e0-fd4a-455e-a9d0-e77c8c059140 as Badge is deleted successfully"

def test_delete_badge_with_invalid_token(client: TestClient):
    response = client.delete(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_delete_badge_without_token(client: TestClient):
    response = client.delete(f"{url_prefix}/6446f1e0-fd4a-455e-a9d0-e77c8c059140")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_delete_badge_by_wrong_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/db67b3f4-0e04-47bb-bc46-94826847ee4f", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Id db67b3f4-0e04-47bb-bc46-94826847ee4f as Badge is not found"