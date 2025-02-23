from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.recipe_tag_recipe_association import *
from utils.user import check_valid_user
from utils.auth import get_current_user
from utils.recipe import get_recipe_by_id
from utils.recipe_tag import get_recipe_tag_by_id
from db.db_setup import get_db
from pydantic_schemas.recipe_tag_recipe_association import RecipeTagRecipeAssociationResponse, RecipeTagRecipeAssociationsLiteResponse, RecipeTagRecipeAssociationsResponse,  RecipeTagRecipeAssociationCreate, RecipeTagRecipeAssociationUpdate


router = APIRouter(
    prefix="/recipe_tag_recipe_associations",
    tags=["Recipe Tag Recipe Associations"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=RecipeTagRecipeAssociationsLiteResponse)
async def read_recipe_tag_recipe_associations(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), skip: int=0, limit: int = 100):
    db_recipe_tag_recipe_associations = get_recipe_tag_recipe_association(db, skip=skip, limit=limit)

    if not db_recipe_tag_recipe_associations:
        raise HTTPException(status_code=404, detail="Recipe Tag Recipe Association list is empty")

    return {
        "detail": f"Recipe Tag Recipe Association list is retrieved successfully",
        "recipe_tag_recipe_associations": db_recipe_tag_recipe_associations
    }

@router.get("/{recipe_tag_recipe_association_id}", status_code=status.HTTP_200_OK, response_model=RecipeTagRecipeAssociationResponse)
async def read_recipe_tag_recipe_associations_by_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_tag_recipe_association_id: UUID):
    db_recipe_tag_recipe_association = get_recipe_tag_recipe_association_by_id(db, recipe_tag_recipe_association_id)

    if not db_recipe_tag_recipe_association:
        raise HTTPException(
            status_code=404, 
            detail=f"ID {recipe_tag_recipe_association_id} as Recipe Tag Recipe Association is not found"
        )

    return {
        "detail": f"ID {recipe_tag_recipe_association_id} as Recipe Tag Recipe Association is retrieved successfully",
        "recipe_tag_recipe_association": db_recipe_tag_recipe_association
    }

@router.get("/by_recipe_id/{recipe_id}", status_code=status.HTTP_200_OK, response_model=RecipeTagRecipeAssociationsResponse)
async def read_recipe_tag_recipe_associations_by_recipe_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_id: UUID):
    db_recipe_tag_recipe_associations = get_recipe_tag_recipe_association_by_recipe_id(db, recipe_id)

    if not db_recipe_tag_recipe_associations:
        raise HTTPException(status_code=404, detail=f"Recipe Tag Recipe Association list for ID {recipe_id} of recipe is empty")

    return {
        "detail": f"Recipe Tag Recipe Association list of ID {recipe_id} of Recipe is retrieved successfully",
        "recipe_tag_recipe_associations": db_recipe_tag_recipe_associations
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RecipeTagRecipeAssociationResponse)
async def add_recipe_tag_recipe_association(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_tag_recipe_association: RecipeTagRecipeAssociationCreate):
    db_recipe = get_recipe_by_id(db, recipe_tag_recipe_association.recipe_id)

    if not db_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_tag_recipe_association.recipe_id} as Recipe is not found"
        )

    db_recipe_tag_recipe_association = check_recipe_tag_recipe_association_by_recipe_tag_duplication(db, recipe_tag_recipe_association)

    if db_recipe_tag_recipe_association:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"ID {recipe_tag_recipe_association.recipe_tag_id} of Recipe Tag as Recipe Tag Recipe Association is already registered"
        )

    db_recipe_tag = get_recipe_tag_by_id(db, recipe_tag_recipe_association.recipe_tag_id)

    if not db_recipe_tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_tag_recipe_association.recipe_tag_id} as Recipe Tag is not found"
        )

    recipe_tag_recipe_association_create = post_recipe_tag_recipe_association(db, recipe_tag_recipe_association)
    result_message = f"ID {recipe_tag_recipe_association.recipe_tag_id} of Recipe Tag as Recipe Tag Recipe Association is created successfully for ID {recipe_tag_recipe_association.recipe_id} of Recipe"

    return {"detail": result_message, "recipe_tag_recipe_association": recipe_tag_recipe_association_create}

@router.put("/{recipe_tag_recipe_association_id}", status_code=status.HTTP_202_ACCEPTED, response_model=RecipeTagRecipeAssociationResponse)
async def change_recipe_tag_recipe_association(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_tag_recipe_association_id: UUID, recipe_tag_recipe_association: RecipeTagRecipeAssociationUpdate):
    db_recipe_tag_recipe_association = get_recipe_tag_recipe_association_by_id(db, recipe_tag_recipe_association_id)

    #TODO! do url param checking to all endpoint
    if not db_recipe_tag_recipe_association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_tag_recipe_association_id} as Recipe Tag Recipe Association is not found"
        )

    if not any(value is not None for value in recipe_tag_recipe_association.dict().values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must include at least one field to update"
        )

    if hasattr(recipe_tag_recipe_association, 'recipe_tag_id') and recipe_tag_recipe_association.recipe_tag_id is not None:
        db_recipe_tag = get_recipe_tag_by_id(db, recipe_tag_recipe_association.recipe_tag_id)

        if not db_recipe_tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"ID {recipe_tag_recipe_association.recipe_tag_id} as Recipe Tag is not found"
            )

    recipe_tag_recipe_association_update = put_recipe_tag_recipe_association(db, recipe_tag_recipe_association_id, recipe_tag_recipe_association)
    result_message = f"ID {recipe_tag_recipe_association.recipe_tag_id} of Recipe Tag as Recipe Tag Recipe Association is updated successfully for ID {db_recipe_tag_recipe_association.recipe_id} of Recipe"

    return {"detail": result_message, "recipe_tag_recipe_association": recipe_tag_recipe_association_update}

@router.delete("/{recipe_tag_recipe_association_id}", status_code=status.HTTP_200_OK)
async def remove_recipe_tag_recipe_association(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_tag_recipe_association_id: UUID):
    db_recipe_tag_recipe_association = get_recipe_tag_recipe_association_by_id(db, recipe_tag_recipe_association_id)

    if not db_recipe_tag_recipe_association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_tag_recipe_association_id} as Recipe Tag Recipe Association is not found"
        )

    delete_recipe_tag_recipe_association(db, recipe_tag_recipe_association_id)
    result_message = f"ID {recipe_tag_recipe_association_id} as Recipe Tag Recipe Association for ID {db_recipe_tag_recipe_association.recipe_id} of Recipe is deleted successfully"

    return {"detail": result_message}
