from dotenv import load_dotenv
import os
import uuid

from db.db_setup import get_db
from utils.recipe_tag import post_recipe_tag
from pydantic_schemas.recipe_tag import RecipeTagCreateSeeder


recipe_tags = [
    {
        'id': '4431d379-fe77-4a6c-9ede-d52de9d939de',
        'name': 'breakfast',
    },
    {
        'id': 'af9228b3-aa8a-4e2b-82eb-2782e59603ee',
        'name': 'lunch',
    },
    {
        'id': 'ef91c1a0-753f-4db1-a04d-3fe3b5496f7a',
        'name': 'brunch',
    },
    {
        'id': 'cb38e39d-251c-47a3-93e1-f21850d8904c',
        'name': 'dinner',
    },
    {
        'id': '7cb716fd-f2b5-4c98-b2b2-6f8b0a596998',
        'name': 'supper',
    },
    {
        'id': '592cfc6d-6c47-4ebb-84b0-ea43ffd19635',
        'name': 'eid',
    },
]

def seed_recipe_tag_data():
    db = next(get_db())

    for recipe_tag in recipe_tags:
        try:
            recipe_tag_data = RecipeTagCreateSeeder(**recipe_tag)
            created_recipe_tag = post_recipe_tag(db, recipe_tag_data )

            print(f'Recipe tag data of {created_recipe_tag.name} has been added to the database.')
        
        except Exception as e:
            print(f'Seeding process failed: {e}')
            continue
    
    db.close()

    print('Seeding process for recipe tags db is completed')

if __name__ == "__main__":
    seed_recipe_tag_data()