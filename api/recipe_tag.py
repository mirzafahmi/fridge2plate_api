from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from api.utils.recipe_tag import *
from db.db_setup import get_db
from pydantic_schemas.recipe_tag import RecipeTag, RecipeTagCreate, RecipeTagCreatedResponse


router = APIRouter(
    prefix="/recipe_tags",
    tags=["Recipe Tags"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[RecipeTag])
async def read_recipe_tags(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    recipe_tags = get_recipe_tags(db, skip=skip, limit=limit)

    if not recipe_tags:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipe Tag list is empty"
        )

    return recipe_tags


@router.get("{recipe_tag_id}", status_code=status.HTTP_200_OK, response_model=RecipeTag)
async def read_recipe_tag_by_id(*, db: Session = Depends(get_db), recipe_tag_id: int):
    recipe_tag_by_id = get_recipe_tag_by_id(db, recipe_tag_id=recipe_tag_id)

    if recipe_tag_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{recipe_tag_id} as Recipe Tag is not found"
        )

    return recipe_tag_by_id


@router.get("by_name/{recipe_tag_name}", status_code=status.HTTP_200_OK, response_model=RecipeTag)
async def read_recipe_tag_by_name(*, db: Session = Depends(get_db), recipe_tag_name: str):
    recipe_tag_by_name = get_recipe_tag_by_name(db, recipe_tag_name=recipe_tag_name)

    if recipe_tag_by_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{recipe_tag_name} as Recipe Tag is not found"
        )

    return recipe_tag_by_name


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_recipe_tag(
    *, db: Session = Depends(get_db), 
    recipe_tag: RecipeTagCreate
):
    recipe_tag_by_name = get_recipe_tag_by_name(db, recipe_tag_name=recipe_tag.name)
    
    if recipe_tag_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{recipe_tag.name} as Recipe Tag is already registered"
        )

    recipe_tag_create = create_recipe_tag(db=db, recipe_tag=recipe_tag)

    result_message = f"{recipe_tag.name} as Recipe Tag is successfully created"
    data = get_recipe_tag_by_name(db, recipe_tag_name=recipe_tag.name)

    return {"result": result_message, "data": data}


@router.put("/{recipe_tag_name}", status_code=status.HTTP_202_ACCEPTED)
async def change_recipe_tag(
    *, db: Session = Depends(get_db), 
    recipe_tag_name: str, 
    recipe_tag: RecipeTagCreate
):
    recipe_tag_by_name = get_recipe_tag_by_name(db, recipe_tag_name=recipe_tag_name)
    
    if not recipe_tag_by_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{recipe_tag_name} as Recipe tag is not registered"
        )

    recipe_tag_update = update_recipe_tag(db=db, recipe_tag_name=recipe_tag_name, recipe_tag=recipe_tag)

    result_message = f"{recipe_tag.name} as Recipe tag is successfully updated from {recipe_tag_name}"
    data = get_recipe_tag_by_name(db, recipe_tag_name=recipe_tag.name)

    return {"result": result_message, "data": data}


@router.delete("/{recipe_tag_name}", status_code=status.HTTP_200_OK)
async def remove_recipe_tag(*, db: Session = Depends(get_db), recipe_tag_name: str):
    recipe_tag_by_name = get_recipe_tag_by_name(db, recipe_tag_name=recipe_tag_name)

    if recipe_tag_by_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{recipe_tag_name} as Recipe tag is not found"
        )

    delete_recipe_tag(db=db, recipe_tag_name=recipe_tag_name)
    result_message = f"{recipe_tag_name} as Recipe tag is successfully deleted"

    return {"result": result_message}