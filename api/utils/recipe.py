from sqlalchemy.orm import Session
from typing import Optional

from db.models.recipe import Recipe
from pydantic_schemas.recipe import RecipeCreate, RecipeUpdate
from api.utils.recipe_category import get_recipe_category_by_name
from api.utils.recipe_tag import get_recipe_tag_by_name
from api.utils.recipe_origin import get_recipe_origin_by_name


def get_recipes(db: Session, skip: int=0, limit: int = 100):
    return db.query(Recipe).offset(skip).limit(limit).all()


def get_recipe_by_id(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


def get_recipe_by_name(db: Session, recipe_name: str):
    return db.query(Recipe).filter(Recipe.name == recipe_name).first()


# def get_recipe_by_recipe_category(db: Session, recipe_category: str):
#     recipe_category = get_recipe_category_by_name(db, recipe_category)

#     return db.query(Recipe).filter(Recipe.recipe_category_id == recipe_category).all()


# def get_recipe_by_recipe_tag(db: Session, recipe_tag: str):
#     recipe_tag = get_recipe_tag_by_name(db, recipe_tag)

#     return db.query(Recipe).filter(Recipe.recipe_tag_id == recipe_tag).all()


# def get_recipe_by_recipe_origin(db: Session, recipe_origin: str):
#     recipe_origin = get_recipe_origin_by_name(db, recipe_origin)

#     return db.query(Recipe).filter(Recipe.recipe_origin_id == recipe_origin).all()


def create_recipe(db: Session, recipe: RecipeCreate):
    recipe_category = get_recipe_category_by_name(db, recipe.recipe_category)
    recipe_tag = get_recipe_tag_by_name(db, recipe.recipe_tag)
    recipe_origin = get_recipe_origin_by_name(db, recipe.recipe_origin)

    db_recipe = Recipe(
                    name=recipe.name,
                    serving=recipe.serving,
                    cooking_time=recipe.cooking_time,
                    author= recipe.author,
                    instructions=recipe.instructions,
                    recipe_category_id=recipe_category.id,
                    recipe_tag_id=recipe_tag.id,
                    recipe_origin_id=recipe_origin.id
                    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe


def update_recipe(db: Session, recipe_name: str, recipe: RecipeUpdate):

    db_recipe = get_recipe_by_name(db, recipe_name)
    print(db_recipe)
    print(recipe)
    if db_recipe:
        for key, value in recipe.dict().items():
            if key == 'recipe_category' and value is not None:
                recipe_category = get_recipe_category_by_name(db, value)
                if recipe_category:
                    setattr(db_recipe, 'recipe_category', recipe_category)

            elif key =='recipe_tag' and value is not None:
                recipe_tag = get_recipe_tag_by_name(db, value)
                if recipe_tag:
                    setattr(db_recipe, 'recipe_tag', recipe_tag)
            
            elif key =='recipe_origin' and value is not None:
                recipe_origin = get_recipe_origin_by_name(db, value)
                if recipe_origin:
                    setattr(db_recipe, 'recipe_origin', recipe_origin)



        db.commit()
        db.refresh(db_recipe)
        
        return db_recipe

    else:
        raise HTTPException(status_code=404, detail=f"Recipe with name {recipe_name} not found")


def delete_recipe(db: Session, recipe_name: str):
    db_recipe = get_recipe_by_name(db, recipe_name)
    
    if not db_recipe:
        raise HTTPException(status_code=404, detail=f"recipe Category with name {recipe_name} not found")

    db.delete(db_recipe)
    db.commit()