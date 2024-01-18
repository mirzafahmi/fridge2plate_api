from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query 
from sqlalchemy.orm import Session

from api.utils.ingredient import *
from db.db_setup import get_db
from pydantic_schemas.ingredient import Ingredient, IngredientCreate, IngredientCreatedResponse


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


@router.post("/ingredient_create", status_code=201)
async def add_ingredient(
    *, db: Session = Depends(get_db), 
    ingredient: IngredientCreate
):
    ingredient_by_name = get_ingredient_by_name(db, ingredient_name=ingredient.name)
    
    if ingredient_by_name:
        raise HTTPException(
            status_code=400, 
            detail=f"{ingredient.name} as Recipe Tag is already registered"
        )

    ingredient_create = create_ingredient(db=db, ingredient=ingredient)

    result_message = f"{ingredient.name} as Recipe Tag is successfully created"
    data = get_ingredient_by_name(db, ingredient_name=ingredient.name)

    return {"result": result_message, "data": data}