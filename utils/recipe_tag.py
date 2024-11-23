from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func, asc
from uuid import UUID
from fastapi import HTTPException, status

from db.models.recipe import RecipeTag, Recipe
from pydantic_schemas.recipe_tag import RecipeTagCreate, RecipeTagUpdate


def get_recipe_tags(db: Session, skip: int=0, limit: int = 100):
    return db.query(RecipeTag).order_by(asc(RecipeTag.name)).offset(skip).limit(limit).all()

def get_recipe_tag_by_id(db: Session, recipe_tag_id: UUID):
    return db.query(RecipeTag).filter(RecipeTag.id == recipe_tag_id).first()

def get_recipe_tag_by_name(db: Session, recipe_tag_name: str):
    return db.query(RecipeTag).filter(RecipeTag.name == recipe_tag_name).first()

def check_unique_recipe_tag_name(db: Session, recipe_tag_name: str):
    return db.query(RecipeTag).filter(func.lower(RecipeTag.name) == func.lower(recipe_tag_name)).first()

def post_recipe_tag(db: Session, recipe_tag: RecipeTagCreate):
    recipe_tag_data = {key: value for key, value in recipe_tag.dict().items() if value is not None}
    db_recipe_tag = RecipeTag(**recipe_tag_data)

    db.add(db_recipe_tag)
    db.commit()
    db.refresh(db_recipe_tag)

    return db_recipe_tag

def put_recipe_tag(db: Session, recipe_tag_id: UUID, recipe_tag: RecipeTagUpdate):
    db_recipe_tag = get_recipe_tag_by_id(db, recipe_tag_id)
    
    if db_recipe_tag:
        if recipe_tag:
            if recipe_tag.name and recipe_tag.name != db_recipe_tag.name:
                if check_unique_recipe_tag_name(db, recipe_tag.name):
                    raise HTTPException(
                            status_code=400, 
                            detail=f"{recipe_tag.name} as Recipe Tag is already registered"
                        )
            for key, value in recipe_tag.dict().items():
                if value is not None:
                    setattr(db_recipe_tag, key, value)

        db.commit()
        db.refresh(db_recipe_tag)

        return db_recipe_tag
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Id {recipe_tag_id} as Recipe Tag is not found"
        )

def delete_recipe_tag(db: Session, recipe_tag_id: UUID):
    db_recipe_tag = get_recipe_tag_by_id(db, recipe_tag_id)

    #CHECK ASSOC
    # db.query(Recipe).filter(Recipe.recipe_tag_id == db_recipe_tag.id).update({
    #     Recipe.recipe_tag_id: None
    # })

    db.commit()

    db.delete(db_recipe_tag)
    db.commit()