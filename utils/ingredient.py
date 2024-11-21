from sqlalchemy.orm import Session, joinedload
from typing import Optional
from sqlalchemy import func, asc
from uuid import UUID
from fastapi import HTTPException

from db.models.recipe import Ingredient, IngredientCategory
from pydantic_schemas.ingredient import IngredientCreate, IngredientUpdate
from utils.ingredient_category import get_ingredient_category_by_name


def get_ingredients(db: Session, skip: int=0, limit: int = 100):
    return db.query(Ingredient).order_by(asc(Ingredient.name)).offset(skip).limit(limit).all()

def get_ingredient_by_id(db: Session, ingredient_id: UUID):
    return db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()

def get_ingredient_by_name(db: Session, ingredient_name: str):
    return db.query(Ingredient).filter(Ingredient.name == ingredient_name).first()
    
def get_ingredient_by_category(db: Session, ingredient_category: str):
    ingredient_by_category = get_ingredient_category_by_name(db, ingredient_category)

    return db.query(Ingredient).filter(Ingredient.ingredient_category_id == ingredient_by_category.id).all()

def check_unique_ingedient_name(db: Session, ingredient_name: str):
    return db.query(Ingredient).filter(func.lower(Ingredient.name) == func.lower(ingredient_name)).first()

def post_ingredient(db: Session, ingredient: IngredientCreate):
    ingredient_data = {key: value for key, value in ingredient.dict().items() if value is not None}
    db_ingredient = Ingredient(**ingredient_data)

    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)

    return db_ingredient

#TODO! remove this dead code
def create_ingredient_by_name(db: Session, ingredient: IngredientCreate):
    ingredient_category = get_ingredient_category_by_name(db, ingredient.ingredient_category)

    if ingredient_category:
        db_ingredient = Ingredient(
            name=ingredient.name, 
            brand=ingredient.brand,
            is_essential=ingredient.is_essential,
            ingredient_category_id=ingredient_category.id,
            icon=ingredient.icon
        )
        db.add(db_ingredient)
        db.commit()
        db.refresh(db_ingredient)

        return db_ingredient

def put_ingredient(
    db: Session, 
    ingredient_id: UUID, 
    ingredient: IngredientUpdate
):
    db_ingredient = get_ingredient_by_id(db, ingredient_id)
    
    if db_ingredient:
        if ingredient:
            if ingredient.name and ingredient.name != db_ingredient.name:
                if check_unique_ingedient_name(db, ingredient.name):
                    raise HTTPException(
                        status_code=400, 
                        detail=f"'{ingredient.name}' as Ingredient is already exists"
                    )
        for key, value in ingredient.dict().items():
            if key == 'ingredient_category' and value is not None:
                ingredient_category = get_ingredient_category_by_name(db, value)
                if ingredient_category:
                    setattr(db_ingredient, 'ingredient_category', ingredient_category)
                    
            elif value is not None:
                setattr(db_ingredient, key, value)

        db.commit()
        db.refresh(db_ingredient)
        
        return db_ingredient



def delete_ingredient(db: Session, ingredient_id: UUID):
    db_ingredient = get_ingredient_by_id(db, ingredient_id)
    db.delete(db_ingredient)
    db.commit()