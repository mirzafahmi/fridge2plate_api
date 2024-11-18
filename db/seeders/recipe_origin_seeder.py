from dotenv import load_dotenv
import os
import uuid

from db.db_setup import get_db
from utils.recipe_origin import post_recipe_origin
from pydantic_schemas.recipe_origin import RecipeOriginCreateSeeder


recipe_origins = [
    {
        'id': 'c9212804-4208-4464-9c18-225bc465e957',
        'name': 'malayian',
    },
    {
        'id': 'f5ab1ae4-0849-4b70-b2f9-00eb3710a370',
        'name': 'indian',
    },
    {
        'id': 'e8636a8f-7f0a-4cbd-9ecc-51a88c61985a',
        'name': 'chinese',
    },
    {
        'id': '6ee5c918-5dcf-45f9-8763-1114a869321d',
        'name': 'indonesian',
    },
    {
        'id': '02aee2d5-7697-4676-b511-21576a1340a8',
        'name': 'italian',
    },
    {
        'id': '4c87da56-4919-4769-850f-3392ff9cf842',
        'name': 'thai',
    },
    {
        'id': 'a500a5eb-f390-47e6-a0b4-5f95d7754031',
        'name': 'vietnamese',
    },
]

def seed_recipe_origin_data():
    db = next(get_db())

    for recipe_origin in recipe_origins:
        try:
            recipe_origin_data = RecipeOriginCreateSeeder(**recipe_origin)
            created_recipe_origin = post_recipe_origin(db, recipe_origin_data )

            print(f'Recipe origin data of {created_recipe_origin.name} has been added to the database.')
        
        except Exception as e:
            print(f'Seeding process failed: {e}')
            continue
    
    db.close()

    print('Seeding process for recipe origins db is completed')

if __name__ == "__main__":
    seed_recipe_origin_data()