from fastapi import APIRouter, Depends, HTTPException, Query, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from uuid import UUID

from db.db_setup import get_db

from utils.user import get_current_user
from utils.ingredient import get_ingredients
from utils.recipe_category import get_recipe_categories
from utils.recipe_tag import get_recipe_tags
from utils.recipe_origin import  get_recipe_origins
from utils.uom import get_uoms

from pydantic_schemas.recipe import RecipeFormFieldsResponse

router = APIRouter(
    prefix="/recipe_form",
    tags=["Recipe Form"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=RecipeFormFieldsResponse)
async def read_recipe_form_fields(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    recipe_categories = get_recipe_categories(db)
    recipe_origins = get_recipe_origins(db)
    recipe_tags = get_recipe_tags(db)
    ingredients = get_ingredients(db)
    uoms = get_uoms(db)

    form_fields = {
        "recipe_categories": recipe_categories,
        "recipe_origins": recipe_origins,
        "recipe_tags": recipe_tags,
        "ingredients": ingredients,
        "uoms": uoms
    }

    return {
        "detail": "Recipe form field is retrieved successfully",
        "recipe_form_fields": form_fields
    }