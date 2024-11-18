from sqlalchemy.orm import Session, joinedload
from typing import Optional

from db.models.recipe import Ingredient, IngredientCategory
from pydantic_schemas.ingredient import IngredientCreate, IngredientUpdate
from utils.ingredient_category import get_ingredient_category_by_name


def get_ingredients(db: Session, skip: int=0, limit: int = 100):
    return db.query(Ingredient).offset(skip).limit(limit).all()


def get_ingredient_by_id(db: Session, ingredient_id: int):
    return db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()


def get_ingredient_by_name(db: Session, ingredient_name: str):
    
    return db.query(Ingredient).filter(Ingredient.name == ingredient_name).first()
    
def get_ingredient_by_category(db: Session, ingredient_category: str):
    ingredient_by_category = get_ingredient_category_by_name(db, ingredient_category)

    return db.query(Ingredient).filter(Ingredient.ingredient_category_id == ingredient_by_category.id).all()

def post_ingredient(db: Session, ingredient: IngredientCreate):
    ingredient_data = {key: value for key, value in ingredient.dict().items() if value is not None}
    db_ingredient = Ingredient(**ingredient_data)

    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)

    return db_ingredient

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



def update_ingredient(
    db: Session, 
    ingredient_name: str, 
    ingredient: IngredientUpdate
):
    db_ingredient = get_ingredient_by_name(db, ingredient_name=ingredient_name)
    
    if db_ingredient:
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



def delete_ingredient(db: Session, ingredient_name: str):
    db_ingredient = get_ingredient_by_name(db, ingredient_name)
    db.delete(db_ingredient)
    db.commit()