from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query , status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.ingredient_recipe_association import *
from db.db_setup import get_db
from pydantic_schemas.ingredient_recipe_association import IngredientRecipeAssociation, IngredientRecipeAssociationResponseLite, IngredientRecipeAssociationsResponseLite


router = APIRouter(
    prefix="/ingredient_recipe_association",
    tags=["Ingredient Recipe Association"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=IngredientRecipeAssociationsResponseLite)
async def read_ingredient_recipe_associations(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    ingredient_recipe_associations = get_ingredient_recipe_associations(db, skip=skip, limit=limit)

    if not ingredient_recipe_associations:
        raise HTTPException(status_code=404, detail="Ingredient recipe association list is empty")

    return {
        "detail": f"Ingredient and recipe association list is retrieved successfully",
        "ingredient_recipe_associations": ingredient_recipe_associations
    }

@router.get("/by_recipe_id/{recipe_id}", status_code=status.HTTP_200_OK, response_model=IngredientRecipeAssociationsResponseLite)
async def read_ingredient_recipe_associations_by_recipe_id(*, db: Session = Depends(get_db), recipe_id: UUID):
    ingredient_recipe_associations = get_ingredient_recipe_associations_by_recipe_id(db, recipe_id)

    if not ingredient_recipe_associations:
        raise HTTPException(status_code=404, detail=f"Ingredient recipe association list for ID {recipe_id} of recipe is empty")

    return {
        "detail": f"Ingredient and recipe association list of ID {recipe_id} recipe is retrieved successfully",
        "ingredient_recipe_associations": ingredient_recipe_associations
    }



@router.get("/by_recipe_name", response_model=List[IngredientRecipeAssociation], deprecated=True)
async def read_ingredient_recipe_associations_by_recipe_name(*, db: Session = Depends(get_db), recipe_name: str):
    ingredient_recipe_associations = get_ingredient_recipe_associations_by_recipe_name(db, recipe_name)

    if not ingredient_recipe_associations:
        raise HTTPException(status_code=404, detail="Ingredient Recipe Association List is empty")

    return ingredient_recipe_associations
