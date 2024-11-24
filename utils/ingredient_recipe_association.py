from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException
from uuid import UUID

from db.models.recipe import IngredientRecipeAssociation
from pydantic_schemas.ingredient_recipe_association import IngredientRecipeAssociationBase
from utils.ingredient import get_ingredient_by_name
from utils.uom import get_uom_by_name
from utils.recipe import get_recipe_by_name, get_recipe_by_id


def get_ingredient_recipe_associations(db: Session, skip: int=0, limit: int = 100):
    data = db.query(IngredientRecipeAssociation).offset(skip).limit(limit).all()

    return data

def get_ingredient_recipe_associations_by_id(db: Session, ingredient_recipe_associations_id: UUID):
    data = db.query(IngredientRecipeAssociation).filter(IngredientRecipeAssociation.id == ingredient_recipe_associations_id).first()

    return data

def get_ingredient_recipe_associations_by_recipe_id(db: Session, recipe_id: UUID):
    data = db.query(IngredientRecipeAssociation).filter(IngredientRecipeAssociation.recipe_id == recipe_id).all()

    return data

def get_ingredient_recipe_associations_by_recipe_name(db: Session, recipe_name: str):
    recipe = get_recipe_by_name(db, recipe_name)

    if not recipe:
        raise HTTPException(status_code=404, detail=f"Recipe with name {recipe_name} not found")

    data = db.query(IngredientRecipeAssociation).filter(IngredientRecipeAssociation.recipe_id == recipe.id).all()

    return data

def post_association(db: Session, recipe_id: int, ingredient: IngredientRecipeAssociationBase):
    ingredient_db = get_ingredient_by_name(db, ingredient.ingredient)
    uom_db = get_uom_by_name(db, ingredient.uom)

    db_association = IngredientRecipeAssociation(
        recipe_id=recipe_id, 
        ingredient_id=ingredient_db.id, 
        quantity=ingredient.quantity, 
        uom_id=uom_db.id
    )

    db.add(db_association)
    db.commit()
    db.refresh(db_association)

    return db_association


def update_association(db: Session, recipe_id: int, ingredient: IngredientRecipeAssociation):
    db_recipe = get_recipe_by_id(db, recipe_id)
    #update must same as create as we delete the current assoc
    if db_recipe:
        # Update the properties of the existing recipe category
        if ingredient:
            for key, value in ingredient.dict().items():
                if value is not None:
                    setattr(db_recipe, key, value)

        db.commit()
        db.refresh(db_recipe)

        return db_recipe
    else:
        raise HTTPException(status_code=404, detail=f"Recipe with name {db_recipe.name} not found")


def delete_association(db: Session, recipe_id: int):
    recipe_name = get_recipe_by_id(db, recipe_id).name
    db_associations = get_ingredient_recipe_associations_by_recipe_id(db, recipe_id)
    print(db_associations)
    if not db_associations:
        raise HTTPException(status_code=404, detail=f"Ingredient association with recipe {recipe_name} not found")

    for db_association in db_associations:
        db.delete(db_association)

    db.commit()