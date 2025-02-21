from dotenv import load_dotenv
import os
import uuid
from faker import Faker

from db.db_setup import get_db
from utils.user import post_user
from pydantic_schemas.user import UserCreateSeeder


load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")

fake = Faker()
NUM_USERS = 10 

users = [
    {
        'id': ADMIN_ID,
        'username': 'admin',
        'email': 'seed@gmail.com',
        'password': 'test123'
    },
    {
        'username': 'tests',
        'email': 'test@gmail.com',
        'password': 'test123'
    },
]

for _ in range(NUM_USERS):
    users.append({
        'username': fake.user_name(),
        'email': fake.email(),
        'password': 'test123'
    })

def seed_user_data():
    db = next(get_db())

    for user in users:
        try:
            user_data = UserCreateSeeder(**user)
            created_user = post_user(db, user_data)

            print(f'user data of {created_user.username} has been added to the database.')
        
        except Exception as e:
            print(f'Seeding process failed: {e}')
            continue
    
    db.close()

    print('Seeding process for user db is completed')

if __name__ == "__main__":
    seed_user_data()