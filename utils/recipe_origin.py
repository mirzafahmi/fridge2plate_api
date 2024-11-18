from sqlalchemy.orm import Session
from typing import Optional

from db.models.recipe import RecipeOrigin
from pydantic_schemas.recipe_origin import RecipeOriginCreate


def get_recipe_origins(db: Session, skip: int=0, limit: int = 100):
    return db.query(RecipeOrigin).offset(skip).limit(limit).all()


def get_recipe_origin_by_id(db: Session, recipe_origin_id: int):
    return db.query(RecipeOrigin).filter(RecipeOrigin.id == recipe_origin_id).first()


def get_recipe_origin_by_name(db: Session, recipe_origin_name: str):
    return db.query(RecipeOrigin).filter(RecipeOrigin.name == recipe_origin_name).first()


def post_recipe_origin(db: Session, recipe_origin: RecipeOriginCreate):
    recipe_origin_data = {key: value for key, value in recipe_origin.dict().items() if value is not None}
    db_recipe_origin = RecipeOrigin(**recipe_origin_data)
    
    db.add(db_recipe_origin)
    db.commit()
    db.refresh(db_recipe_origin)

    return db_recipe_origin


def update_recipe_origin(
    db: Session, 
    recipe_origin_name: str, 
    recipe_origin: RecipeOriginCreate
):
    db_recipe_origin = get_recipe_origin_by_name(db, recipe_origin_name)
    
    if db_recipe_origin:
        
        if recipe_origin:
            for key, value in recipe_origin.dict().items():
                if value is not None:
                    setattr(db_recipe_origin, key, value)

        db.commit()
        db.refresh(db_recipe_origin)

        return db_recipe_origin
    else:
        raise HTTPException(status_code=404, detail=f"Recipe Origin with name {recipe_origin_name} not found")


def delete_recipe_origin(db: Session, recipe_origin_name: str):
    db_recipe_origin = get_recipe_origin_by_name(db, recipe_origin_name)
    
    if not db_recipe_origin:
        raise HTTPException(status_code=404, detail=f"Recipe Origin with name {recipe_origin_name} not found")

    db.delete(db_recipe_origin)
    db.commit()