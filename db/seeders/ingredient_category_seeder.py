from dotenv import load_dotenv
import os
import uuid

from db.db_setup import get_db
from utils.ingredient_category import post_ingredient_category
from pydantic_schemas.ingredient_category import IngredientCategoryCreateSeeder


ingredient_categories = [
    {
        'id': 'b4b165f6-a4f2-45f6-bda6-0a49092d3f03',
        'name': 'proteins & meat'
    },
    {
        'id': '6722eb62-884a-4208-8596-ed82d310e832',
        'name': 'vegetables'
    },
    {
        'id': '5592db88-7059-4c97-8a6e-82817144bb31',
        'name': 'grains & starches'
    },
    {
        'id': '5c56349b-a5fb-4d10-ba77-a6362a8c6b88',
        'name': 'dairy'
    },
    {
        'id': '2ad5eb58-5753-4de3-b090-1c44baf671eb',
        'name': 'condiments & sauces'
    },
    {
        "name": "fruits"
    },
    {
        "name": "legumes & beans"
    },
    {
        "name": "nuts & seeds"
    },
    {
        "name": "herb & spices"
    },
    {
        "name": "oil & fats"
    },
    {
        "name": "sweeteners & sugars"
    },
    {
        "name": "canned & preserved goods"
    },
    {
        "name": "miscellaneous"
    }
]

def seed_ingredient_category_data():
    db = next(get_db())

    for ingredient_category in ingredient_categories:
        try:
            ingredient_category_data = IngredientCategoryCreateSeeder(**ingredient_category)
            created_ingredient_category = post_ingredient_category(db, ingredient_category_data)

            print(f'Ingredient category data of {created_ingredient_category.name} has been added to the database.')
        
        except Exception as e:
            print(f'Seeding process failed: {e}')
            continue
    
    db.close()

    print('Seeding process for ingredient category db is completed')

if __name__ == "__main__":
    seed_ingredient_category_data()