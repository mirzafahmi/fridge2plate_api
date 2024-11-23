from dotenv import load_dotenv
import os
import uuid

from db.db_setup import get_db
from utils.recipe import post_recipe
from pydantic_schemas.recipe import RecipeCreate

recipes = [
    {
        "name": "Ayam masak lemak cili padi",
        "serving": "4-5",
        "cooking_time": "30 minutes",
        "recipe_category_id": "949defd8-d47b-4b0e-b846-163f9936f8e7",
        "recipe_origin_id": "c9212804-4208-4464-9c18-225bc465e957",
        "recipe_tags": [
            "4431d379-fe77-4a6c-9ede-d52de9d939de", 
            "af9228b3-aa8a-4e2b-82eb-2782e59603ee"
        ],
        "ingredients":[
            {
                "ingredient_id": "53bef429-f7a8-432f-80c4-0d06e42e4930",
                "quantity": 3,
                "uom_id": "7b3a717b-a011-41e9-a818-348e92140b3a",
                "is_essential": True
            },
            {
                "ingredient_id": "09bebf2e-c6df-4edc-8764-ee57c6707f7b",
                "quantity": 3,
                "uom_id": "7b3a717b-a011-41e9-a818-348e92140b3a",
                "is_essential": False
            }
        ],
        "steps": [
            {
                "step_number": 1,
                "description": "potong ayam"
            },
            {
                "step_number": 2,
                "description": "potong lobak"
            },
            {
                "step_number": 3,
                "description": "masak"
            }
        ],
    },
    {
        "name": "test",
        "serving": "1-2",
        "cooking_time": "45 minutes",
        "recipe_category_id": "949defd8-d47b-4b0e-b846-163f9936f8e7",
        "recipe_origin_id": "c9212804-4208-4464-9c18-225bc465e957",
        "recipe_tags": [
            "4431d379-fe77-4a6c-9ede-d52de9d939de", 
            "af9228b3-aa8a-4e2b-82eb-2782e59603ee"
        ],
        "ingredients": [
            {
                "ingredient_id": "53bef429-f7a8-432f-80c4-0d06e42e4930",
                "quantity": 2,
                "uom_id": "7b3a717b-a011-41e9-a818-348e92140b3a",
                "is_essential": True
            },
            {
                "ingredient_id": "09bebf2e-c6df-4edc-8764-ee57c6707f7b",
                "quantity": 1,
                "uom_id": "7b3a717b-a011-41e9-a818-348e92140b3a",
                "is_essential": True
            }
        ],
        "steps": [
            {
                "step_number": 1,
                "description": "potong ayam"
            },
            {
                "step_number": 2,
                "description": "potong lobak"
            }
        ],
    },
]

def seed_recipe_data():
    db = next(get_db())

    for recipe in recipes:
        try:
            recipe_data = RecipeCreate(**recipe)
            created_recipe = post_recipe(db, recipe_data)

            print(f'recipe data of {created_recipe.name} has been added to the database.')
        
        except Exception as e:
            print(f'Seeding process failed: {e}')
            continue
    
        db.close()

    print('Seeding process for recipe db is completed')

if __name__ == "__main__":
    seed_recipe_data()