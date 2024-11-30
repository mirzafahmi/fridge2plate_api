from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import os

from utils.recipe_image import get_recipe_images_by_recipe_id
from db.db_setup import get_db


router = APIRouter(
    prefix="/recipe_image",
    tags=["Recipe Image"])

UPLOAD_FOLDER = "uploads/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.get("/by_recipe_id/{recipe_id}", status_code=status.HTTP_200_OK)
async def read_recipe_image_by_recipe_id(*, db: Session = Depends(get_db), recipe_id: UUID):
    recipe_images = get_recipe_images_by_recipe_id(db, recipe_id)

    if not recipe_images:
        raise HTTPException(status_code=404, detail=f"Recipe image list for ID {recipe_id} of recipe is empty")

    return {
        "detail": f"Recipe image list of ID {recipe_id} of recipe is retrieved successfully",
        "recipe_images": recipe_images
    }
