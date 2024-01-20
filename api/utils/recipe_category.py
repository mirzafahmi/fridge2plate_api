from sqlalchemy.orm import Session
from typing import Optional

from db.models.recipe import RecipeCategory
from pydantic_schemas.recipe_category import RecipeCategoryCreate


def get_recipe_categories(db: Session, skip: int=0, limit: int = 100):
    return db.query(RecipeCategory).offset(skip).limit(limit).all()


def get_recipe_category_by_id(db: Session, recipe_category_id: int):
    return db.query(RecipeCategory).filter(RecipeCategory.id == recipe_category_id).first()


def get_recipe_category_by_name(db: Session, recipe_category_name: str):
    return db.query(RecipeCategory).filter(RecipeCategory.name == recipe_category_name).first()


def create_recipe_category(db: Session, recipe_category: RecipeCategoryCreate):
    db_recipe_category = RecipeCategory(name=recipe_category.name)
    db.add(db_recipe_category)
    db.commit()
    db.refresh(db_recipe_category)

    return db_recipe_category


def update_recipe_category(
    db: Session, 
    recipe_category_name: str, 
    recipe_category: RecipeCategoryCreate
):
    db_recipe_category = get_recipe_category_by_name(db, recipe_category_name)
    
    if db_recipe_category:
        
        if recipe_category:
            for key, value in recipe_category.dict().items():
                if value is not None:
                    setattr(db_recipe_category, key, value)

        db.commit()
        db.refresh(db_recipe_category)

        return db_recipe_category
    else:
        raise HTTPException(status_code=404, detail=f"Recipe Category with name {recipe_category_name} not found")


def delete_recipe_category(db: Session, recipe_category_name: str):
    db_recipe_category = get_recipe_category_by_name(db, recipe_category_name)
    
    if not db_recipe_category:
        raise HTTPException(status_code=404, detail=f"Recipe Category with name {recipe_category_name} not found")

    db.delete(db_recipe_category)
    db.commit()