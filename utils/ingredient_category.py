from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func, asc
from fastapi import HTTPException, status
from uuid import UUID

from db.models.recipe import IngredientCategory, Ingredient
from pydantic_schemas.ingredient_category import IngredientCategoryCreate


def get_ingredient_categories(db: Session, skip: int=0, limit: int = 100):
    return db.query(IngredientCategory).order_by(asc(IngredientCategory.name)).offset(skip).limit(limit).all()

def get_ingredient_category_by_id(db: Session, ingredient_category_id: UUID):
    return db.query(IngredientCategory).filter(IngredientCategory.id == ingredient_category_id).first()

def get_ingredient_category_by_name(db: Session, ingredient_category_name: str):
    return db.query(IngredientCategory).filter(IngredientCategory.name == ingredient_category_name).first()

def check_unique_ingedient_category_name(db: Session, ingredient_category_name: str):
    return db.query(IngredientCategory).filter(func.lower(IngredientCategory.name) == func.lower(ingredient_category_name)).first()

def post_ingredient_category(db: Session, ingredient_category: IngredientCategoryCreate):
    ingredient_category_data = {key: value for key, value in ingredient_category.dict().items() if value is not None}
    db_ingredient_category = IngredientCategory(**ingredient_category_data)

    db.add(db_ingredient_category)
    db.commit()
    db.refresh(db_ingredient_category)

    return db_ingredient_category

def update_ingredient_category(
    db: Session, 
    ingredient_category_id: UUID, 
    ingredient_category: Optional[IngredientCategoryCreate]
):
    db_ingredient_category = get_ingredient_category_by_id(db, ingredient_category_id)

    if db_ingredient_category:
        if ingredient_category:
            if ingredient_category.name and ingredient_category.name != db_ingredient_category.name:
                if check_unique_ingedient_category_name(db, ingredient_category.name):
                    raise HTTPException(
                        status_code=400, 
                        detail=f"'{ingredient_category.name}' as Ingredient Category is already registered"
                    )
            for key, value in ingredient_category.dict().items():
                if value is not None:
                    setattr(db_ingredient_category, key, value)

        db.commit()
        db.refresh(db_ingredient_category)

        return db_ingredient_category
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Ingredient Category with id {ingredient_category_id} not found"
        )


def delete_ingredient_category(db: Session, ingredient_category_id: UUID):
    db_ingredient_category = get_ingredient_category_by_id(db, ingredient_category_id)

    db.query(Ingredient).filter(Ingredient.ingredient_category_id == db_ingredient_category.id).update({
        Ingredient.ingredient_category_id: None
    })

    db.commit()
    
    db.delete(db_ingredient_category)
    db.commit()





def update_ingredient_category_by_name(
    db: Session, 
    ingredient_category_name: str, 
    ingredient_category: Optional[IngredientCategoryCreate],
    new_name: Optional[str] = None
):
    db_ingredient_category = get_ingredient_category_by_name(db, ingredient_category_name)
    
    if db_ingredient_category:
        if ingredient_category:
            for key, value in ingredient_category.dict().items():
                if value is not None:
                    setattr(db_ingredient_category, key, value)

        if new_name:
            db_ingredient_category.name = new_name

        db.commit()
        db.refresh(db_ingredient_category)

        return db_ingredient_category
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Ingredient Category with name {ingredient_category_name} not found"
        )


def delete_ingredient_category_by_name(db: Session, ingredient_category_name: str):
    db_ingredient_category = get_ingredient_category_by_name(db, ingredient_category_name)
    
    if not db_ingredient_category:
        raise HTTPException(
            status_code=404, 
            detail=f"Ingredient Category with name {ingredient_category_name} not found"
        )

    db.delete(db_ingredient_category)
    db.commit()