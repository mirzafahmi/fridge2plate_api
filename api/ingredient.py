from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query 
from sqlalchemy.orm import Session

from api.utils.ingredient import *
from api.utils.ingredient_category import get_ingredient_category_by_name
from db.db_setup import get_db
from pydantic_schemas.ingredient import Ingredient, IngredientCreate, IngredientUpdate, IngredientCreatedResponse


router = APIRouter(tags=["Ingredient List"])

@router.get("/ingredient_list", response_model=List[Ingredient])
async def read_ingredient(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    ingredients = get_ingredients(db, skip=skip, limit=limit)

    if not ingredients:
        raise HTTPException(status_code=404, detail="Ingredient list is empty")

    return ingredients


@router.get("/ingredient_id/{ingredient_id}", response_model=Ingredient)
async def read_ingredient_by_id(*, db: Session = Depends(get_db), ingredient_id: int):
    ingredient_by_id = get_ingredient_by_id(db, ingredient_id=ingredient_id)

    if ingredient_by_id is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{ingredient_id} as Ingredient is not found"
        )

    return ingredient_by_id


@router.get("/ingredient_name/{ingredient_name}", response_model=Ingredient)
async def read_ingredient_by_name(*, db: Session = Depends(get_db), ingredient_name: str):
    ingredient_by_name = get_ingredient_by_name(db, ingredient_name=ingredient_name)

    if ingredient_by_name is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{ingredient_name} as Ingredient is not found"
        )

    return ingredient_by_name

@router.get("/ingredient_by_category/{ingredient_category}", response_model=List[Ingredient])
async def read_ingredient_by_category(*, db: Session = Depends(get_db), ingredient_category: str):
    ingredient_by_category = get_ingredient_by_category(db, ingredient_category=ingredient_category)

    if ingredient_by_category is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{ingredient_category} as Ingredient Category is not found"
        )

    return ingredient_by_category


@router.post("/ingredient_create", status_code=201, response_model=Ingredient)
async def add_ingredient(
    *, db: Session = Depends(get_db), 
    ingredient: IngredientCreate
):
    ingredient_by_name = get_ingredient_by_name(db, ingredient.name)
    ingredient_category = get_ingredient_category_by_name(db, ingredient.ingredient_category_name)
    
    if ingredient_by_name:
        raise HTTPException(
            status_code=400, 
            detail=f"{ingredient.name} as Ingredient is already registered"
        )
    
    if not ingredient_category:
        raise HTTPException(
            status_code=400, 
            detail=f"{ingredient.ingredient_category} as Ingredient Category is not found"
        )

    ingredient_create = create_ingredient_by_name(db=db, ingredient=ingredient)

    result_message = f"{ingredient.name} as Ingredient is successfully created"
    data = get_ingredient_by_name(db, ingredient_name=ingredient.name)


    return data


@router.put("/ingredient_update/{ingredient_name}", status_code=200, response_model=Ingredient)
async def change_ingredient(
    *, db: Session = Depends(get_db), 
    ingredient: IngredientUpdate,
    ingredient_name: str, 
):
    ingredient_by_name = get_ingredient_by_name(db, ingredient.name)
    path_ingredient_name = get_ingredient_by_name(db, ingredient_name)

    if ingredient_by_name:
        raise HTTPException(
            status_code=400, 
            detail=f"{ingredient.name} as Ingredient is already registered"
        )
    
    if not path_ingredient_name:
        raise HTTPException(
            status_code=400, 
            detail=f"{ingredient_name} as Ingredient is not registered"
        )

    if ingredient.ingredient_category:
        ingredient_category = get_ingredient_category_by_name(db, ingredient.ingredient_category)
        
        if not ingredient_category:
            raise HTTPException(
                status_code=400, 
                detail=f"{ingredient.ingredient_category} as Ingredient Category is not register"
            )

    ingredient_update = update_ingredient(
        db=db, 
        ingredient=ingredient, 
        ingredient_name=ingredient_name,
        )

    result_message = f"{ingredient.name} as Ingredient is successfully updated"

    if ingredient.name is not None:
        data = get_ingredient_by_name(db, ingredient.name)
    else:
        data = get_ingredient_by_name(db, ingredient_name=ingredient_name)

    return data


@router.delete("/ingredient_delete/{ingredient_name}", status_code=200)
async def remove_ingredient(*, db: Session = Depends(get_db), ingredient_name: str):
    ingredient_by_name = get_ingredient_by_name(db, ingredient_name=ingredient_name)

    if ingredient_by_name is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{ingredient_name} as Recipe Category is not found"
        )

    delete_ingredient(db=db, ingredient_name=ingredient_name)
    result_message = f"{ingredient_name} as Recipe Category is successfully deleted"

    return {"result": result_message}