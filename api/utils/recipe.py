from sqlalchemy.orm import Session
from typing import Optional

from db.models.recipe import Recipe
from pydantic_schemas.recipe import RecipeCreate
from api.utils.recipe_category import get_recipe_category_by_name
from api.utils.recipe_tag import get_recipe_tag_by_name
from api.utils.recipe_origin import get_recipe_origin_by_name


def get_recipes(db: Session, skip: int=0, limit: int = 100):
    return db.query(Recipe).offset(skip).limit(limit).all()


def get_recipe_by_id(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


def get_recipe_by_name(db: Session, recipe_name: str):
    return db.query(Recipe).filter(Recipe.name == recipe_name).first()


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


def update_recipe(
    db: Session, 
    recipe_name: str, 
    recipe: Optional[RecipeCreate],
    new_name: Optional[str] = None
):
    db_recipe = get_recipe_by_name(db, recipe_name)
    
    if db_recipe:
        # Update the properties of the existing recipe category
        if recipe:
            for key, value in recipe.dict().items():
                if value is not None:
                    setattr(db_recipe, key, value)

        if new_name:
            db_recipe.name = new_name

        db.commit()
        db.refresh(db_recipe)

        return db_recipe
    else:
        raise HTTPException(status_code=404, detail=f"recipe Category with name {recipe_name} not found")


def delete_recipe(db: Session, recipe_name: str):
    db_recipe = get_recipe_by_name(db, recipe_name)
    
    if not db_recipe:
        raise HTTPException(status_code=404, detail=f"recipe Category with name {recipe_name} not found")

    db.delete(db_recipe)
    db.commit()