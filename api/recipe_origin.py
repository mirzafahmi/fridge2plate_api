from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query 
from sqlalchemy.orm import Session

from api.utils.recipe_origin import *
from db.db_setup import get_db
from pydantic_schemas.recipe_origin import RecipeOrigin, RecipeOriginCreate, RecipeOriginCreatedResponse


router = APIRouter(tags=["Recipe Origin"])

@router.get("/recipe_origin_list", response_model=List[RecipeOrigin])
async def read_recipe_origin(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    recipe_origins = get_recipe_origins(db, skip=skip, limit=limit)

    if not recipe_origins:
        raise HTTPException(status_code=404, detail="Recipe Origin list is empty")

    return recipe_origins


@router.get("/recipe_origin_id/{recipe_origin_id}", response_model=RecipeOrigin)
async def read_recipe_origin_by_id(*, db: Session = Depends(get_db), recipe_origin_id: int):
    recipe_origin_by_id = get_recipe_origin_by_id(db, recipe_origin_id=recipe_origin_id)

    if recipe_origin_by_id is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{recipe_origin_id} as Recipe Origin is not found"
        )

    return recipe_origin_by_id


@router.get("/recipe_origin_name/{recipe_origin_name}", response_model=RecipeOrigin)
async def read_recipe_origin_by_name(*, db: Session = Depends(get_db), recipe_origin_name: str):
    recipe_origin_by_name = get_recipe_origin_by_name(db, recipe_origin_name=recipe_origin_name)

    if recipe_origin_by_name is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{recipe_origin_name} as Recipe Origin is not found"
        )

    return recipe_origin_by_name


@router.post("/recipe_origin_create", status_code=201)
async def add_recipe_origin(
    *, db: Session = Depends(get_db), 
    recipe_origin: RecipeOriginCreate
):
    recipe_origin_by_name = get_recipe_origin_by_name(db, recipe_origin_name=recipe_origin.name)
    
    if recipe_origin_by_name:
        raise HTTPException(
            status_code=400, 
            detail=f"{recipe_origin.name} as Recipe Tag is already registered"
        )

    recipe_origin_create = create_recipe_origin(db=db, recipe_origin=recipe_origin)

    result_message = f"{recipe_origin.name} as Recipe Tag is successfully created"
    data = get_recipe_origin_by_name(db, recipe_origin_name=recipe_origin.name)

    return {"result": result_message, "data": data}


@router.put("/recipe_origin_update/{recipe_origin_name}", status_code=202)
async def change_recipe_origin(
    *, db: Session = Depends(get_db), 
    recipe_origin_name: str, 
    recipe_origin: RecipeOriginCreate
):
    recipe_origin_by_name = get_recipe_origin_by_name(db, recipe_origin_name=recipe_origin_name)
    
    if not recipe_origin_by_name:
        raise HTTPException(
            status_code=404, 
            detail=f"{recipe_origin_name} as Recipe tag is not registered"
        )

    recipe_origin_update = update_recipe_origin(db=db, recipe_origin_name=recipe_origin_name, recipe_origin=recipe_origin)

    result_message = f"{recipe_origin.name} as Recipe tag is successfully updated from {recipe_origin_name}"
    data = get_recipe_origin_by_name(db, recipe_origin_name=recipe_origin.name)

    return {"result": result_message, "data": data}


@router.delete("/recipe_origin_delete/{recipe_origin_name}", status_code=200)
async def remove_recipe_origin(*, db: Session = Depends(get_db), recipe_origin_name: str):
    recipe_origin_by_name = get_recipe_origin_by_name(db, recipe_origin_name=recipe_origin_name)

    if recipe_origin_by_name is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{recipe_origin_name} as Recipe tag is not found"
        )

    delete_recipe_origin(db=db, recipe_origin_name=recipe_origin_name)
    result_message = f"{recipe_origin_name} as Recipe tag is successfully deleted"

    return {"result": result_message}