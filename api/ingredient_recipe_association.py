from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query , status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.ingredient_recipe_association import *
from utils.ingredient import get_ingredient_by_id
from utils.uom import get_uom_by_id
from utils.recipe import get_recipe_by_id
from db.db_setup import get_db
from pydantic_schemas.ingredient_recipe_association import IngredientRecipeAssociation, IngredientRecipeAssociationCreate, IngredientRecipeAssociationUpdate, IngredientRecipeAssociationResponseLite, IngredientRecipeAssociationsResponseLite


router = APIRouter(
    prefix="/ingredient_recipe_association",
    tags=["Ingredient Recipe Association"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=IngredientRecipeAssociationsResponseLite)
async def read_ingredient_recipe_associations(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    db_ingredient_recipe_associations = get_ingredient_recipe_associations(db, skip=skip, limit=limit)

    if not db_ingredient_recipe_associations:
        raise HTTPException(status_code=404, detail="Ingredient recipe association list is empty")

    return {
        "detail": f"Ingredient Recipe Association list is retrieved successfully",
        "ingredient_recipe_associations": db_ingredient_recipe_associations
    }

@router.get("/{ingredient_recipe_association_id}", status_code=status.HTTP_200_OK, response_model=IngredientRecipeAssociationResponseLite)
async def read_ingredient_recipe_associations_by_id(*, db: Session = Depends(get_db), ingredient_recipe_association_id: UUID):
    db_ingredient_recipe_association = get_ingredient_recipe_associations_by_id(db, ingredient_recipe_association_id)

    if not db_ingredient_recipe_association:
        raise HTTPException(status_code=404, detail=f"ID {ingredient_recipe_association_id} as Ingredient Recipe Association is not found")

    return {
        "detail": f"ID {ingredient_recipe_association_id} as Ingredient Recipe Association is retrieved successfully",
        "ingredient_recipe_association": db_ingredient_recipe_association
    }

@router.get("/by_recipe_id/{recipe_id}", status_code=status.HTTP_200_OK, response_model=IngredientRecipeAssociationsResponseLite)
async def read_ingredient_recipe_associations_by_recipe_id(*, db: Session = Depends(get_db), recipe_id: UUID):
    ingredient_recipe_associations = get_ingredient_recipe_associations_by_recipe_id(db, recipe_id)

    if not ingredient_recipe_associations:
        raise HTTPException(status_code=404, detail=f"Ingredient Recipe Association list for ID {recipe_id} of recipe is empty")

    return {
        "detail": f"Ingredient and recipe association list of ID {recipe_id} recipe is retrieved successfully",
        "ingredient_recipe_associations": ingredient_recipe_associations
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=IngredientRecipeAssociationResponseLite)
async def add_ingredient_recipe_associations(*, db: Session = Depends(get_db), ingredient_recipe_association: IngredientRecipeAssociationCreate):
    db_recipe = get_recipe_by_id(db, ingredient_recipe_association.recipe_id)

    if not db_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {ingredient_recipe_association.recipe_id} as Recipe is not found"
        )

    db_ingredient_recipe_association = check_ingredient_recipe_associations_by_ingredient_duplication(db, ingredient_recipe_association)

    if db_ingredient_recipe_association:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"ID {ingredient_recipe_association.ingredient_id} of Ingredient as Ingredient Recipe Association is already registered"
        )

    ingredient_by_id = get_ingredient_by_id(db, ingredient_recipe_association.ingredient_id)

    if not ingredient_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {ingredient_recipe_association.ingredient_id} as Ingredient is not found"
        )
    
    uom_by_id = get_uom_by_id(db, ingredient_recipe_association.uom_id)

    if not uom_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {ingredient_recipe_association.uom_id} as UOM is not found"
        )

    ingredient_recipe_association_create = post_association(db, ingredient_recipe_association)
    result_message = f"ID {ingredient_recipe_association.ingredient_id} of Ingredient as Ingredient Recipe Association is created successfully for ID {ingredient_recipe_association.recipe_id} of Recipe"

    return {"detail": result_message, "ingredient_recipe_association": ingredient_recipe_association_create}

@router.put("/{ingredient_recipe_association_id}", status_code=status.HTTP_202_ACCEPTED, response_model=IngredientRecipeAssociationResponseLite)
async def change_ingredient_recipe_associations(*, db: Session = Depends(get_db), ingredient_recipe_association_id: UUID, ingredient_recipe_association: IngredientRecipeAssociationUpdate):
    db_ingredient_recipe_association = get_ingredient_recipe_associations_by_id(db, ingredient_recipe_association_id)

    if not db_ingredient_recipe_association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {ingredient_recipe_association_id} as Ingredient Recipe Association is not found"
        )

    if not any(value is not None for value in ingredient_recipe_association.dict().values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must include at least one field to update"
        )

    if hasattr(ingredient_recipe_association, 'ingredient_id') and ingredient_recipe_association.ingredient_id is not None:
        ingredient_by_id = get_ingredient_by_id(db, ingredient_recipe_association.ingredient_id)

        if not ingredient_by_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"ID {ingredient_recipe_association.ingredient_id} as Ingredient is not found"
            )

    if hasattr(ingredient_recipe_association, 'uom_id') and ingredient_recipe_association.uom_id is not None:
        uom_by_id = get_uom_by_id(db, ingredient_recipe_association.uom_id)

        if not uom_by_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"ID {ingredient_recipe_association.uom_id} as UOM is not found"
            )

    ingredient_recipe_association_update = put_association(db, ingredient_recipe_association_id, ingredient_recipe_association)
    result_message = f"ID {ingredient_recipe_association.ingredient_id} of Ingredient as Ingredient Recipe Association is updated successfully for ID {db_ingredient_recipe_association.recipe_id} of Recipe"

    return {"detail": result_message, "ingredient_recipe_association": ingredient_recipe_association_update}
    
@router.delete("/{ingredient_recipe_association_id}", status_code=status.HTTP_200_OK)
async def remove_ingredient_recipe_associations(*, db: Session = Depends(get_db), ingredient_recipe_association_id: UUID):
    db_ingredient_recipe_association = get_ingredient_recipe_associations_by_id(db, ingredient_recipe_association_id)

    if not db_ingredient_recipe_association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {ingredient_recipe_association_id} as Ingredient Recipe Association is not found"
        )

    delete_association(db, ingredient_recipe_association_id)
    result_message = f"ID {ingredient_recipe_association_id} as Ingredient Recipe Association for ID {db_ingredient_recipe_association.recipe_id} of recipe is deleted successfully"

    return {"detail": result_message}











@router.get("/by_recipe_name", response_model=List[IngredientRecipeAssociation], deprecated=True)
async def read_ingredient_recipe_associations_by_recipe_name(*, db: Session = Depends(get_db), recipe_name: str):
    ingredient_recipe_associations = get_ingredient_recipe_associations_by_recipe_name(db, recipe_name)

    if not ingredient_recipe_associations:
        raise HTTPException(status_code=404, detail="Ingredient Recipe Association List is empty")

    return ingredient_recipe_associations
