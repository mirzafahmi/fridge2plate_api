from sqlalchemy.orm import Session
from typing import Optional

from db.models.recipe import Ingredient
from pydantic_schemas.ingredient import IngredientCreate


def get_ingredients(db: Session, skip: int=0, limit: int = 100):
    return db.query(Ingredient).offset(skip).limit(limit).all()


def get_ingredient_by_id(db: Session, ingredient_id: int):
    return db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()


def get_ingredient_by_name(db: Session, ingredient_name: str):
    return db.query(Ingredient).filter(Ingredient.name == ingredient_name).first()


def create_ingredient(db: Session, ingredient: IngredientCreate):
    db_ingredient = Ingredient(
        name=ingredient.name, 
        brand=ingredient.brand,
        is_essential=ingredient.is_essential,
        ingredient_category_id=ingredient.ingredient_category_id
    )
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)

    return db_ingredient


def update_ingredient(
    db: Session, 
    ingredient_name: str, 
    ingredient: IngredientCreate
):
    db_ingredient = get_ingredient_by_name(db, ingredient_name)
    
    if db_ingredient:
        
        if ingredient:
            for key, value in ingredient.dict().items():
                setattr(db_ingredient, key, value)

        db.commit()
        db.refresh(db_ingredient)

        return db_ingredient
    else:
        raise HTTPException(status_code=404, detail=f"Ingredient with name {ingredient_name} not found")


def delete_ingredient(db: Session, ingredient_name: str):
    db_ingredient = get_ingredient_by_name(db, ingredient_name)
    
    if not db_ingredient:
        raise HTTPException(status_code=404, detail=f"Ingredient with name {ingredient_name} not found")

    db.delete(db_ingredient)
    db.commit()