from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func, asc
from uuid import UUID
from fastapi import HTTPException, status

from db.models.recipe import RecipeCategory, Recipe
from pydantic_schemas.recipe_category import RecipeCategoryCreate, RecipeCategoryUpdate


def get_recipe_categories(db: Session, skip: int=0, limit: int = 100):
    return db.query(RecipeCategory).order_by(asc(RecipeCategory.name)).offset(skip).limit(limit).all()

def get_recipe_category_by_id(db: Session, recipe_category_id: UUID):
    return db.query(RecipeCategory).filter(RecipeCategory.id == recipe_category_id).first()

def get_recipe_category_by_name(db: Session, recipe_category_name: str):
    return db.query(RecipeCategory).filter(RecipeCategory.name == recipe_category_name).first()

def check_unique_recipe_category_name(db: Session, recipe_category_name: str):
    return db.query(RecipeCategory).filter(func.lower(RecipeCategory.name) == func.lower(recipe_category_name)).first()

def post_recipe_category(db: Session, recipe_category: RecipeCategoryCreate):
    recipe_category_data = {key: value for key, value in recipe_category.dict().items() if value is not None}
    db_recipe_category = RecipeCategory(**recipe_category_data)

    db.add(db_recipe_category)
    db.commit()
    db.refresh(db_recipe_category)

    return db_recipe_category

def put_recipe_category(db: Session, recipe_category_id: UUID, recipe_category: RecipeCategoryUpdate):
    db_recipe_category = get_recipe_category_by_id(db, recipe_category_id)
    
    if db_recipe_category:
        if recipe_category:
            if recipe_category.name and recipe_category.name != db_recipe_category.name:
                if check_unique_recipe_category_name(db, recipe_category.name):
                    raise HTTPException(
                        status_code=400, 
                        detail=f"'{recipe_category.name}' as Recipe Category is already registered"
                    )
            for key, value in recipe_category.dict().items():
                if value is not None:
                    setattr(db_recipe_category, key, value)

        db.commit()
        db.refresh(db_recipe_category)

        return db_recipe_category
    else:
        raise HTTPException(status_code=404, detail=f"Recipe Category with name {recipe_category_name} not found")

def delete_recipe_category(db: Session, recipe_category_id: UUID):
    db_recipe_category = get_recipe_category_by_id(db, recipe_category_id)
    
    db.query(Recipe).filter(Recipe.recipe_category_id == db_recipe_category.id).update({
        Recipe.recipe_category_id: None
    })

    db.commit()

    db.delete(db_recipe_category)
    db.commit()