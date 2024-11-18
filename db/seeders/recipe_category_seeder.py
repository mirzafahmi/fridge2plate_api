from dotenv import load_dotenv
import os
import uuid

from db.db_setup import get_db
from utils.recipe_category import post_recipe_category
from pydantic_schemas.recipe_category import RecipeCategoryCreateSeeder


recipe_categories = [
    {
        'id': '439cc2b6-1acb-4b02-a15b-67f1f4fe9bef',
        'name': 'breakfast'
    },
    {
        'id': '949defd8-d47b-4b0e-b846-163f9936f8e7',
        'name': 'lunch'
    },
    {
        'id': '813bd870-eadc-4566-b390-a92c202d262d',
        'name': 'dinner'
    },
]

def seed_recipe_category_data():
    db = next(get_db())

    for recipe_category in recipe_categories:
        try:
            recipe_category_data = RecipeCategoryCreateSeeder(**recipe_category)
            created_recipe_category = post_recipe_category(db, recipe_category_data )

            print(f'Recipe category data of {created_recipe_category.name} has been added to the database.')
        
        except Exception as e:
            print(f'Seeding process failed: {e}')
            continue
    
    db.close()

    print('Seeding process for recipe category db is completed')

if __name__ == "__main__":
    seed_data()