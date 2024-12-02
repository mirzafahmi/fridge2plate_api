from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import os

from utils.recipe_image import get_recipe_images, get_recipe_image_by_id, get_recipe_images_by_recipe_id, post_recipe_image, put_recipe_image, delete_recipe_image
from utils.recipe import get_recipe_by_id
from pydantic_schemas.recipe_image import RecipeImageCreate, RecipeImageUpdate, RecipeImageResponse, RecipeImagesResponse
from db.db_setup import get_db


router = APIRouter(
    prefix="/recipe_image",
    tags=["Recipe Image"])

UPLOAD_FOLDER = "uploads/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.get("/", status_code=status.HTTP_200_OK, response_model=RecipeImagesResponse)
async def read_recipe_images(*, db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    db_recipe_images = get_recipe_images(db, skip=skip, limit=limit)

    if not db_recipe_images:
        raise HTTPException(status_code=404, detail="Recipe Images list is empty")

    return {
        "detail": f"Recipe Images list is retrieved successfully",
        "recipe_images": db_recipe_images
    }

@router.get("/{recipe_image_id}", status_code=status.HTTP_200_OK, response_model=RecipeImageResponse)
async def read_recipe_image_by_recipe_id(*, db: Session = Depends(get_db), recipe_image_id: UUID):
    db_recipe_image = get_recipe_image_by_id(db, recipe_image_id)

    if not db_recipe_image:
        raise HTTPException(
            status_code=404, 
            detail=f"ID {recipe_image_id} as Recipe Image is not found"
        )

    return {
        "detail": f"ID {recipe_image_id} as Recipe Image is retrieved successfully",
        "recipe_image": db_recipe_image
    }

@router.get("/by_recipe_id/{recipe_id}", status_code=status.HTTP_200_OK, response_model=RecipeImagesResponse)
async def read_recipe_image_by_recipe_id(*, db: Session = Depends(get_db), recipe_id: UUID):
    recipe_images = get_recipe_images_by_recipe_id(db, recipe_id)

    if not recipe_images:
        raise HTTPException(status_code=404, detail=f"Recipe image list for ID {recipe_id} of recipe is empty")

    return {
        "detail": f"Recipe image list of ID {recipe_id} of recipe is retrieved successfully",
        "recipe_images": recipe_images
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RecipeImagesResponse)
async def add_recipe_image(*, db: Session = Depends(get_db), recipe_image: RecipeImageCreate):
    db_recipe = get_recipe_by_id(db, recipe_image.recipe_id)

    if not db_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_image.recipe_id} as Recipe is not found"
        )

    recipe_image_create = post_recipe_image(db, recipe_image)
    result_message = f"{recipe_image.image} of Recipe Image is created successfully for ID {recipe_image.recipe_id} of Recipe"

    return {
        "detail": result_message, 
        "recipe_images": 
            [  
                {"id": img.id, "image": img.image, "recipe_id": img.recipe_id} for img in recipe_image_create
            ]
    }

@router.put("/{recipe_image_id}", status_code=status.HTTP_202_ACCEPTED, response_model=RecipeImageResponse)
async def change_recipe_image(*, db: Session = Depends(get_db), recipe_image_id: UUID, recipe_image: RecipeImageUpdate):
    db_recipe_image = get_recipe_image_by_id(db, recipe_image_id)

    if not db_recipe_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_image_id} as Recipe Image is not found"
        )
    
    if hasattr(recipe_image, 'recipe_id') and recipe_image.recipe_id is not None:
        db_recipe = get_recipe_by_id(db, recipe_image.recipe_id)

        if not db_recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"ID {recipe_image.recipe_id} as Recipe is not found"
            )
    
    if not any(value is not None for value in recipe_image.dict().values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must include at least one field to update"
        )
    
    recipe_image_update = put_recipe_image(db, recipe_image_id, recipe_image)
    result_message = f"ID {recipe_image_id} of Recipe Image is updated successfully for ID {db_recipe_image.recipe_id} of Recipe"

    return {"detail": result_message, "recipe_image": recipe_image_update}


@router.delete("/{recipe_image_id}", status_code=status.HTTP_200_OK)
async def remove_recipe_image(*, db: Session = Depends(get_db), recipe_image_id: UUID):
    db_recipe_image = get_recipe_image_by_id(db, recipe_image_id)

    if not db_recipe_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_image_id} as Recipe Image is not found"
        )

    delete_recipe_image(db, recipe_image_id)
    result_message = f"ID {recipe_image_id} as Recipe Image for ID {db_recipe_image.recipe_id} of Recipe is deleted successfully"

    return {"detail": result_message}