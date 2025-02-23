from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.recipe_origin import *
from utils.user import check_valid_user
from utils.auth import get_current_user
from db.db_setup import get_db
from pydantic_schemas.recipe_origin import RecipeOrigin, RecipeOriginCreate, RecipeOriginUpdate, RecipeOriginResponse, RecipeOriginsResponse


router = APIRouter(
    prefix="/recipe_origins",
    tags=["Recipe Origins"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=RecipeOriginsResponse)
async def read_recipe_origin(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), skip: int=0, limit: int = 100):
    recipe_origins = get_recipe_origins(db, skip=skip, limit=limit)

    if not recipe_origins:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipe Origin list is empty"
        )

    return {
        "detail": "Recipe Origin list is retrieved successfully",
        "recipe_origins": recipe_origins
    }

@router.get("/{recipe_origin_id}", status_code=status.HTTP_200_OK, response_model=RecipeOriginResponse)
async def read_recipe_origin_by_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_origin_id: UUID):
    recipe_origin_by_id = get_recipe_origin_by_id(db, recipe_origin_id)

    if recipe_origin_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe_origin_id} as Recipe Origin is not found"
        )

    return {
        "detail": f"Id {recipe_origin_id} as Recipe Origin is retrieved successfully",
        "recipe_origin": recipe_origin_by_id
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RecipeOriginResponse)
async def add_recipe_origin(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_origin: RecipeOriginCreate):
    recipe_origin_by_name = get_recipe_origin_by_name(db, recipe_origin_name=recipe_origin.name)
    
    if recipe_origin_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{recipe_origin.name} as Recipe Origin is already registered"
        )

    check_valid_user(db, recipe_origin)

    recipe_origin_create = post_recipe_origin(db, recipe_origin)

    result_message = f"{recipe_origin.name} as Recipe Origin is created successfully"

    return {"detail": result_message, "recipe_origin": recipe_origin_create}

@router.put("/{recipe_origin_id}", status_code=status.HTTP_202_ACCEPTED, response_model=RecipeOriginResponse)
async def change_recipe_origin(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_origin_id: UUID, recipe_origin: RecipeOriginUpdate):
    recipe_origin_by_id = get_recipe_origin_by_id(db, recipe_origin_id)
    
    if not recipe_origin_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe_origin_id} as Recipe Origin is not found"
        )

    check_valid_user(db, recipe_origin)
    
    recipe_origin_update = put_recipe_origin(db, recipe_origin_id, recipe_origin)
    result_message = f"Id {recipe_origin_id} as Recipe Origin is updated successfully"

    return {"detail": result_message, "recipe_origin": recipe_origin_update}


@router.delete("/{recipe_origin_id}", status_code=status.HTTP_200_OK)
async def remove_recipe_origin(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_origin_id: UUID):
    recipe_origin_by_id = get_recipe_origin_by_id(db, recipe_origin_id)

    if not recipe_origin_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe_origin_id} as Recipe Origin is not found"
        )

    delete_recipe_origin(db, recipe_origin_id)
    result_message = f"Id {recipe_origin_id} as Recipe Origin is deleted successfully"

    return {"detail": result_message}




@router.get("/by_name/{recipe_origin_name}", status_code=status.HTTP_200_OK, response_model=RecipeOrigin, deprecated=True)
async def read_recipe_origin_by_name(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_origin_name: str):
    recipe_origin_by_name = get_recipe_origin_by_name(db, recipe_origin_name=recipe_origin_name)

    if recipe_origin_by_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{recipe_origin_name} as Recipe Origin is not found"
        )

    return recipe_origin_by_name