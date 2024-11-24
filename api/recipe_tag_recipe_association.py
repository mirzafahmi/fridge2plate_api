from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.recipe_tag_recipe_association import *
from db.db_setup import get_db
from pydantic_schemas.recipe_tag_recipe_association import RecipeTagRecipeAssociationsLiteResponse, RecipeTagRecipeAssociationsListLiteResponse


router = APIRouter(
    prefix="/recipe_tag_recipe_association",
    tags=["Recipe Tag Recipe Association"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=RecipeTagRecipeAssociationsListLiteResponse)
async def read_recipe_tag_recipe_associations(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    recipe_tag_recipe_associations = get_recipe_tag_recipe_association(db, skip=skip, limit=limit)

    if not recipe_tag_recipe_associations:
        raise HTTPException(status_code=404, detail="Recipe tag recipe association list is empty")

    return {
        "detail": f"Recipe tag and recipe association list is retrieved successfully",
        "recipe_tag_recipe_associations": recipe_tag_recipe_associations
    }

@router.get("/by_recipe_id/{recipe_id}", status_code=status.HTTP_200_OK, response_model=RecipeTagRecipeAssociationsLiteResponse)
async def read_recipe_tag_recipe_associations_by_recipe_id(*, db: Session = Depends(get_db), recipe_id: UUID):
    recipe_tag_recipe_associations = get_recipe_tag_recipe_association_by_recipe_id(db, recipe_id)

    if not recipe_tag_recipe_associations:
        raise HTTPException(status_code=404, detail=f"Recipe tag recipe association list for ID {recipe_id} of recipe is empty")

    return {
        "detail": f"Recipe tag and recipe association list of ID {recipe_id} of recipe is retrieved successfully",
        "recipe_tag_recipe_associations": recipe_tag_recipe_associations
    }
