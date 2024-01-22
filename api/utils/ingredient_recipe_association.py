from sqlalchemy.orm import Session
from typing import Optional

from db.models.recipe import IngredientRecipeAssociation
from pydantic_schemas.ingredient_recipe_association import IngredientRecipeAssociationBase
from api.utils.ingredient import get_ingredient_by_name
from api.utils.uom import get_uom_by_name


def get_ingredient_recipe_associations(db: Session, skip: int=0, limit: int = 100):
    data = db.query(IngredientRecipeAssociation).offset(skip).limit(limit).all()
    print(data)
    return data

def create_association(
    db: Session, 
    recipe_id: int, 
    ingredient: IngredientRecipeAssociationBase
):
    print(ingredient)
    print(ingredient.ingredient)
    print(ingredient.uom)
    ingredient_db = get_ingredient_by_name(db, ingredient.ingredient)
    uom_db = get_uom_by_name(db, ingredient.uom)

    db_association = IngredientRecipeAssociation(
        recipe_id=recipe_id, 
        ingredient_id=ingredient_db.id, 
        quantity=ingredient.quantity, 
        uom_id=uom_db.id)


    db.add(db_association)
    db.commit()
    db.refresh(db_association)

    return db_association
