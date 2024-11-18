from sqlalchemy.orm import Session
from typing import Optional

from db.models.recipe import IngredientCategory
from pydantic_schemas.ingredient_category import IngredientCategoryCreate


def get_ingredient_categories(db: Session, skip: int=0, limit: int = 100):
    return db.query(IngredientCategory).offset(skip).limit(limit).all()


def get_ingredient_category_by_id(db: Session, ingredient_category_id: int):
    return db.query(IngredientCategory).filter(IngredientCategory.id == ingredient_category_id).first()


def get_ingredient_category_by_name(db: Session, ingredient_category_name: str):
    return db.query(IngredientCategory).filter(IngredientCategory.name == ingredient_category_name).first()


def post_ingredient_category(db: Session, ingredient_category: IngredientCategoryCreate):
    if ingredient_category.dict().get('id') is not None:
        db_ingredient_category = IngredientCategory(
            id=ingredient_category.id, 
            name=ingredient_category.name
        )
    else:
        db_ingredient_category = IngredientCategory(name=ingredient_category.name)

    db.add(db_ingredient_category)
    db.commit()
    db.refresh(db_ingredient_category)

    return db_ingredient_category


def update_ingredient_category(
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
        raise HTTPException(status_code=404, detail=f"Ingredient Category with name {ingredient_category_name} not found")


def delete_ingredient_category(db: Session, ingredient_category_name: str):
    db_ingredient_category = get_ingredient_category_by_name(db, ingredient_category_name)
    
    if not db_ingredient_category:
        raise HTTPException(status_code=404, detail=f"Ingredient Category with name {ingredient_category_name} not found")

    db.delete(db_ingredient_category)
    db.commit()