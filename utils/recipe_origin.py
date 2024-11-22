from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func, asc
from uuid import UUID
from fastapi import HTTPException, status

from db.models.recipe import RecipeOrigin, Recipe
from pydantic_schemas.recipe_origin import RecipeOriginCreate, RecipeOriginUpdate


def get_recipe_origins(db: Session, skip: int=0, limit: int = 100):
    return db.query(RecipeOrigin).order_by(asc(RecipeOrigin.name)).offset(skip).limit(limit).all()

def get_recipe_origin_by_id(db: Session, recipe_origin_id: UUID):
    return db.query(RecipeOrigin).filter(RecipeOrigin.id == recipe_origin_id).first()

def get_recipe_origin_by_name(db: Session, recipe_origin_name: str):
    return db.query(RecipeOrigin).filter(RecipeOrigin.name == recipe_origin_name).first()

def check_unique_recipe_origin_name(db: Session, recipe_origin_name: str):
    return db.query(RecipeOrigin).filter(func.lower(RecipeOrigin.name) == func.lower(recipe_origin_name)).first()

def post_recipe_origin(db: Session, recipe_origin: RecipeOriginCreate):
    recipe_origin_data = {key: value for key, value in recipe_origin.dict().items() if value is not None}
    db_recipe_origin = RecipeOrigin(**recipe_origin_data)
    
    db.add(db_recipe_origin)
    db.commit()
    db.refresh(db_recipe_origin)

    return db_recipe_origin

def put_recipe_origin(db: Session, recipe_origin_id: UUID, recipe_origin: RecipeOriginUpdate):
    db_recipe_origin = get_recipe_origin_by_id(db, recipe_origin_id)
    
    if db_recipe_origin:
        if recipe_origin:
            if recipe_origin.name and recipe_origin.name != db_recipe_origin.name:
                if check_unique_recipe_origin_name(db, recipe_origin.name):
                    raise HTTPException(
                            status_code=400, 
                            detail=f"{recipe_origin.name} as Recipe Origin is already registered"
                        )
            for key, value in recipe_origin.dict().items():
                if value is not None:
                    setattr(db_recipe_origin, key, value)

        db.commit()
        db.refresh(db_recipe_origin)

        return db_recipe_origin
    else:
        raise HTTPException(status_code=404, detail=f"{recipe_origin_name} as Recipe Origin is not found")

def delete_recipe_origin(db: Session, recipe_origin_id: UUID):
    db_recipe_origin = get_recipe_origin_by_id(db, recipe_origin_id)
    
    db.query(Recipe).filter(Recipe.recipe_origin_id == db_recipe_origin.id).update({
        Recipe.recipe_origin_id: None
    })

    db.commit()

    db.delete(db_recipe_origin)
    db.commit()