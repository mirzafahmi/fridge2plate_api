from sqlalchemy.orm import Session
from typing import Optional

from db.models.recipe import IngredientRecipeAssociation
from pydantic_schemas.ingredient_recipe_association import IngredientRecipeAssociationBase
from api.utils.ingredient import get_ingredient_by_name
from api.utils.uom import get_uom_by_name
from api.utils.recipe import get_recipe_by_name


def get_ingredient_recipe_associations(db: Session, skip: int=0, limit: int = 100):
    data = db.query(IngredientRecipeAssociation).offset(skip).limit(limit).all()

    return data


def get_ingredient_recipe_associations_by_id(db: Session, ingredient_recipe_associations_id: int):
    data = db.query(IngredientRecipeAssociation).filter(IngredientRecipeAssociation.id == ingredient_recipe_associations_id).first()

    return data


def get_ingredient_recipe_associations_by_recipe_name(db: Session, recipe_name: str):
    recipe = get_recipe_by_name(db, recipe_name)

    data = db.query(IngredientRecipeAssociation).filter(IngredientRecipeAssociation.recipe_id == recipe.id).all()

    return data


def create_association(
    db: Session, 
    recipe_id: int, 
    ingredient: IngredientRecipeAssociationBase
):

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


def update_association(
    db: Session, 
    recipe_name: str, 
    ingredient: IngredientRecipeAssociation
):
    db_recipe = get_recipe_by_name(db, recipe_name)
    
    if db_recipe:
        # Update the properties of the existing recipe category
        if recipe:
            for key, value in recipe.dict().items():
                if value is not None:
                    setattr(db_recipe, key, value)

        if new_name:
            db_recipe.name = new_name

        db.commit()
        db.refresh(db_recipe)

        return db_recipe
    else:
        raise HTTPException(status_code=404, detail=f"recipe Category with name {recipe_name} not found")
