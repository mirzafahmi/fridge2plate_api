from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.recipe_category import *
from utils.user import check_valid_user
from db.db_setup import get_db
from pydantic_schemas.recipe_category import RecipeCategory, RecipeCategoryCreate, RecipeCategoryUpdate, RecipeCategoryResponse, RecipeCategoriesResponse


router = APIRouter(
    prefix="/recipe_categories",
    tags=["Recipe Categories"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=RecipeCategoriesResponse)
async def read_recipe_categories(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    recipe_categories = get_recipe_categories(db, skip=skip, limit=limit)

    if not recipe_categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipe Category list is empty"
        )

    return {
        "detail": "Recipe Category list is retrieved successfully",
        "recipe_categories": recipe_categories
    }

@router.get("/{recipe_category_id}", status_code=status.HTTP_200_OK, response_model=RecipeCategoryResponse)
async def read_recipe_category_by_id(*, db: Session = Depends(get_db), recipe_category_id: UUID):
    recipe_category_by_id = get_recipe_category_by_id(db, recipe_category_id)

    if recipe_category_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe_category_id} as Recipe Category is not found"
        )

    return {
        "detail": f"Id {recipe_category_id} as Recipe Category is retrieved successfully",
        "recipe_category": recipe_category_by_id
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RecipeCategoryResponse)
async def add_recipe_category(*, db: Session = Depends(get_db), recipe_category: RecipeCategoryCreate):
    recipe_category_by_name = get_recipe_category_by_name(db, recipe_category_name=recipe_category.name)
    
    if recipe_category_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{recipe_category.name} as Recipe Category is already registered"
        )

    check_valid_user(db, recipe_category)

    recipe_category_create = post_recipe_category(db, recipe_category)

    result_message = f"{recipe_category.name} as Recipe Category is created successfully"

    return {"detail": result_message, "recipe_category": recipe_category_create}

@router.put("/{recipe_category_id}", status_code=status.HTTP_202_ACCEPTED, response_model=RecipeCategoryResponse)
async def change_recipe_category(*, db: Session = Depends(get_db), recipe_category_id: UUID, recipe_category: RecipeCategoryUpdate):
    db_recipe_category = get_recipe_category_by_id(db, recipe_category_id)
    
    if not db_recipe_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe_category_id} as Recipe Category is not found"
        )

    check_valid_user(db, recipe_category)

    recipe_category_update = put_recipe_category(db, recipe_category_id, recipe_category)
    result_message = f"Id {recipe_category_id} as Recipe Category is updated successfully"

    return {"detail": result_message, "recipe_category": recipe_category_update}

@router.delete("/{recipe_category_id}", status_code=status.HTTP_200_OK)
async def remove_recipe_category(*, db: Session = Depends(get_db), recipe_category_id: UUID):
    db_recipe_category = get_recipe_category_by_id(db, recipe_category_id)

    if not db_recipe_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe_category_id} as Recipe Category is not found"
        )

    delete_recipe_category(db, recipe_category_id)
    result_message = f"Id {recipe_category_id} as Recipe Category is deleted successfully"

    return {"detail": result_message}





@router.get("/by_name/{recipe_category_name}", status_code=status.HTTP_200_OK, response_model=RecipeCategory, deprecated=True)
async def read_recipe_category_by_name(*, db: Session = Depends(get_db), recipe_category_name: str):
    recipe_category_by_name = get_recipe_category_by_name(db, recipe_category_name=recipe_category_name)

    if recipe_category_by_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{recipe_category_name} name for Recipe Category is not found"
        )

    return recipe_category_by_name