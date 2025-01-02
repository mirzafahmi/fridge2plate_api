from dotenv import load_dotenv
import os
import uuid

from db.db_setup import get_db
from utils.badge import post_badge
from pydantic_schemas.badge import BadgeCreateSeeder

def generate_image_path(name):
    return f"badge_{name.lower().replace(' ', '_')}.png"

badges = [
    {
        'id': '3afb1e3d-617e-41f8-b140-b6a5fd876446',
        'name': 'Getting Started',
        'description': "Created at least 1 recipe",
    },
    {
        'id': '52518fea-cae4-4a79-abf4-65cb8a122f16',
        'name': 'Veteran',
        'description': "Created at least 5 recipe",
    },
    {
        'id': '6446f1e0-fd4a-455e-a9d0-e77c8c059140',
        'name': 'Community Leader',
        'description': "Reached at least 5 follower",
    },
    {
        'id': 'a554c4b7-c843-4ed0-bb68-c0f71f508ec7',
        'name': 'Enthusiast',
        'description': "Have at least 4 preferred recipe category",
    },
    {
        'id': 'ce668760-0c4c-4859-9f61-691853584f68',
        'name': 'Versatile',
        'description': "Created at least 4 recipe in any recipe origin",
    },
    {
        'id': '897b194c-b2c7-414b-8ec4-30af5c3dde7b',
        'name': 'Social Butterfly',
        'description': "Commented at least 5 comments",
    },
]

badges = [
    {**badge, 'image': generate_image_path(badge['name'])} for badge in badges
]

def seed_badge_data():
    db = next(get_db())

    for badge in badges:
        try:
            badge_data = BadgeCreateSeeder(**badge)
            created_badge = post_badge(db, badge_data)

            print(f'Badge data of {created_badge.name} has been added to the database.')
        
        except Exception as e:
            print(f'Seeding process failed: {e}')
            continue
    
    db.close()

    print('Seeding process for badge db is completed')

if __name__ == "__main__":
    seed_badge_data()