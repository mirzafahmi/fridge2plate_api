from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func, asc
from uuid import UUID, uuid4
from fastapi import HTTPException
import os
from dotenv import load_dotenv

from db.models.recipe import Recipe, RecipeTagRecipeAssociation, RecipeInstruction, Ingredient, IngredientRecipeAssociation, RecipeImage, RecipeTip
from pydantic_schemas.recipe import RecipeCreate, RecipeUpdate
from utils.recipe_category import get_recipe_category_by_name
from utils.recipe_tag import get_recipe_tag_by_name
from utils.recipe_origin import get_recipe_origin_by_name
from utils.instruction import validate_step_number


load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")

def get_recipes(db: Session, skip: int=0, limit: int = 100):
    return db.query(Recipe).offset(skip).limit(limit).all()

def get_recipe_by_id(db: Session, recipe_id: UUID):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()

def get_recipe_by_name(db: Session, recipe_name: str):
    return db.query(Recipe).filter(Recipe.name == recipe_name).first()

def post_recipe(db: Session, recipe_data: RecipeCreate):
    try:
        db_recipe = Recipe(
            id=recipe_data.id if hasattr(recipe_data, 'id') and recipe_data.id is not None else uuid4(),
            name=recipe_data.name,
            serving=recipe_data.serving,
            cooking_time=recipe_data.cooking_time,
            recipe_category_id=recipe_data.recipe_category_id,
            recipe_origin_id=recipe_data.recipe_origin_id,
            created_by=recipe_data.created_by if recipe_data.created_by else UUID(ADMIN_ID) #if error related to uuid
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

        for instruction in sorted(recipe_data.steps, key=lambda x: x.step_number): #could cause error in test
            validate_step_number(db, db_recipe.id, instruction.step_number)
            instruction_model = RecipeInstruction(
                step_number=instruction.step_number,
                description=instruction.description,
                recipe_id=db_recipe.id,
            )
            db.add(instruction_model)
            db.flush() #need to make the instance accessible for next iter
        
        if recipe_data.images:
            for image in recipe_data.images:
                recipe_image_model = RecipeImage(
                    image=image,
                    recipe_id=db_recipe.id,
                )
                db.add(recipe_image_model)
        
        if recipe_data.tips:
            for tip in recipe_data.tips:
                recipe_tip_model = RecipeTip(
                    description=tip,
                    recipe_id=db_recipe.id,
                )
                db.add(recipe_tip_model)
        db.commit()
        db.refresh(db_recipe)
        
        return db_recipe

    except Exception as e:
        raise RuntimeError(f"Failed to create recipe: {e}")

def put_recipe(db: Session, recipe_id: UUID, recipe_data: RecipeUpdate):
    try:
        # Retrieve the existing recipe
        db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
        if not db_recipe:
            raise ValueError(f"ID {recipe_id} of recipe is not found")

        # Update main recipe fields
        if hasattr(recipe_data, 'name') and recipe_data.name is not None:
            db_recipe.name = recipe_data.name

        if hasattr(recipe_data, 'serving') and recipe_data.serving is not None:
            db_recipe.serving = recipe_data.serving

        if hasattr(recipe_data, 'cooking_time') and recipe_data.cooking_time is not None:
            db_recipe.cooking_time = recipe_data.cooking_time

        if hasattr(recipe_data, 'recipe_category_id') and recipe_data.recipe_category_id is not None:
            db_recipe.recipe_category_id = recipe_data.recipe_category_id

        if hasattr(recipe_data, 'recipe_origin_id') and recipe_data.recipe_origin_id is not None:
            db_recipe.recipe_origin_id = recipe_data.recipe_origin_id

        if hasattr(recipe_data, 'created_by') and recipe_data.created_by is not None:
            db_recipe.created_by = recipe_data.created_by

        if hasattr(recipe_data, 'recipe_tags') and recipe_data.recipe_tags is not None:
            existing_tag_ids = {tag.recipe_tag_id for tag in db_recipe.recipe_tag_recipe_associations}
            new_tag_ids = set(recipe_data.recipe_tags)

            # Remove tags not in the new data
            for tag_id in existing_tag_ids - new_tag_ids:
                db.query(RecipeTagRecipeAssociation).filter_by(recipe_id=recipe_id, recipe_tag_id=tag_id).delete()

            # Add new tags
            for tag_id in new_tag_ids - existing_tag_ids:
                recipe_tag_association = RecipeTagRecipeAssociation(
                    recipe_id=recipe_id,
                    recipe_tag_id=tag_id
                )
                db.add(recipe_tag_association)
        
        if hasattr(recipe_data, 'ingredients') and recipe_data.ingredients is not None:
            existing_ingredient_associations = {assoc.ingredient_id: assoc for assoc in db_recipe.ingredient_recipe_associations}
            new_ingredients = {ingredient.ingredient_id: ingredient for ingredient in recipe_data.ingredients}

            # Remove ingredients not in the new data
            for ingredient_id in set(existing_ingredient_associations) - set(new_ingredients):
                db.query(IngredientRecipeAssociation).filter_by(recipe_id=recipe_id, ingredient_id=ingredient_id).delete()

            # Update or add new ingredients
            for ingredient_id, ingredient in new_ingredients.items():
                if ingredient_id in existing_ingredient_associations:
                    # Update existing association
                    assoc = existing_ingredient_associations[ingredient_id]
                    if hasattr(ingredient, 'uom_id') and ingredient.uom_id is not None:
                        assoc.uom_id = ingredient.uom_id
                    if hasattr(ingredient, 'quantity') and ingredient.quantity is not None:
                        assoc.quantity = ingredient.quantity
                    if hasattr(ingredient, 'is_essential') and ingredient.is_essential is not None:
                        assoc.is_essential = ingredient.is_essential
                else:
                    # Add new association
                    ingredient_recipe_association = IngredientRecipeAssociation(
                        ingredient_id=ingredient_id,
                        recipe_id=recipe_id,
                        uom_id=ingredient.uom_id,
                        quantity=ingredient.quantity,
                        is_essential=ingredient.is_essential
                    )
                    db.add(ingredient_recipe_association)

        #caused by created_by, use pydantic schemas in utils
        if hasattr(recipe_data, 'steps') and recipe_data.steps is not None:
            db.query(RecipeInstruction).filter_by(recipe_id=recipe_id).delete()
            
            for instruction in recipe_data.steps:
                instruction_model = RecipeInstruction(
                    step_number=instruction.step_number,
                    description=instruction.description,
                    recipe_id=recipe_id
                )
                db.add(instruction_model)

        #TODO! convert images as list of str not as list of recipeimage obj
        if hasattr(recipe_data, 'images') and recipe_data.images is not None:
            db.query(RecipeImage).filter_by(recipe_id=recipe_id).delete()
            for image in recipe_data.images:
                recipe_image_model = RecipeImage(
                    image=image,
                    recipe_id=recipe_id
                )
                db.add(recipe_image_model)

        db.commit()
        db.refresh(db_recipe)
        
        return db_recipe

    except Exception as e:
        db.rollback()  # Rollback in case of an error
        raise RuntimeError(f"Failed to update recipe: {e}")

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