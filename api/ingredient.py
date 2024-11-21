from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.ingredient import *
from utils.ingredient_category import get_ingredient_category_by_id
from utils.user import get_user_by_id
from db.db_setup import get_db
from pydantic_schemas.ingredient import Ingredient, IngredientCreate, IngredientUpdate, IngredientResponse, IngredientsResponse


router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=IngredientsResponse)
async def read_ingredient(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    ingredients = get_ingredients(db, skip=skip, limit=limit)

    if not ingredients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient list is empty")

    return {
        "detail": f"Ingredient list is retrieved successfully",
        "ingredients": ingredients
    }


@router.get("/{ingredient_id}", status_code=status.HTTP_200_OK, response_model=IngredientResponse)
async def read_ingredient_by_id(*, db: Session = Depends(get_db), ingredient_id: UUID):
    ingredient_by_id = get_ingredient_by_id(db, ingredient_id=ingredient_id)

    if ingredient_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {ingredient_id} as Ingredient is not found"
        )

    return {
        "detail": f"Id {ingredient_id} as Ingredient Category is retrieved successfully",
        "ingredient": ingredient_by_id
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=IngredientResponse)
async def add_ingredient(
    *, db: Session = Depends(get_db), 
    ingredient: IngredientCreate
):
    ingredient_by_name = get_ingredient_by_name(db, ingredient.name)
    ingredient_category = get_ingredient_category_by_id(db, ingredient.ingredient_category_id)
    
    if ingredient_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{ingredient.name} as Ingredient is already registered"
        )
    
    if not ingredient_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {ingredient.ingredient_category_id} as Ingredient Category is not found"
        )

    ingredient_create = post_ingredient(db=db, ingredient=ingredient)

    result_message = f"{ingredient.name} as Ingredient is successfully created"

    return {"detail": result_message, "ingredient": ingredient_create}


@router.put("/{ingredient_id}", status_code=status.HTTP_202_ACCEPTED, response_model=IngredientResponse)
async def change_ingredient(
    *, db: Session = Depends(get_db), 
    ingredient: IngredientUpdate,
    ingredient_id: UUID, 
):
    db_ingredient = get_ingredient_by_id(db, ingredient_id)

    if not db_ingredient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Id {ingredient_id} as Ingredient is not found"
        )

    if ingredient.ingredient_category_id:
        ingredient_category = get_ingredient_category_by_id(db, ingredient.ingredient_category_id)
        
        if not ingredient_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Id {ingredient.ingredient_category_id} as Ingredient Category is not found"
            )
    
    if ingredient.created_by:
        creator_id = get_user_by_id(db, ingredient.created_by)

        if not creator_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Id {ingredient.created_by} as User is not found"
            )

    ingredient_update = put_ingredient(db, ingredient_id, ingredient)

    result_message = f"Id {ingredient_id} as Ingredient is successfully updated"

    return {"detail": result_message, "ingredient": ingredient_update}

@router.delete("/{ingredient_id}", status_code=status.HTTP_200_OK)
async def remove_ingredient(*, db: Session = Depends(get_db), ingredient_id: UUID):
    ingredient_by_id = get_ingredient_by_id(db, ingredient_id)

    if ingredient_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {ingredient_id} as Ingredient is not found"
        )

    delete_ingredient(db, ingredient_id)
    result_message = f"Id {ingredient_id} as Ingredient is successfully deleted"

    return {"detail": result_message}






@router.get("/by_name/{ingredient_name}", status_code=status.HTTP_200_OK, response_model=Ingredient, deprecated=True)
async def read_ingredient_by_name(*, db: Session = Depends(get_db), ingredient_name: str):
    ingredient_by_name = get_ingredient_by_name(db, ingredient_name=ingredient_name)

    if ingredient_by_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{ingredient_name} as Ingredient is not found"
        )

    return ingredient_by_name

@router.get("/by_category/{ingredient_category}", status_code=status.HTTP_200_OK, response_model=List[Ingredient], deprecated=True)
async def read_ingredient_by_category(*, db: Session = Depends(get_db), ingredient_category: str):
    ingredient_by_category = get_ingredient_by_category(db, ingredient_category=ingredient_category)

    if ingredient_by_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{ingredient_category} as Ingredient Category is not found"
        )

    return ingredient_by_category