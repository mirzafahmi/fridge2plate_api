from sqlalchemy.orm import Session
from typing import Optional

from db.models.recipe import RecipeTag
from pydantic_schemas.recipe_tag import RecipeTagCreate


def get_recipe_tags(db: Session, skip: int=0, limit: int = 100):
    return db.query(RecipeTag).offset(skip).limit(limit).all()


def get_recipe_tag_by_id(db: Session, recipe_tag_id: int):
    return db.query(RecipeTag).filter(RecipeTag.id == recipe_tag_id).first()


def get_recipe_tag_by_name(db: Session, recipe_tag_name: str):
    return db.query(RecipeTag).filter(RecipeTag.name == recipe_tag_name).first()


def post_recipe_tag(db: Session, recipe_tag: RecipeTagCreate):
    recipe_tag_data = {key: value for key, value in recipe_tag.dict().items() if value is not None}
    db_recipe_tag = RecipeTag(**recipe_tag_data)

    db.add(db_recipe_tag)
    db.commit()
    db.refresh(db_recipe_tag)

    return db_recipe_tag

#TODO: modify all update utils to exclude from auto assign id in update and must user id same as creator id to be able modify
def update_recipe_tag(
    db: Session, 
    recipe_tag_name: str, 
    recipe_tag: RecipeTagCreate):

    db_recipe_tag = get_recipe_tag_by_name(db, recipe_tag_name)
    
    if db_recipe_tag:
        
        if recipe_tag:
            for key, value in recipe_tag.dict().items():
                if value is not None:
                    setattr(db_recipe_tag, key, value)

        db.commit()
        db.refresh(db_recipe_tag)

        return db_recipe_tag
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Recipe Tag with name {recipe_tag_name} not found"
        )


def delete_recipe_tag(db: Session, recipe_tag_name: str):
    db_recipe_tag = get_recipe_tag_by_name(db, recipe_tag_name)
    
    if not db_recipe_tag:
        raise HTTPException(
            status_code=404, 
            detail=f"Recipe Tag with name {recipe_tag_name} not found"
        )

    db.delete(db_recipe_tag)
    db.commit()