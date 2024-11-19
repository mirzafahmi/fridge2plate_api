from fastapi.testclient import TestClient


url_prefix = '/ingredient_categories/'

def test_get_category_list(client: TestClient):
    response = client.get(f"{url_prefix }")

    assert response.status_code == 200

    ingredient_categories = response.json()

    assert isinstance(ingredient_categories, list)
    assert len(ingredient_categories) == 2