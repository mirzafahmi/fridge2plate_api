from fastapi.testclient import TestClient
import pytest
from uuid import UUID

url_prefix = '/recipe_instructions'

@pytest.fixture
def recipe_instruction_id(client: TestClient, token:str):
    recipe_instruction_id = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        headers={"Authorization": f"Bearer {token}"}
    ).json()["instructions"][0]["id"]

    return recipe_instruction_id

def test_get_recipe_instruction_list(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Instruction list is retrieved successfully"

    instructions = response.json()['instructions']
    
    assert isinstance(instructions, list)
    assert len(instructions) == 5

    assert instructions[0]["step_number"] == 1
    assert instructions[0]["description"] == "potong ayam"
    assert instructions[0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert instructions[1]["step_number"] == 2
    assert instructions[1]["description"] == "potong lobak"
    assert instructions[1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert instructions[2]["step_number"] == 3
    assert instructions[2]["description"] == "masak"
    assert instructions[2]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert instructions[3]["step_number"] == 1
    assert instructions[3]["description"] == "potong ayam"
    assert instructions[3]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

    assert instructions[4]["step_number"] == 2
    assert instructions[4]["description"] == "potong lobak"
    assert instructions[4]["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

def test_get_recipe_instruction_list_with_invalid_token(client: TestClient):
    response = client.get(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_recipe_instruction_list_without_token(client: TestClient):
    response = client.get(f"{url_prefix}/"
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_recipe_instruction_by_id(client: TestClient, recipe_instruction_id: UUID, token: str):
    response = client.get(f"{url_prefix}/{recipe_instruction_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )

    instruction = response.json()['instruction']

    assert instruction["step_number"] == 1
    assert instruction["description"] == "potong ayam"
    assert instruction["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

def test_get_recipe_instruction_by_id_with_invalid_token(client: TestClient, recipe_instruction_id: UUID, token: str):
    response = client.get(f"{url_prefix}/{recipe_instruction_id}", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_get_recipe_instruction_by_id_without_token(client: TestClient, recipe_instruction_id: UUID, token: str):
    response = client.get(f"{url_prefix}/{recipe_instruction_id}"
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_get_recipe_instruction_by_wrong_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d376338", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == f"ID 6b86885b-a613-4ca6-a9b7-584c3d376338 as Instruction is not found"

def test_get_recipe_instruction_by_invalid_id(client: TestClient, token: str):
    response = client.get(f"{url_prefix}/6b86885b-a613-4ca6-a9b7-584c3d37633z", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "instruction_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_post_recipe_instruction(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": 3,
            "description": "test instruction",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    assert response.json()["detail"] == "test instruction instruction as step number 3 of Instruction is created successfully for ID 6b86885b-a613-4ca6-a9b7-584c3d376337 of Recipe"

    instruction = response.json()['instruction']

    assert instruction["step_number"] == 3
    assert instruction["description"] == "test instruction"
    assert instruction["recipe_id"] == "6b86885b-a613-4ca6-a9b7-584c3d376337"

def test_post_recipe_instruction_with_invalid_token(client: TestClient):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": 3,
            "description": "test instruction",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        },
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_post_recipe_instruction_without_token(client: TestClient):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": 3,
            "description": "test instruction",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_post_recipe_instruction_with_duplicate_step_number(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": 2,
            "description": "test instruction",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Step number 2 of Instruction for ID 6b86885b-a613-4ca6-a9b7-584c3d376337 of Recipe is already registered"

def test_post_recipe_instruction_with_skipped_step_number(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": 4,
            "description": "test instruction",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 409
    assert response.json()["detail"] == "Step number 4 is invalid. The next step should be 3."

def test_post_recipe_instruction_with_negative_step_number(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": -4,
            "description": "test instruction",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'step_number']
    assert response_json["msg"]  == "Value error, step_number must be a positive integer"
    assert response_json["type"] == "value_error"

def test_post_recipe_instruction_with_invalid_step_number(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": "",
            "description": "test instruction",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'step_number']
    assert response_json["msg"]  == "Input should be a valid integer, unable to parse string as an integer"
    assert response_json["type"] == "int_parsing"

def test_post_recipe_instruction_without_step_number(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "description": "test instruction",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'step_number']
    assert response_json["msg"]  == "Field required"
    assert response_json["type"] == "missing"

def test_post_recipe_instruction_with_empty_description(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": "3",
            "description": "",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422
    
    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'description']
    assert response_json["msg"]  == "String should have at least 3 characters"
    assert response_json["type"] == "string_too_short"

def test_post_recipe_instruction_without_description(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": "3",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376337"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()["detail"][0]

    assert response_json["loc"] == ['body', 'description']
    assert response_json["msg"]  == "Field required"
    assert response_json["type"] == "missing"

def test_post_recipe_instruction_with_wrong_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": 3,
            "description": "test instruction",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d376338"
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ID 6b86885b-a613-4ca6-a9b7-584c3d376338 as Recipe is not found"

def test_post_recipe_instruction_with_invalid_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": 3,
            "description": "test instruction",
            "recipe_id": "6b86885b-a613-4ca6-a9b7-584c3d37633z"
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

def test_post_recipe_instruction_with_empty_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": 3,
            "description": "test instruction",
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

def test_post_recipe_instruction_without_recipe_id(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/", 
        json={
            "step_number": 3,
            "description": "test instruction"
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

def test_put_recipe_instruction_by_changing_description(client: TestClient, recipe_instruction_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_instruction_id}", 
        json={
            "description": "test instruction"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 202
    assert response.json()["detail"] == f"ID {recipe_instruction_id} of Instruction is updated successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    instruction = response.json()["instruction"]
    
    assert instruction["id"] == recipe_instruction_id
    assert instruction["step_number"] == 1
    assert instruction["description"] == "test instruction"
    assert instruction["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"
    
    instructions_by_recipe_id_response = client.get(f"{url_prefix}/by_recipe_id/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    instructions = instructions_by_recipe_id_response.json()["instructions"]

    assert instructions_by_recipe_id_response.status_code == 200

    assert instructions[0]["step_number"] == 1
    assert instructions[0]["description"] == "test instruction"
    assert instructions[0]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert instructions[1]["step_number"] == 2
    assert instructions[1]["description"] == "potong lobak"
    assert instructions[1]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

    assert instructions[2]["step_number"] == 3
    assert instructions[2]["description"] == "masak"
    assert instructions[2]["recipe_id"] == "2cdd1a37-9c45-4202-a38c-026686b0ff71"

def test_put_recipe_instruction_by_changing_description_with_invalid_token(client: TestClient, recipe_instruction_id: UUID):
    response = client.put(f"{url_prefix}/{recipe_instruction_id}", 
        json={
            "description": "test instruction"
        },
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_put_recipe_instruction_by_changing_description(client: TestClient, recipe_instruction_id: UUID):
    response = client.put(f"{url_prefix}/{recipe_instruction_id}", 
        json={
            "description": "test instruction"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_put_recipe_instruction_with_empty_description(client: TestClient, recipe_instruction_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_instruction_id}", 
        json={
            "description": "",
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

def test_put_recipe_instruction_without_description(client: TestClient, recipe_instruction_id: UUID, token: str):
    response = client.put(f"{url_prefix}/{recipe_instruction_id}", 
        json={},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1

    assert response_json["detail"][0]["loc"] == ["body", "description"]
    assert response_json["detail"][0]["msg"] == "Field required"
    assert response_json["detail"][0]["type"] == "missing"

def test_put_recipe_instruction_with_wrong_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        json={
            "description": "test update instruction",
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 404
    assert response.json()["detail"] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 as Instruction is not found"

def test_put_recipe_instruction_with_invalid_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff7z", 
        json={
            "description": "test update instruction",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "instruction_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_put_recipe_instruction_without_id(client: TestClient, token: str):
    response = client.put(f"{url_prefix}/", 
        json={
            "description": "test update instruction",
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 405
    assert response.json()["detail"] == f"Method Not Allowed"

def test_delete_recipe_instruction(client: TestClient, recipe_instruction_id: UUID, token: str):
    response = client.delete(f"{url_prefix}/{recipe_instruction_id}", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {recipe_instruction_id} as Instruction is deleted successfully for ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 of Recipe"

    instruction_response = client.get(f"{url_prefix}/{recipe_instruction_id}")
    
    assert instruction_response.status_code == 404
    assert instruction_response.json()["detail"] == f"ID {recipe_instruction_id} as Instruction is not found"

def test_delete_recipe_instruction(client: TestClient, recipe_instruction_id: UUID):
    response = client.delete(f"{url_prefix}/{recipe_instruction_id}", 
        headers={"Authorization": f"Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_delete_recipe_instruction(client: TestClient, recipe_instruction_id: UUID):
    response = client.delete(f"{url_prefix}/{recipe_instruction_id}"
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_delete_recipe_instruction_with_wrong_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff71", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "ID 2cdd1a37-9c45-4202-a38c-026686b0ff71 as Instruction is not found"

def test_delete_recipe_instruction_with_invalid_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/2cdd1a37-9c45-4202-a38c-026686b0ff7z", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422

    response_json = response.json()

    assert response_json["detail"] is not None
    assert len(response_json["detail"]) == 1
    
    assert response_json["detail"][0]["loc"] == ["path", "instruction_id"]
    assert response_json["detail"][0]["msg"] == "Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `z` at 36"
    assert response_json["detail"][0]["type"] == "uuid_parsing"

def test_delete_recipe_instruction_without_id(client: TestClient, token: str):
    response = client.delete(f"{url_prefix}/", 
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 405
    assert response.json()["detail"] == f"Method Not Allowed"