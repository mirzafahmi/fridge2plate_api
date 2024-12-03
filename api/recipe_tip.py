from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from db.db_setup import get_db
from utils.recipe_tip import *
from utils.recipe import get_recipe_by_id
from pydantic_schemas.recipe_tip import RecipeTipResponse, RecipeTipsResponse


router = APIRouter(
    prefix="/recipe_tip",
    tags=["Recipe Tip"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=RecipeTipsResponse)
async def read_recipe_tip_by_recipe_id(*, db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    db_recipe_tips = get_recipe_tips(db, skip=skip, limit=limit)

    if not db_recipe_tips:
        raise HTTPException(status_code=404, detail="Recipe Tip list is empty")

    return {
        "detail": f"Recipe Tip list is retrieved successfully",
        "recipe_tips": db_recipe_tips
    }

@router.get("/{recipe_tip_id}", status_code=status.HTTP_200_OK, response_model=RecipeTipResponse)
async def read_recipe_tip_by_recipe_id(*, db: Session = Depends(get_db), recipe_tip_id: UUID):
    db_recipe_tip = get_recipe_tip_by_id(db, recipe_tip_id)

    if not db_recipe_tip:
        raise HTTPException(
            status_code=404, 
            detail=f"ID {recipe_tip_id} as Recipe Tip is not found"
        )

    return {
        "detail": f"ID {recipe_tip_id} as Recipe Tip is retrieved successfully",
        "recipe_tip": db_recipe_tip
    }

@router.get("/by_recipe_id/{recipe_id}", status_code=status.HTTP_200_OK, response_model=RecipeTipsResponse)
async def read_recipe_tip_by_recipe_id(*, db: Session = Depends(get_db), recipe_id: UUID):
    recipe_tips = get_recipe_tips_by_recipe_id(db, recipe_id)

    if not recipe_tips:
        raise HTTPException(
            status_code=404, 
            detail=f"Recipe Tip list for ID {recipe_id} of recipe is empty"
        )

    return {
        "detail": f"Recipe Tip list of ID {recipe_id} of recipe is retrieved successfully",
        "recipe_tips": recipe_tips
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RecipeTipsResponse)
async def add_recipe_tip(*, db: Session = Depends(get_db), recipe_tip: RecipeTipCreate):
    db_recipe = get_recipe_by_id(db, recipe_tip.recipe_id)

    if not db_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_tip.recipe_id} as Recipe is not found"
        )
    
    for tip in recipe_tip.description:
        db_recipe_tip = check_recipe_tip_duplication(db, recipe_tip.recipe_id, tip)

        if db_recipe_tip:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail=f"{tip} of Recipe Tip for ID {recipe_tip.recipe_id} of Recipe is already registered"
            )

    recipe_tip_create = post_recipe_tip(db, recipe_tip)
    result_message = f"{len(recipe_tip_create)} of Recipe Tip is created successfully for ID {recipe_tip.recipe_id} of Recipe"

    return {
        "detail": result_message, 
        "recipe_tips": [  
                {"id": tip.id, "description": tip.description, "recipe_id": tip.recipe_id} for tip in recipe_tip_create
            ]
    }

@router.put("/{recipe_tip_id}", status_code=status.HTTP_202_ACCEPTED, response_model=RecipeTipResponse)
async def change_recipe_tip(*, db: Session = Depends(get_db), recipe_tip_id: UUID, recipe_tip: RecipeTipUpdate):
    db_recipe_tip = get_recipe_tip_by_id(db , recipe_tip_id)

    if not db_recipe_tip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_tip_id} as Recipe Tip is not found"
        )

    if not any(value is not None for value in recipe_tip.dict().values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must include at least one field to update"
        )
    print(recipe_tip)
    recipe_tip_update = put_recipe_tip(db, recipe_tip_id, recipe_tip)
    result_message = f"ID {recipe_tip_id} of Recipe Tip is updated successfully for ID {db_recipe_tip.recipe_id} of Recipe"

    return {"detail": result_message, "recipe_tip": recipe_tip_update}

@router.delete("/{recipe_tip_id}", status_code=status.HTTP_200_OK)
async def remove_recipe_tip(*, db: Session = Depends(get_db), recipe_tip_id: UUID):
    db_recipe_tip = get_recipe_tip_by_id(db , recipe_tip_id)

    if not db_recipe_tip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_tip_id} as Recipe Tip is not found"
        )

    delete_recipe_tip(db, recipe_tip_id)
    result_message = f"ID {recipe_tip_id} as Recipe Tip is deleted successfully for ID {db_recipe_tip.recipe_id} of Recipe"

    return {"detail": result_message}