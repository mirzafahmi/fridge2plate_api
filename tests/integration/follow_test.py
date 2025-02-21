from fastapi.testclient import TestClient

url_prefix = '/auth'
ADMIN_ID = "db67b3f4-0e04-47bb-bc46-94826847ee4f"

def test_post_follow_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/follow/0c619092-817e-4f73-b25f-8e187e69dded",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {ADMIN_ID} of user followed ID 0c619092-817e-4f73-b25f-8e187e69dded"

    user_following_list = client.get(f"{url_prefix}/following",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert user_following_list.status_code == 200

    following_list = user_following_list.json()["followings"]
    assert len(following_list) == 2

    assert following_list[0]['id'] == "0c619092-817e-4f73-b25f-8e187e69dded"
    assert following_list[0]['username'] == "second_user"
    assert following_list[0]['email'] == "test1@example.com"
    assert following_list[0]["cooked_count"] == 0
    assert following_list[0]["bookmarked_count"] == 0
    assert following_list[0]["liked_count"] == 0

    assert "created_date" in following_list[0]
    assert "updated_date" in following_list[0]

    assert following_list[1]['id'] == "799bb766-8ebe-4f51-a153-6e3c5530c3c2"
    assert following_list[1]['username'] == "third_user"
    assert following_list[1]['email'] == "test2@example.com"
    assert following_list[1]["cooked_count"] == 0
    assert following_list[1]["bookmarked_count"] == 0
    assert following_list[1]["liked_count"] == 0

    assert "created_date" in following_list[1]
    assert "updated_date" in following_list[1]

    follower_list = client.get(f"{url_prefix}/followers/0c619092-817e-4f73-b25f-8e187e69dded",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert follower_list.status_code == 200
    
    follower_list = follower_list.json()["followers"]
    assert len(follower_list) == 1

    assert follower_list[0]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert follower_list[0]['username'] == "testuser"
    assert follower_list[0]['email'] == "test@example.com"
    assert follower_list[0]["cooked_count"] == 0
    assert follower_list[0]["bookmarked_count"] == 0
    assert follower_list[0]["liked_count"] == 0

    assert "created_date" in follower_list[0]
    assert "updated_date" in follower_list[0]
    
def test_post_unfollow_action(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/follow/799bb766-8ebe-4f51-a153-6e3c5530c3c2",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {ADMIN_ID} of user unfollowed ID 799bb766-8ebe-4f51-a153-6e3c5530c3c2"

    user_following_list = client.get(f"{url_prefix}/following",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert user_following_list.status_code == 200

    following_list = user_following_list.json()["followings"]
    assert len(following_list) == 0

    follower_list = client.get(f"{url_prefix}/followers/799bb766-8ebe-4f51-a153-6e3c5530c3c2",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert follower_list.status_code == 200
    
    follower_list = follower_list.json()["followers"]
    assert len(follower_list) == 0

def test_post_toggle_follow_action_to_origin(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/follow/0c619092-817e-4f73-b25f-8e187e69dded",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {ADMIN_ID} of user followed ID 0c619092-817e-4f73-b25f-8e187e69dded"

    user_following_list = client.get(f"{url_prefix}/following",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert user_following_list.status_code == 200

    following_list = user_following_list.json()["followings"]
    assert len(following_list) == 2

    assert following_list[0]['id'] == "0c619092-817e-4f73-b25f-8e187e69dded"
    assert following_list[0]['username'] == "second_user"
    assert following_list[0]['email'] == "test1@example.com"
    assert following_list[0]["cooked_count"] == 0
    assert following_list[0]["bookmarked_count"] == 0
    assert following_list[0]["liked_count"] == 0

    assert "created_date" in following_list[0]
    assert "updated_date" in following_list[0]

    assert following_list[1]['id'] == "799bb766-8ebe-4f51-a153-6e3c5530c3c2"
    assert following_list[1]['username'] == "third_user"
    assert following_list[1]['email'] == "test2@example.com"
    assert following_list[1]["cooked_count"] == 0
    assert following_list[1]["bookmarked_count"] == 0
    assert following_list[1]["liked_count"] == 0

    assert "created_date" in following_list[1]
    assert "updated_date" in following_list[1]

    follower_list = client.get(f"{url_prefix}/followers/0c619092-817e-4f73-b25f-8e187e69dded",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert follower_list.status_code == 200
    
    follower_list = follower_list.json()["followers"]
    assert len(follower_list) == 1

    assert follower_list[0]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert follower_list[0]['username'] == "testuser"
    assert follower_list[0]['email'] == "test@example.com"
    assert follower_list[0]["cooked_count"] == 0
    assert follower_list[0]["bookmarked_count"] == 0
    assert follower_list[0]["liked_count"] == 0

    assert "created_date" in follower_list[0]
    assert "updated_date" in follower_list[0]

    response = client.post(f"{url_prefix}/follow/0c619092-817e-4f73-b25f-8e187e69dded",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {ADMIN_ID} of user unfollowed ID 0c619092-817e-4f73-b25f-8e187e69dded"

    user_following_list = client.get(f"{url_prefix}/following",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert user_following_list.status_code == 200

    following_list = user_following_list.json()["followings"]
    assert len(following_list) == 1

    assert following_list[0]['id'] == "799bb766-8ebe-4f51-a153-6e3c5530c3c2"
    assert following_list[0]['username'] == "third_user"
    assert following_list[0]['email'] == "test2@example.com"
    assert following_list[0]["cooked_count"] == 0
    assert following_list[0]["bookmarked_count"] == 0
    assert following_list[0]["liked_count"] == 0

    assert "created_date" in following_list[0]
    assert "updated_date" in following_list[0]

    follower_list = client.get(f"{url_prefix}/followers/0c619092-817e-4f73-b25f-8e187e69dded",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert follower_list.status_code == 200
    
    follower_list = follower_list.json()["followers"]
    assert len(follower_list) == 0

def test_post_toggle_unfollow_action_to_origin(client: TestClient, token: str):
    response = client.post(f"{url_prefix}/follow/799bb766-8ebe-4f51-a153-6e3c5530c3c2",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {ADMIN_ID} of user unfollowed ID 799bb766-8ebe-4f51-a153-6e3c5530c3c2"

    user_following_list = client.get(f"{url_prefix}/following",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert user_following_list.status_code == 200

    following_list = user_following_list.json()["followings"]
    assert len(following_list) == 0

    follower_list = client.get(f"{url_prefix}/followers/799bb766-8ebe-4f51-a153-6e3c5530c3c2",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert follower_list.status_code == 200
    
    follower_list = follower_list.json()["followers"]
    assert len(follower_list) == 0

    response = client.post(f"{url_prefix}/follow/799bb766-8ebe-4f51-a153-6e3c5530c3c2",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json()["detail"] == f"ID {ADMIN_ID} of user followed ID 799bb766-8ebe-4f51-a153-6e3c5530c3c2"

    user_following_list = client.get(f"{url_prefix}/following",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert user_following_list.status_code == 200

    following_list = user_following_list.json()["followings"]
    assert len(following_list) == 1

    assert following_list[0]['id'] == "799bb766-8ebe-4f51-a153-6e3c5530c3c2"
    assert following_list[0]['username'] == "third_user"
    assert following_list[0]['email'] == "test2@example.com"
    assert following_list[0]["cooked_count"] == 0
    assert following_list[0]["bookmarked_count"] == 0
    assert following_list[0]["liked_count"] == 0

    assert "created_date" in following_list[0]
    assert "updated_date" in following_list[0]

    follower_list = client.get(f"{url_prefix}/followers/799bb766-8ebe-4f51-a153-6e3c5530c3c2",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert follower_list.status_code == 200
    
    follower_list = follower_list.json()["followers"]
    assert len(follower_list) == 1

    assert follower_list[0]['id'] == "db67b3f4-0e04-47bb-bc46-94826847ee4f"
    assert follower_list[0]['username'] == "testuser"
    assert follower_list[0]['email'] == "test@example.com"
    assert follower_list[0]["cooked_count"] == 0
    assert follower_list[0]["bookmarked_count"] == 0
    assert follower_list[0]["liked_count"] == 0

    assert "created_date" in follower_list[0]
    assert "updated_date" in follower_list[0]