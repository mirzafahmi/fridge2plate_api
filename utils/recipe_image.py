from sqlalchemy.orm import Session
from uuid import UUID

from db.models.recipe import RecipeImage


def get_recipe_images_by_recipe_id(db: Session, recipe_id: UUID):
    recipe_images = db.query(RecipeImage).filter(RecipeImage.recipe_id == recipe_id).all()

    return recipe_images
