from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query 
from sqlalchemy.orm import Session

from api.utils.recipe_category import *
from db.db_setup import get_db
from pydantic_schemas.recipe_category import RecipeCategory, RecipeCategoryCreate, RecipeCategoryCreatedResponse


router = APIRouter(tags=["Recipe Category"])

@router.get("/recipe_category_list", response_model=List[RecipeCategory])
async def read_recipe_categories(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    recipe_categories = get_recipe_categories(db, skip=skip, limit=limit)

    if not recipe_categories:
        raise HTTPException(
            status_code=404, 
            detail="Recipe Category list is empty"
        )

    return recipe_categories


@router.get("/recipe_category_by_id/{recipe_category_id}", response_model=RecipeCategory)
async def read_recipe_category_by_id(*, db: Session = Depends(get_db), recipe_category_id: int):
    recipe_category_by_id = get_recipe_category_by_id(db, recipe_category_id=recipe_category_id)

    if recipe_category_by_id is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{recipe_category_id} id for Recipe Category is not found"
        )

    return recipe_category_by_id


@router.get("/recipe_category_by_name/{recipe_category_name}", response_model=RecipeCategory)
async def read_recipe_category_by_name(*, db: Session = Depends(get_db), recipe_category_name: str):
    recipe_category_by_name = get_recipe_category_by_name(db, recipe_category_name=recipe_category_name)

    if recipe_category_by_name is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{recipe_category_name} name for Recipe Category is not found"
        )

    return recipe_category_by_name


@router.post("/recipe_category_create", status_code=201)
async def add_recipe_category(
    *, db: Session = Depends(get_db), 
    recipe_category: RecipeCategoryCreate
):
    recipe_category_by_name = get_recipe_category_by_name(db, recipe_category_name=recipe_category.name)
    
    if recipe_category_by_name:
        raise HTTPException(
            status_code=400, 
            detail=f"{recipe_category.name} as recipe Category is already registered"
        )

    recipe_category_create = create_recipe_category(db=db, recipe_category=recipe_category)

    result_message = f"{recipe_category.name} as recipe Category is successfully created"
    data = get_recipe_category_by_name(db, recipe_category_name=recipe_category.name)

    return {"result": result_message, "data": data}


@router.put("/recipe_category_update/{recipe_category_name}", status_code=202)
async def change_recipe_category(
    *, db: Session = Depends(get_db), 
    recipe_category_name: str, 
    recipe_category: RecipeCategoryCreate
):
    recipe_category_by_name = get_recipe_category_by_name(db, recipe_category_name=recipe_category_name)
    
    if not recipe_category_by_name:
        raise HTTPException(
            status_code=404, 
            detail=f"{recipe_category_name} as Recipe Category is not registered"
        )

    recipe_category_update = update_recipe_category(db=db, recipe_category_name=recipe_category_name, recipe_category=recipe_category)

    result_message = f"{recipe_category.name} as Recipe Category is successfully updated from {recipe_category_name}"
    data = get_recipe_category_by_name(db, recipe_category_name=recipe_category.name)

    return {"result": result_message, "data": data}


@router.delete("/recipe_category_delete/{recipe_category_name}", status_code=200)
async def remove_recipe_category(*, db: Session = Depends(get_db), recipe_category_name: str):
    recipe_category_by_name = get_recipe_category_by_name(db, recipe_category_name=recipe_category_name)

    if recipe_category_by_name is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{recipe_category_name} as Recipe Category is not found"
        )

    delete_recipe_category(db=db, recipe_category_name=recipe_category_name)
    result_message = f"{recipe_category_name} as Recipe Category is successfully deleted"

    return {"result": result_message}