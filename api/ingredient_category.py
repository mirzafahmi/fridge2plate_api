from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from utils.ingredient_category import *
from db.db_setup import get_db
from pydantic_schemas.ingredient_category import IngredientCategory, IngredientCategoryCreate, IngredientCategoryCreatedResponse


router = APIRouter(
    prefix='/ingredient_categories', 
    tags=["Ingredient Categories"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[IngredientCategory])
async def read_ingredient_categories(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    ingredient_categories = get_ingredient_categories(db, skip=skip, limit=limit)

    if not ingredient_categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient Categories is empty")

    return ingredient_categories


@router.get("/{ingredient_category_id}", status_code=status.HTTP_200_OK, response_model=IngredientCategory)
async def read_ingredient_category_by_id(*, db: Session = Depends(get_db), ingredient_category_id: int):
    ingredient_category_by_id = get_ingredient_category_by_id(db, ingredient_category_id=ingredient_category_id)

    if ingredient_category_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{ingredient_category_id} as Ingredient Category is not found"
        )

    return ingredient_category_by_id


@router.get("/by_name/{ingredient_category_name}", status_code=status.HTTP_200_OK, response_model=IngredientCategory)
async def read_ingredient_category_by_name(*, db: Session = Depends(get_db), ingredient_category_name: str):
    ingredient_category_by_name = get_ingredient_category_by_name(db, ingredient_category_name=ingredient_category_name)

    if ingredient_category_by_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{ingredient_category_name} as Ingredient Category is not found"
        )

    return ingredient_category_by_name


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_ingredient_category(*, db: Session = Depends(get_db), ingredient_category: IngredientCategoryCreate):
    ingredient_category_by_name = get_ingredient_category_by_name(db, ingredient_category_name=ingredient_category.name)
    
    if ingredient_category_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{ingredient_category.name} as Ingredient Category is already registered"
        )

    ingredient_category_create = post_ingredient_category(db=db, ingredient_category=ingredient_category)

    result_message = f"{ingredient_category.name} as Ingredient Category is successfully created"
    data = get_ingredient_category_by_name(db, ingredient_category_name=ingredient_category.name)

    return {"result": result_message, "data": data}

@router.put("/{ingredient_category_id}", status_code=status.HTTP_202_ACCEPTED)
async def change_ingredient_category_by_id(
    *, db: Session = Depends(get_db), 
    ingredient_category_id: str, 
    ingredient_category: IngredientCategoryCreate
):
    db_ingredient_category = get_ingredient_category_by_id(db, ingredient_category_id=ingredient_category_id)
    
    if not db_ingredient_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {ingredient_category_id} as Ingredient Category is not registered"
        )

    ingredient_category_update = update_ingredient_category(db=db, ingredient_category_id=ingredient_category_id, ingredient_category=ingredient_category)

    result_message = f"Id {ingredient_category_id} as Ingredient Category is successfully updated"

    return {"result": result_message, "data": ingredient_category_update}


@router.delete("/{ingredient_category_id}", status_code=status.HTTP_200_OK)
async def remove_ingredient_category_by_id(*, db: Session = Depends(get_db), ingredient_category_id: str):
    db_ingredient_category = get_ingredient_category_by_id(db, ingredient_category_id=ingredient_category_id)

    if db_ingredient_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient Category is not found")

    delete_ingredient_category(db=db, ingredient_category_id=ingredient_category_id)
    result_message = f"Id {ingredient_category_id} as Ingredient Category is successfully deleted"

    return {"result": result_message}

#TODO! convert all end point using name into using id
@router.put("/by_name/{ingredient_category_name}", status_code=status.HTTP_202_ACCEPTED, deprecated=True)
async def change_ingredient_category_by_name(
    *, db: Session = Depends(get_db), 
    ingredient_category_name: str, 
    ingredient_category: IngredientCategoryCreate
):
    ingredient_category_by_name = get_ingredient_category_by_name(db, ingredient_category_name=ingredient_category_name)
    
    if not ingredient_category_by_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{ingredient_category_name} as Ingredient Category is not registered"
        )

    ingredient_category_update = update_ingredient_category_by_name(db=db, ingredient_category_name=ingredient_category_name, ingredient_category=ingredient_category)

    result_message = f"{ingredient_category.name} as Ingredient Category is successfully updated from {ingredient_category_name}"
    data = get_ingredient_category_by_name(db, ingredient_category_name=ingredient_category.name)

    return {"result": result_message, "data": data}


@router.delete("/by_name/{ingredient_category_name}", status_code=status.HTTP_200_OK, deprecated=True)
async def remove_ingredient_category_by_name(*, db: Session = Depends(get_db), ingredient_category_name: str):
    ingredient_category_by_name = get_ingredient_category_by_name(db, ingredient_category_name=ingredient_category_name)

    if ingredient_category_by_name is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingredient Category is not found")

    delete_ingredient_category_by_name(db=db, ingredient_category_name=ingredient_category_name)
    result_message = f"{ingredient_category_name} as Ingredient Category is successfully deleted"

    return {"result": result_message}

#TODO! convert name to id for method of retrieve data
# @router.put("/ingredient_category_update_path/{ingredient_category_name}", status_code=202)
# async def change_ingredient_category(
#     *,
#     db: Session = Depends(get_db),
#     ingredient_category_name: str,
#     new_name: Optional[str] = Query(None, title="New Name"),
#     ingredient_category: Optional[IngredientCategoryCreate] = None
# ):
#     ingredient_category_by_name = get_ingredient_category_by_name(db, ingredient_category_name=ingredient_category_name)

#     if not ingredient_category_by_name:
#         raise HTTPException(
#             status_code=404, 
#             detail=f"{ingredient_category_name} as Ingredient Category is not registered"
#         )

#     # Assuming you have a function that updates the ingredient category based on the new name
#     ingredient_category_update = update_ingredient_category(
#         db=db,
#         ingredient_category_name=ingredient_category_name,
#         ingredient_category=ingredient_category,
#         new_name=new_name,
#     )

#     result_message = f"Ingredient Category is successfully updated from {ingredient_category_name} to {new_name}"
#     data = get_ingredient_category_by_name(db, ingredient_category_name=new_name)

#     return {"result": result_message, "data": data}




