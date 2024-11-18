from dotenv import load_dotenv
import os
import uuid

from db.db_setup import get_db
from utils.ingredient import post_ingredient
from pydantic_schemas.ingredient import IngredientCreateSeeder

storage_url = 'static/ingredient/'

ingredients = [
    {
        'id': '53bef429-f7a8-432f-80c4-0d06e42e4930',
        'name': 'chicken',
        'brand': 'chicken',
        'icon': f'{storage_url}ayam.svg',
        'ingredient_category_id': 'b4b165f6-a4f2-45f6-bda6-0a49092d3f03'
    },
    {
        'id': '0ad73f6f-eb7d-40a6-98d2-170f1dbec18c',
        'name': 'fish',
        'brand': 'fish',
        'icon': f'{storage_url}fish.svg',
        'ingredient_category_id': 'b4b165f6-a4f2-45f6-bda6-0a49092d3f03'
    },
    {
        'id': '09bebf2e-c6df-4edc-8764-ee57c6707f7b',
        'name': 'carrot',
        'brand': 'carrot',
        'icon': f'{storage_url}lobak.svg',
        'ingredient_category_id': '6722eb62-884a-4208-8596-ed82d310e832'
    },
    {
        'id': '10700cfd-44d2-47dd-9fd1-efcce913dcff',
        'name': 'tomato',
        'brand': 'tomato',
        'icon': f'{storage_url}tomato.svg',
        'ingredient_category_id': '6722eb62-884a-4208-8596-ed82d310e832'
    },
]

def seed_ingredient_data():
    db = next(get_db())

    for ingredient in ingredients:
        try:
            ingredient_data = IngredientCreateSeeder(**ingredient)
            created_ingredient = post_ingredient(db, ingredient_data )

            print(f'Ingredient data of {created_ingredient.name} has been added to the database.')
        
        except Exception as e:
            print(f'Seeding process failed: {e}')
            continue
    
    db.close()

    print('Seeding process for ingredient db is completed')

if __name__ == "__main__":
    seed_ingredient_data()