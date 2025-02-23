from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.recipe_tag import *
from utils.user import check_valid_user
from utils.auth import get_current_user
from db.db_setup import get_db
from pydantic_schemas.recipe_tag import RecipeTag, RecipeTagCreate, RecipeTagUpdate, RecipeTagResponse, RecipeTagsResponse


router = APIRouter(
    prefix="/recipe_tags",
    tags=["Recipe Tags"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=RecipeTagsResponse)
async def read_recipe_tags(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), skip: int=0, limit: int = 100):
    recipe_tags = get_recipe_tags(db, skip=skip, limit=limit)

    if not recipe_tags:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipe Tag list is empty"
        )

    return {
        "detail": "Recipe Tag list is retrieved successfully",
        "recipe_tags": recipe_tags
    }

@router.get("/{recipe_tag_id}", status_code=status.HTTP_200_OK, response_model=RecipeTagResponse)
async def read_recipe_tag_by_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_tag_id: UUID):
    recipe_tag_by_id = get_recipe_tag_by_id(db, recipe_tag_id)

    if recipe_tag_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe_tag_id} as Recipe Tag is not found"
        )

    return {
        "detail": f"Id {recipe_tag_id} as Recipe Tag is retrieved successfully",
        "recipe_tag": recipe_tag_by_id
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RecipeTagResponse)
async def add_recipe_tag(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_tag: RecipeTagCreate):
    recipe_tag_by_name = get_recipe_tag_by_name(db, recipe_tag.name)
    
    if recipe_tag_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{recipe_tag.name} as Recipe Tag is already registered"
        )

    check_valid_user(db, recipe_tag)

    recipe_tag_create = post_recipe_tag(db, recipe_tag)

    result_message = f"{recipe_tag.name} as Recipe Tag is created successfully"

    return {"detail": result_message, "recipe_tag": recipe_tag_create}

@router.put("/{recipe_tag_id}", status_code=status.HTTP_202_ACCEPTED, response_model=RecipeTagResponse)
async def change_recipe_tag(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_tag_id: UUID, recipe_tag: RecipeTagUpdate):
    recipe_tag_by_id = get_recipe_tag_by_id(db, recipe_tag_id)
    
    if not recipe_tag_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe_tag_id} as Recipe Tag is not registered"
        )

    check_valid_user(db, recipe_tag)
    
    recipe_tag_update = put_recipe_tag(db, recipe_tag_id, recipe_tag)

    result_message = f"Id {recipe_tag_id} as Recipe Tag is updated successfully"

    return {"detail": result_message, "recipe_tag": recipe_tag_update}

@router.delete("/{recipe_tag_id}", status_code=status.HTTP_200_OK)
async def remove_recipe_tag(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_tag_id: UUID):
    recipe_tag_by_id = get_recipe_tag_by_id(db, recipe_tag_id)

    if recipe_tag_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe_tag_id} as Recipe Tag is not found"
        )

    delete_recipe_tag(db, recipe_tag_id)
    result_message = f"Id {recipe_tag_id} as Recipe Tag is deleted successfully"

    return {"detail": result_message}




@router.get("by_name/{recipe_tag_name}", status_code=status.HTTP_200_OK, response_model=RecipeTag, deprecated=True)
async def read_recipe_tag_by_name(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_tag_name: str):
    recipe_tag_by_name = get_recipe_tag_by_name(db, recipe_tag_name=recipe_tag_name)

    if recipe_tag_by_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{recipe_tag_name} as Recipe Tag is not found"
        )

    return recipe_tag_by_name
