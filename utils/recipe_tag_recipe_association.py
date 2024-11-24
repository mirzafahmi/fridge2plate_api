from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status

from db.models.recipe import RecipeTagRecipeAssociation


def get_recipe_tag_recipe_association(db: Session, skip: int=0, limit: int = 100):
    data = db.query(RecipeTagRecipeAssociation).offset(skip).limit(limit).all()

    return data

def get_recipe_tag_recipe_association_by_recipe_id(db: Session, recipe_id: UUID):
    data = db.query(RecipeTagRecipeAssociation).filter(RecipeTagRecipeAssociation.recipe_id == recipe_id).all()

    return data