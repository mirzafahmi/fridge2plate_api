from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func, asc
from uuid import UUID
from fastapi import HTTPException
import os
from dotenv import load_dotenv

from db.models.recipe import Recipe, RecipeTagRecipeAssociation, Instruction, Ingredient, IngredientRecipeAssociation, RecipeImage
from pydantic_schemas.recipe import RecipeCreate, RecipeUpdate
from utils.recipe_category import get_recipe_category_by_name
from utils.recipe_tag import get_recipe_tag_by_name
from utils.recipe_origin import get_recipe_origin_by_name


load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")

def get_recipes(db: Session, skip: int=0, limit: int = 100):
    return db.query(Recipe).offset(skip).limit(limit).all()

def get_recipe_by_id(db: Session, recipe_id: UUID):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()

def get_recipe_by_name(db: Session, recipe_name: str):
    return db.query(Recipe).filter(Recipe.name == recipe_name).first()

def post_recipe(db: Session, recipe_data):
    try:
        db_recipe = Recipe(
            name=recipe_data.name,
            serving=recipe_data.serving,
            cooking_time=recipe_data.cooking_time,
            recipe_category_id=recipe_data.recipe_category_id,
            recipe_origin_id=recipe_data.recipe_origin_id,
            created_by=recipe_data.created_by if recipe_data.created_by else ADMIN_ID #if error related to uuid
        )
        db.add(db_recipe)
        db.flush() 

        for tag_id in recipe_data.recipe_tags:
            recipe_tag_association = RecipeTagRecipeAssociation(
                recipe_id=db_recipe.id, 
                recipe_tag_id=tag_id
            )
            db.add(recipe_tag_association)

        for ingredient in recipe_data.ingredients:
            ingredient_recipe_association = IngredientRecipeAssociation(
                ingredient_id=ingredient.ingredient_id, 
                recipe_id=db_recipe.id,
                uom_id=ingredient.uom_id,
                quantity=ingredient.quantity,
                is_essential=ingredient.is_essential
            )
            db.add(ingredient_recipe_association)

        for instruction in recipe_data.steps:
            instruction_model = Instruction(
                step_number=instruction.step_number,
                description=instruction.description,
                recipe_id=db_recipe.id
            )
            db.add(instruction_model)
        #issue with images test with seeder too
        if recipe_data.images:
            for image in recipe_data.images:
                recipe_image_model = RecipeImage(
                    image=image,
                    recipe_id=db_recipe.id
                )
                db.add(recipe_image_model)
        db.commit()
        db.refresh(db_recipe)
        return db_recipe

    except Exception as e:
        raise RuntimeError(f"Failed to create recipe: {e}")

def update_recipe(db: Session, recipe_id: UUID, recipe: RecipeUpdate):
    db_recipe = get_recipe_by_id(db, recipe_id)

    if db_recipe:
        for key, value in recipe.dict().items():
            if value is not None:
                setattr(db_recipe, key, value)

        db.commit()
        db.refresh(db_recipe)
        
    return db_recipe

def delete_recipe(db: Session, recipe_id: UUID):
    db_recipe = get_recipe_by_id(db, recipe_id)
    db.delete(db_recipe)
    db.commit()