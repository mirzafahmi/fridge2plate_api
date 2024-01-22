from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query 
from sqlalchemy.orm import Session

from api.utils.ingredient_recipe_association import *
from db.db_setup import get_db
from pydantic_schemas.ingredient_recipe_association import IngredientRecipeAssociation


router = APIRouter(tags=["Ingredient Recipe Association"])

@router.get("/ingredient_recipe_association_list", response_model=List[IngredientRecipeAssociation])
async def read_ingredient_recipe_associations(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    ingredient_recipe_associations = get_ingredient_recipe_associations(db, skip=skip, limit=limit)

    if not ingredient_recipe_associations:
        raise HTTPException(status_code=404, detail="Ingredient Categories is empty")

    return ingredient_recipe_associations