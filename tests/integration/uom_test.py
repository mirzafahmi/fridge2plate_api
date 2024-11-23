from fastapi.testclient import TestClient


url_prefix = '/uoms'
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

#TODO add combination of empty field for post and put endpoint
def test_get_uom_list(client: TestClient):
    response = client.get(f"{url_prefix}/")

    assert response.status_code == 200
    assert response.json()["detail"] == "UOM list is retrieved successfully"

    uoms = response.json()["uoms"]

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

def test_get_uom_by_id(client: TestClient):
    response = client.get(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38")

    assert response.status_code == 200
    assert response.json()["detail"] == f"Id 8c935f60-2f3a-410a-9860-09bb2c270a38 as UOM is retrieved successfully"

    uom = response.json()["uom"]
    
    assert uom['id'] == "8c935f60-2f3a-410a-9860-09bb2c270a38"
    assert uom['name'] == "clove"
    assert uom['unit'] == "clove"
    assert uom['weightage'] == 1.0
    assert uom["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in uom
    assert "created_date" in uom

def test_get_uom_by_wrong_id(client: TestClient):
    response = client.get(f"{url_prefix}/b4b165f6-a4f2-45f6-bda6-0a49092d3f01")

    assert response.status_code == 404
    assert response.json()["detail"] == "Id b4b165f6-a4f2-45f6-bda6-0a49092d3f01 as UOM is not found"

def test_post_uom(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test UOM",
        "unit": "test UOM",
        "weightage": 1,
        "created_by": ADMIN_ID
    })

    assert response.status_code == 201
    assert response.json()["detail"] == f"test uom as UOM is successfully created"

    uom = response.json()["uom"]

    assert uom["name"] == "test uom"
    assert uom["unit"] == "test UOM"
    assert uom["weightage"] == 1.0
    assert uom["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in uom
    assert "created_date" in uom

def test_post_uom_with_various_letter_case(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "tESt UOM",
        "unit": "test UOM",
        "weightage": 1,
        "created_by": ADMIN_ID
    })

    assert response.status_code == 201
    assert response.json()["detail"] == f"test uom as UOM is successfully created"

    uom = response.json()["uom"]

    assert uom["name"] == "test uom"
    assert uom["unit"] == "test UOM"
    assert uom["weightage"] == 1.0
    assert uom["creator"]["id"] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in uom
    assert "created_date" in uom

def test_post_uom_with_duplicate_name(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "piece",
        "unit": "test UOM unit",
        "weightage": 1,
        "created_by": ADMIN_ID
    })

    assert response.status_code == 400
    assert response.json()["detail"] == f"piece as UOM is already registered"

def test_post_uom_with_empty_name(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "",
        "unit": "test UOM unit",
        "weightage": 1,
        "created_by": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_uom_without_name(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "unit": "test UOM unit",
        "weightage": 1,
        "created_by": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_uom_with_duplicate_unit(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test UOM",
        "unit": "piece",
        "weightage": 1,
        "created_by": ADMIN_ID
    })

    assert response.status_code == 400
    assert response.json()["detail"] == f"piece as UOM unit is already registered"

def test_post_uom_with_empty_unit(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test UOM",
        "unit": "",
        "weightage": 1,
        "created_by": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "unit"]
    assert response_json["detail"][0]["msg"] == "String should have at least 1 character"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_post_uom_with_without_unit(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test UOM",
        "weightage": 1,
        "created_by": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "unit"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_uom_with_with_empty_weightage(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test UOM",
        "unit": "test UOM unit",
        "weightage": 0,
        "created_by": ADMIN_ID
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "weightage"]
    assert response_json["detail"][0]["msg"] == "Input should be greater than 0"
    assert response_json["detail"][0]["type"] == "greater_than"

def test_post_uom_with_without_weightage(client: TestClient):
    response = client.post(f"{url_prefix}/", json={
        "name": "test UOM",
        "unit": "test UOM unit",
        "created_by": ADMIN_ID
    })
    
    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "weightage"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_post_uom_with_not_available_creator_id(client: TestClient): 
    response = client.post(f"{url_prefix}/", json={
        "name": "test UOM",
        "unit": "test UOM unit",
        "weightage": 1,
        "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    })

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 3fa85f64-5717-4562-b3fc-2c963f66afa6 as User is not found"

def test_post_uom_with_invalid_creator_id(client: TestClient): 
    response = client.post(f"{url_prefix}/", json={
        "name": "test UOM",
        "unit": "test UOM unit",
        "weightage": 1,
        "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afaz"
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_uom_with_empty_creator_id(client: TestClient): 
    response = client.post(f"{url_prefix}/", json={
        "name": "test UOM",
        "unit": "test UOM unit",
        "weightage": 1,
        "created_by": ""
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_uom_by_changing_name(client: TestClient):
    response = client.put(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38", json={
        "name": "updated uom",
    })

    assert response.status_code == 202
    assert response.json()["detail"] == "Id 8c935f60-2f3a-410a-9860-09bb2c270a38 as UOM is successfully updated"

    uom = response.json()["uom"]

    assert uom['id'] == "8c935f60-2f3a-410a-9860-09bb2c270a38"
    assert uom['name'] == "updated uom"
    assert uom["unit"] == "clove"
    assert uom["weightage"] == 1.0
    assert uom["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in uom
    assert "created_date" in uom

def test_put_uom_by_changing_name_with_various_letter_case(client: TestClient):
    response = client.put(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38", json={
        "name": "updated UOM",
    })

    assert response.status_code == 202
    assert response.json()["detail"] == "Id 8c935f60-2f3a-410a-9860-09bb2c270a38 as UOM is successfully updated"

    uom = response.json()["uom"]

    assert uom['id'] == "8c935f60-2f3a-410a-9860-09bb2c270a38"
    assert uom['name'] == "updated uom"
    assert uom["unit"] == "clove"
    assert uom["weightage"] == 1.0
    assert uom["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in uom
    assert "created_date" in uom

def test_put_uom_by_changing_name_with_duplicate_name(client: TestClient):
    response = client.put(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38", json={
        "name": "piece",
    })

    assert response.status_code == 400
    assert response.json()["detail"] == f"piece as UOM is already registered"

def test_put_uom_with_empty_name(client: TestClient):
    response = client.put(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38", json={
        "name": "",
    })

    assert response.status_code == 422
    
    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "name"]
    assert response_json["detail"][0]["msg"] == "String should have at least 3 characters"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_put_uom_by_changing_unit(client: TestClient):
    response = client.put(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38", json={
        "unit": "updated uom unit",
    })

    assert response.status_code == 202
    assert response.json()["detail"] == "Id 8c935f60-2f3a-410a-9860-09bb2c270a38 as UOM is successfully updated"

    uom = response.json()["uom"]

    assert uom['id'] == "8c935f60-2f3a-410a-9860-09bb2c270a38"
    assert uom['name'] == "clove"
    assert uom["unit"] == "updated uom unit"
    assert uom["weightage"] == 1.0
    assert uom["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in uom
    assert "created_date" in uom

def test_put_uom_by_changing_unit_with_various_letter_case(client: TestClient):
    response = client.put(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38", json={
        "unit": "updated UOM UNIT",
    })

    assert response.status_code == 202
    assert response.json()["detail"] == "Id 8c935f60-2f3a-410a-9860-09bb2c270a38 as UOM is successfully updated"

    uom = response.json()["uom"]

    assert uom['id'] == "8c935f60-2f3a-410a-9860-09bb2c270a38"
    assert uom['name'] == "clove"
    assert uom["unit"] == "updated UOM UNIT"
    assert uom["weightage"] == 1.0
    assert uom["creator"]["id"]== "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert "updated_date" in uom
    assert "created_date" in uom

def test_put_uom_by_changing_unit_with_duplicate_unit(client: TestClient):
    response = client.put(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38", json={
        "unit": "piece",
    })

    assert response.status_code == 400
    assert response.json()["detail"] == f"piece as UOM unit is already registered"

def test_put_uom_by_changing_unit_with_empty_unit(client: TestClient):
    response = client.put(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38", json={
        "unit": "",
    })

    assert response.status_code == 422
    
    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "unit"]
    assert response_json["detail"][0]["msg"] == "String should have at least 1 character"
    assert response_json["detail"][0]["type"] == "string_too_short"

def test_put_uom_with_not_available_creator_id(client: TestClient):
    response = client.put(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38", json={
        "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    })

    assert response.status_code == 404
    assert response.json()["detail"] == f"Id 3fa85f64-5717-4562-b3fc-2c963f66afa6 as User is not found"

def test_put_uom_with_invalid_creator_id(client: TestClient):
    response = client.put(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38", json={
        "created_by": "3fa85f64-5717-4562-b3fc-2c963f66afaz"
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_uom_with_empty_creator_id(client: TestClient):
    response = client.put(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38", json={
        "created_by": ""
    })

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["body", "created_by"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 0"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_delete_uom(client: TestClient):
    response = client.delete(f"{url_prefix}/8c935f60-2f3a-410a-9860-09bb2c270a38")

    assert response.status_code == 200
    assert response.json()["detail"] == "Id 8c935f60-2f3a-410a-9860-09bb2c270a38 as UOM is successfully deleted"

def test_delete_uom_by_wrong_id(client: TestClient):
    response = client.delete(f"{url_prefix}/db67b3f4-0e04-47bb-bc46-94826847ee4f")

    assert response.status_code == 404
    assert response.json()["detail"] == "Id db67b3f4-0e04-47bb-bc46-94826847ee4f as UOM is not found"
