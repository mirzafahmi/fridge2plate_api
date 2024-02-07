from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query 
from sqlalchemy.orm import Session

from api.utils.recipe import *
from api.utils.ingredient_recipe_association import *
from api.utils.recipe_category import get_recipe_category_by_name
from api.utils.recipe_tag import get_recipe_tag_by_name
from api.utils.recipe_origin import get_recipe_origin_by_name

from db.db_setup import get_db
from pydantic_schemas.recipe import Recipe, RecipeCreate, RecipeCreatedResponse, RecipeUpdate


router = APIRouter(tags=["Recipe List"])

@router.get("/recipe_list", response_model=List[Recipe])
async def read_recipes(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    recipes = get_recipes(db, skip=skip, limit=limit)

    if not recipes:
        raise HTTPException(status_code=404, detail="Recipe list is empty")

    return recipes


@router.get("/recipe_id/{recipe_id}", response_model=Recipe)
async def read_recipe_by_id(*, db: Session = Depends(get_db), recipe_id: int):
    recipe_by_id = get_recipe_by_id(db, recipe_id=recipe_id)

    if recipe_by_id is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Id {recipe_id} as Recipe is not found"
        )

    return recipe_by_id


@router.get("/recipe_name/{recipe_name}", response_model=Recipe)
async def read_recipe_by_name(*, db: Session = Depends(get_db), recipe_name: str):
    recipe_by_name = get_recipe_by_name(db, recipe_name=recipe_name)

    if recipe_by_name is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{recipe_name} as Recipe is not found"
        )

    return recipe_by_name


@router.post("/recipe_create", status_code=201, response_model=Recipe)
async def add_recipe(
    *, db: Session = Depends(get_db), 
    recipe: RecipeCreate
):
    recipe_by_name = get_recipe_by_name(db, recipe.name)
    recipe_category = get_recipe_category_by_name(db, recipe.recipe_category)
    recipe_tag = get_recipe_tag_by_name(db, recipe.recipe_tag)
    recipe_origin = get_recipe_origin_by_name(db, recipe.recipe_origin)
    
    if recipe_by_name:
        raise HTTPException(
            status_code=400, 
            detail=f"{recipe.name} as recipe is already registered"
        )
    
    if not recipe_category:
        raise HTTPException(
            status_code=400, 
            detail=f"{recipe.recipe_category} as Recipe Category is not found"
        )
    
    if not recipe_tag:
        raise HTTPException(
            status_code=400, 
            detail=f"{recipe.recipe_tag} as Recipe Tag is not found"
        )
    
    if not recipe_origin:
        raise HTTPException(
            status_code=400, 
            detail=f"{recipe.recipe_origin} as Recipe Origin is not found"
        )

    try:
        recipe_create = create_recipe(db=db, recipe=recipe)

        for ingredient in recipe.ingredients:

            create_association(db=db, recipe_id=recipe_create.id, ingredient=ingredient)

    except:
        raise HTTPException(
            status_code=500, 
            detail=f"Error creating {recipe.name} as Recipe: {str(e)}"
        )

    result_message = f"{recipe.name} as Recipe is successfully created"
    data = get_recipe_by_name(db, recipe_name=recipe.name)


    return data


@router.put("/recipe_update/{recipe_name}", status_code=200, response_model=Recipe)
async def change_recipe(
    *, db: Session = Depends(get_db), 
    recipe_name: str, 
    recipe: RecipeUpdate,    
):

    recipe_by_name = get_recipe_by_name(db, recipe_name)

    if not recipe_by_name:
        raise HTTPException(
            status_code=400, 
            detail=f"{recipe.name} as Recipe is not found"
        )

    if recipe.recipe_category_id:
        recipe_category = get_recipe_category_by_name(db, recipe.recipe_category)

        if not recipe_category:
            raise HTTPException(
                status_code=400, 
                detail=f"{recipe.recipe_category} as Recipe Category is not found"
            )

    if recipe.recipe_tag_id:
        recipe_tag = get_recipe_tag_by_name(db, recipe.recipe_tag)

        if not recipe_tag:
            raise HTTPException(
                status_code=400, 
                detail=f"{recipe.recipe_tag} as Recipe Tag is not found"
            )

    if recipe.recipe_origin_id:
        recipe_origin = get_recipe_origin_by_name(db, recipe.recipe_origin)

        if not recipe_origin:
            raise HTTPException(
                status_code=400, 
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
            status_code=500, 
            detail=f"Error creating {recipe.name} as Recipe: {str(e)}"
        )


    if recipe.name is not None:
        data = get_recipe_by_name(db, recipe.name)
    else:
        data = get_recipe_by_name(db, recipe_name)

    return data