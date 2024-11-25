from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.ingredient_category import *
from utils.user import check_valid_user, get_current_user
from db.db_setup import get_db
from pydantic_schemas.ingredient_category import IngredientCategory, IngredientCategoryCreate, IngredientCategoryUpdate, IngredientCategoryResponse, IngredientCategoriesResponse


router = APIRouter(
    prefix='/ingredient_categories', 
    tags=["Ingredient Categories"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=IngredientCategoriesResponse)
async def read_ingredient_categories(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), skip: int=0, limit: int = 100):
    ingredient_categories = get_ingredient_categories(db, skip=skip, limit=limit)

    if not ingredient_categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Ingredient Category list is empty"
        )

    return {
        "detail": "Ingredient Category list is retrieved successfully",
        "ingredient_categories": ingredient_categories
    }

@router.get("/{ingredient_category_id}", status_code=status.HTTP_200_OK, response_model=IngredientCategoryResponse)
async def read_ingredient_category_by_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), ingredient_category_id: UUID):
    ingredient_category_by_id = get_ingredient_category_by_id(db, ingredient_category_id=ingredient_category_id)

    if ingredient_category_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {ingredient_category_id} as Ingredient Category is not found"
        )
    
    return {
        "detail": f"Id {ingredient_category_id} as Ingredient Category is retrieved successfully",
        "ingredient_category": ingredient_category_by_id
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=IngredientCategoryResponse)
async def add_ingredient_category(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), ingredient_category: IngredientCategoryCreate):
    ingredient_category_by_name = get_ingredient_category_by_name(db, ingredient_category.name)

    if ingredient_category_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{ingredient_category.name} as Ingredient Category is already registered"
        )

    check_valid_user(db, ingredient_category)

    ingredient_category_create = post_ingredient_category(db, ingredient_category)

    result_message = f"{ingredient_category.name} as Ingredient Category is created successfully"

    return {"detail": result_message, "ingredient_category": ingredient_category_create}

@router.put("/{ingredient_category_id}", status_code=status.HTTP_202_ACCEPTED, response_model=IngredientCategoryResponse)
async def change_ingredient_category_by_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), ingredient_category_id: UUID, ingredient_category: IngredientCategoryUpdate):
    db_ingredient_category = get_ingredient_category_by_id(db, ingredient_category_id=ingredient_category_id)
    
    if not db_ingredient_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {ingredient_category_id} as Ingredient Category is not found"
        )

    check_valid_user(db, ingredient_category)

    ingredient_category_update = update_ingredient_category(db=db, ingredient_category_id=ingredient_category_id, ingredient_category=ingredient_category)
    result_message = f"Id {ingredient_category_id} as Ingredient Category is updated successfully"

    return {"detail": result_message, "ingredient_category": ingredient_category_update}


@router.delete("/{ingredient_category_id}", status_code=status.HTTP_200_OK)
async def remove_ingredient_category_by_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), ingredient_category_id: UUID):
    db_ingredient_category = get_ingredient_category_by_id(db, ingredient_category_id)

    if not db_ingredient_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {ingredient_category_id} as Ingredient Category is not found"
        )

    delete_ingredient_category(db, ingredient_category_id)
    result_message = f"Id {ingredient_category_id} as Ingredient Category is deleted successfully"

    return {"detail": result_message}

#TODO! convert all end point using name into using id
@router.get("/by_name/{ingredient_category_name}", status_code=status.HTTP_200_OK, response_model=IngredientCategory, deprecated=True)
async def read_ingredient_category_by_name(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), ingredient_category_name: str):
    ingredient_category_by_name = get_ingredient_category_by_name(db, ingredient_category_name=ingredient_category_name)

    if ingredient_category_by_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{ingredient_category_name} as Ingredient Category is not found"
        )

    return ingredient_category_by_name

@router.put("/by_name/{ingredient_category_name}", status_code=status.HTTP_202_ACCEPTED, deprecated=True)
async def change_ingredient_category_by_name(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), ingredient_category_name: str, ingredient_category: IngredientCategoryCreate):
    ingredient_category_by_name = get_ingredient_category_by_name(db, ingredient_category_name=ingredient_category_name)
    
    if not ingredient_category_by_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{ingredient_category_name} as Ingredient Category is not registered"
        )

    ingredient_category_update = update_ingredient_category_by_name(db=db, ingredient_category_name=ingredient_category_name, ingredient_category=ingredient_category)

    result_message = f"{ingredient_category.name} as Ingredient Category is successfully updated from {ingredient_category_name}"
    data = get_ingredient_category_by_name(db, ingredient_category_name=ingredient_category.name)

    return {"result": result_message, "data": data}


@router.delete("/by_name/{ingredient_category_name}", status_code=status.HTTP_200_OK, deprecated=True)
async def remove_ingredient_category_by_name(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), ingredient_category_name: str):
    ingredient_category_by_name = get_ingredient_category_by_name(db, ingredient_category_name=ingredient_category_name)

    if ingredient_category_by_name is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient Category is not found")

    delete_ingredient_category_by_name(db=db, ingredient_category_name=ingredient_category_name)
    result_message = f"{ingredient_category_name} as Ingredient Category is deleted successfully"

    return {"result": result_message}






