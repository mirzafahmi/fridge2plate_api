from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException
from uuid import UUID

from db.models.recipe import IngredientRecipeAssociation
from pydantic_schemas.ingredient_recipe_association import IngredientRecipeAssociationCreate, IngredientRecipeAssociationUpdate
from utils.ingredient import get_ingredient_by_id
from utils.uom import get_uom_by_id
from utils.recipe import get_recipe_by_name, get_recipe_by_id


def get_ingredient_recipe_associations(db: Session, skip: int=0, limit: int = 100):
    return db.query(IngredientRecipeAssociation).offset(skip).limit(limit).all()

def get_ingredient_recipe_associations_by_id(db: Session, ingredient_recipe_associations_id: UUID):
    return db.query(IngredientRecipeAssociation).filter(IngredientRecipeAssociation.id == ingredient_recipe_associations_id).first()

def get_ingredient_recipe_associations_by_recipe_id(db: Session, recipe_id: UUID):
    return db.query(IngredientRecipeAssociation).filter(IngredientRecipeAssociation.recipe_id == recipe_id).all()

def get_ingredient_recipe_associations_by_recipe_name(db: Session, recipe_name: str):
    recipe = get_recipe_by_name(db, recipe_name)
    return db.query(IngredientRecipeAssociation).filter(IngredientRecipeAssociation.recipe_id == recipe.id).all()

def check_ingredient_recipe_associations_by_ingredient_duplication(db: Session, ingredient_recipe_association: IngredientRecipeAssociationCreate):
    return db.query(IngredientRecipeAssociation).filter_by(recipe_id=ingredient_recipe_association.recipe_id, ingredient_id=ingredient_recipe_association.ingredient_id).first()

def post_association(db: Session, ingredient: IngredientRecipeAssociationCreate):
    ingredient_data = {key: value for key, value in ingredient.dict().items() if value is not None}
    db_association = IngredientRecipeAssociation(**ingredient_data)

    db.add(db_association)
    db.commit()
    db.refresh(db_association)

    return db_association

def put_association(db: Session, ingredient_recipe_association_id: UUID, ingredient: IngredientRecipeAssociationUpdate):
    db_ingredient_recipe_asscociation = get_ingredient_recipe_associations_by_id(db, ingredient_recipe_association_id)

    if ingredient:
        for key, value in ingredient.dict().items():
            if value is not None:
                setattr(db_ingredient_recipe_asscociation, key, value)

    db.commit()
    db.refresh(db_ingredient_recipe_asscociation)

    return db_ingredient_recipe_asscociation

def delete_association(db: Session, ingredient_recipe_association_id: UUID):
    db_ingredient_recipe_asscociation = get_ingredient_recipe_associations_by_id(db, ingredient_recipe_association_id)
    
    db.delete(db_ingredient_recipe_asscociation)
    db.commit()