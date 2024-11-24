from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.recipe import *
from utils.ingredient_recipe_association import *
from utils.recipe_category import get_recipe_category_by_id
from utils.recipe_tag import get_recipe_tag_by_id
from utils.recipe_origin import get_recipe_origin_by_id

from db.db_setup import get_db
from pydantic_schemas.recipe import Recipe, RecipeCreate, RecipeUpdate, RecipeResponse, RecipesResponse, RecipeLiteResponse, RecipesLiteResponse


router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=RecipesResponse)
async def read_recipes(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    recipes = get_recipes(db, skip=skip, limit=limit)

    if not recipes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipe list is empty"
        )

    return {
        "detail": "Recipe list is retrieved successfully",
        "recipes": recipes
    }

@router.get("/lite", status_code=status.HTTP_200_OK, response_model=RecipesLiteResponse)
async def read_recipes(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    recipes = get_recipes(db, skip=skip, limit=limit)

    if not recipes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recipe list is empty"
        )

    return {
        "detail": "Recipe list Lite is retrieved successfully",
        "recipes": recipes
    }

@router.get("/{recipe_id}", status_code=status.HTTP_200_OK, response_model=RecipeResponse)
async def read_recipe_by_id(*, db: Session = Depends(get_db), recipe_id: UUID):
    recipe_by_id = get_recipe_by_id(db, recipe_id)

    if recipe_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe_id} as Recipe is not found"
        )

    return {
        "detail": f"Id {recipe_id} as Recipe is retrieved successfully",
        "recipe": recipe_by_id
    }

@router.get("/{recipe_id}/lite", status_code=status.HTTP_200_OK, response_model=RecipeLiteResponse)
async def read_recipe_by_id(*, db: Session = Depends(get_db), recipe_id: UUID):
    recipe_by_id = get_recipe_by_id(db, recipe_id)

    if recipe_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe_id} as Recipe is not found"
        )

    return {
        "detail": f"Id {recipe_id} as Recipe Lite is retrieved successfully",
        "recipe": recipe_by_id
    }

#remove unique name
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RecipeLiteResponse)
async def add_recipe(*, db: Session = Depends(get_db), recipe: RecipeCreate):
    recipe_category = get_recipe_category_by_id(db, recipe.recipe_category_id)
    
    if not recipe_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe.recipe_category_id} as Recipe Category is not found"
        )
    
    recipe_origin = get_recipe_origin_by_id(db, recipe.recipe_origin_id)

    if not recipe_origin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe.recipe_origin_id} as Recipe Origin is not found"
        )
    for recipe_tag in recipe.recipe_tags:
        recipe_tag = get_recipe_tag_by_id(db, recipe_tag)

        if not recipe_tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Id {recipe_tag} as Recipe Tag is not found"
            )
            
    recipe_create = post_recipe(db, recipe)

    result_message = f"{recipe.name} as Recipe is successfully created"

    return {"detail": result_message,"recipe": recipe_create}

@router.put("/{recipe_id}", status_code=status.HTTP_202_ACCEPTED, response_model=RecipeResponse)
async def change_recipe(*, db: Session = Depends(get_db), recipe_name: str, recipe: RecipeUpdate):
    recipe_by_name = get_recipe_by_name(db, recipe_name)

    if not recipe_by_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{recipe.name} as Recipe is not found"
        )

    if recipe.recipe_category_id:
        recipe_category = get_recipe_category_by_name(db, recipe.recipe_category)

        if not recipe_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"{recipe.recipe_category} as Recipe Category is not found"
            )

    if recipe.recipe_tag_id:
        recipe_tag = get_recipe_tag_by_name(db, recipe.recipe_tag)

        if not recipe_tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"{recipe.recipe_tag} as Recipe Tag is not found"
            )

    if recipe.recipe_origin_id:
        recipe_origin = get_recipe_origin_by_name(db, recipe.recipe_origin)

        if not recipe_origin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"{recipe.recipe_origin} as Recipe Origin is not found"
            )

    try:
        recipe_update = update_recipe(
            db=db, 
            recipe_name=recipe_name,
            recipe=recipe, 
        )

        if recipe.ingredients:
            delete_association(db, recipe_by_name.id)

            for ingredient in recipe.ingredients:

                update_association(db=db, recipe_id=recipe_by_name.id, ingredient=ingredient)

    except:
        db.rollback()
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error creating {recipe.name} as Recipe: {str(e)}"
        )


    if recipe.name is not None:
        data = get_recipe_by_name(db, recipe.name)
    else:
        data = get_recipe_by_name(db, recipe_name)

    return data


@router.delete("/{recipe_id}", status_code=status.HTTP_200_OK)
async def remove_recipe(*, db: Session = Depends(get_db), recipe_id: UUID):
    recipe_by_id = get_recipe_by_id(db, recipe_id)

    if not recipe_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {recipe_id} as Recipe is not found"
        )

    delete_recipe(db, recipe_id)
    result_message = f"Id {recipe_id} as Recipe is successfully deleted"

    return {"detail": result_message}



@router.get("/by_name/{recipe_name}", status_code=status.HTTP_200_OK, response_model=Recipe, deprecated=True)
async def read_recipe_by_name(*, db: Session = Depends(get_db), recipe_name: str):
    recipe_by_name = get_recipe_by_name(db, recipe_name=recipe_name)

    if recipe_by_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{recipe_name} as Recipe is not found"
        )

    return recipe_by_name