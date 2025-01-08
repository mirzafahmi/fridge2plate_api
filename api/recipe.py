from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.user import check_valid_user, get_current_user
from utils.recipe import *
from utils.ingredient import get_ingredient_by_id
from utils.ingredient_recipe_association import *
from utils.recipe_category import get_recipe_category_by_id
from utils.recipe_tag import get_recipe_tag_by_id
from utils.recipe_origin import get_recipe_origin_by_id
from utils.uom import get_uom_by_id
from utils.recipe_user_association import get_or_create_recipe_user_association, toggle_action

from db.db_setup import get_db
from pydantic_schemas.recipe import Recipe, RecipeCreate, RecipeUpdate, RecipeResponse, RecipesResponse, RecipeLiteResponse, RecipesLiteResponse
from pydantic_schemas.recipe_user_association import ActionSchema, RecipeUserAssociation, RecipeUserAssociationResponse, RecipeUserAssociationsResponse


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

    recipe_ids = [recipe.id for recipe in recipes]

    interaction_counts = get_recipe_interaction_counts(db, recipe_ids)
    
    for recipe in recipes:
        counts = interaction_counts.get(recipe.id, {})
        recipe.cooked_count = counts.get("cooked_count", 0)
        recipe.bookmarked_count = counts.get("bookmarked_count", 0)
        recipe.liked_count = counts.get("liked_count", 0)
        
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

    recipe_ids = [recipe.id for recipe in recipes]

    interaction_counts = get_recipe_interaction_counts(db, recipe_ids)
    
    for recipe in recipes:
        counts = interaction_counts.get(recipe.id, {})
        recipe.cooked_count = counts.get("cooked_count", 0)
        recipe.bookmarked_count = counts.get("bookmarked_count", 0)
        recipe.liked_count = counts.get("liked_count", 0)

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
            detail=f"ID {recipe_id} as Recipe is not found"
        )

    interaction_counts = get_recipe_interaction_counts(db, [recipe_id])
    
    counts = interaction_counts.get(recipe_id, {})
    recipe_by_id.cooked_count = counts.get("cooked_count", 0)
    recipe_by_id.bookmarked_count = counts.get("bookmarked_count", 0)
    recipe_by_id.liked_count = counts.get("liked_count", 0)

    return {
        "detail": f"ID {recipe_id} as Recipe is retrieved successfully",
        "recipe": recipe_by_id
    }

@router.get("/{recipe_id}/lite", status_code=status.HTTP_200_OK, response_model=RecipeLiteResponse)
async def read_recipe_by_id(*, db: Session = Depends(get_db), recipe_id: UUID):
    recipe_by_id = get_recipe_by_id(db, recipe_id)

    if recipe_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_id} as Recipe is not found"
        )

    #TODO add this to post and put
    interaction_counts = get_recipe_interaction_counts(db, [recipe_id])

    counts = interaction_counts.get(recipe_id, {})
    recipe_by_id.cooked_count = counts.get("cooked_count", 0)
    recipe_by_id.bookmarked_count = counts.get("bookmarked_count", 0)
    recipe_by_id.liked_count = counts.get("liked_count", 0)

    return {
        "detail": f"ID {recipe_id} as Recipe Lite is retrieved successfully",
        "recipe": recipe_by_id
    }

#remove unique name
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RecipeLiteResponse)
async def add_recipe(*, db: Session = Depends(get_db), recipe: RecipeCreate):
    recipe_category_by_id = get_recipe_category_by_id(db, recipe.recipe_category_id)
    
    if not recipe_category_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe.recipe_category_id} as Recipe Category is not found"
        )
    
    recipe_origin_by_id = get_recipe_origin_by_id(db, recipe.recipe_origin_id)

    if not recipe_origin_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe.recipe_origin_id} as Recipe Origin is not found"
        )

    for recipe_tag in recipe.recipe_tags:
        recipe_tag_by_id = get_recipe_tag_by_id(db, recipe_tag)

        if not recipe_tag_by_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"ID {recipe_tag} as Recipe Tag is not found"
            )

    for ingredient in recipe.ingredients:
        ingredients_by_id = get_ingredient_by_id(db, ingredient.ingredient_id)

        if not ingredients_by_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"ID {ingredient.ingredient_id} as Ingredient is not found"
            )
        
        uom_by_id = get_uom_by_id(db, ingredient.uom_id)

        if not uom_by_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"ID {ingredient.uom_id} as UOM is not found"
            )
    #TODO uom checking


    check_valid_user(db, recipe)

    recipe_create = post_recipe(db, recipe)

    result_message = f"{recipe.name} as Recipe is created successfully"

    return {"detail": result_message,"recipe": recipe_create}

@router.post("/{recipe_id}/toggle", status_code=status.HTTP_200_OK, response_model=RecipeUserAssociationResponse)
async def toggle_recipe_action(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_id: UUID, action: ActionSchema):
    user_id = UUID(current_user['sub'])
    action_value = action.action
    
    recipe_by_id = get_recipe_by_id(db, recipe_id)

    if not recipe_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_id} as Recipe is not found"
        )

    association = get_or_create_recipe_user_association(db, recipe_id, user_id)

    updated_association = toggle_action(db, association, action_value)

    interaction_counts = get_recipe_interaction_counts(db, [recipe_id])

    counts = interaction_counts.get(recipe_id, {})
    updated_association.recipe.cooked_count = counts.get("cooked_count", 0)
    updated_association.recipe.bookmarked_count = counts.get("bookmarked_count", 0)
    updated_association.recipe.liked_count = counts.get("liked_count", 0)
    
    result_message = f"ID{recipe_id} as Recipe is {action_value} successfully"

    return {"detail": result_message, "recipe_user_association": updated_association}

#TODO endpoint to retrieved liked, bookmarked and cooked

@router.put("/{recipe_id}", status_code=status.HTTP_202_ACCEPTED, response_model=RecipeLiteResponse)
async def change_recipe(*, db: Session = Depends(get_db), recipe_id: UUID, recipe: RecipeUpdate):
    recipe_by_id = get_recipe_by_id(db, recipe_id)

    if not recipe_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_id} as Recipe is not found"
        )

    if hasattr(recipe, 'recipe_category_id') and recipe.recipe_category_id is not None:
        recipe_category_by_id = get_recipe_category_by_id(db, recipe.recipe_category_id)

        if not recipe_category_by_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"ID {recipe.recipe_category_id} as Recipe Category is not found"
            )
    
    if hasattr(recipe, 'recipe_origin_id') and recipe.recipe_origin_id is not None:
        recipe_origin_by_id = get_recipe_origin_by_id(db, recipe.recipe_origin_id)

        if not recipe_origin_by_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"ID {recipe.recipe_origin_id} as Recipe Origin is not found"
            )

    if hasattr(recipe, 'recipe_tags') and recipe.recipe_tags is not None:
        for recipe_tag in recipe.recipe_tags:
            recipe_tag_by_id = get_recipe_tag_by_id(db, recipe_tag)

            if not recipe_tag_by_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"ID {recipe_tag} as Recipe Tag is not found"
                )

    if hasattr(recipe, 'ingredients') and recipe.ingredients is not None:
        for ingredient in recipe.ingredients:    
            ingredients_by_id = get_ingredient_by_id(db, ingredient.ingredient_id)

            if not ingredients_by_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"ID {ingredient.ingredient_id} as Ingredient is not found"
                )
            
            uom_by_id = get_uom_by_id(db, ingredient.uom_id)

            if not uom_by_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail=f"ID {ingredient.uom_id} as UOM is not found"
                )

    check_valid_user(db, recipe)

    try:
        recipe_update = put_recipe(db, recipe_id, recipe)
        result_message = f"ID {recipe_id} as Recipe is updated successfully"

        return {"detail": result_message, "recipe": recipe_update}

    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{recipe_id}", status_code=status.HTTP_200_OK)
async def remove_recipe(*, db: Session = Depends(get_db), recipe_id: UUID):
    recipe_by_id = get_recipe_by_id(db, recipe_id)

    if not recipe_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {recipe_id} as Recipe is not found"
        )

    delete_recipe(db, recipe_id)
    result_message = f"ID {recipe_id} as Recipe is deleted successfully"

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