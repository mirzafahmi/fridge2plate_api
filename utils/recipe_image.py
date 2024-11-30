from sqlalchemy.orm import Session
from uuid import UUID

from db.models.recipe import RecipeImage


def get_recipe_image(db: Session, skip: int=0, limit: int = 100):
    return db.query(RecipeImage).offset(skip).limit(limit).all()

def get_recipe_image_by_id(db: Session, recipe_image_id: UUID):
    return db.query(RecipeImage).filter(RecipeImage.id == recipe_image_id).first()

def get_recipe_images_by_recipe_id(db: Session, recipe_id: UUID):
    return db.query(RecipeImage).filter(RecipeImage.recipe_id == recipe_id).all()

def post_recipe_image(db: Session, recipe_image: str):
    recipe_image_data = {key: value for key, value in recipe_image.dict().items() if value is not None}
    db_association = RecipeTagRecipeAssociation(**recipe_image_data)

    db.add(db_association)
    db.commit()
    db.refresh(db_association)

    return db_association

def put_recipe_image(db: Session, recipe_image_id: UUID, recipe_image:str):
    db_recipe_tag_recipe_asscociation = get_recipe_image_by_id(db, recipe_image_id)

    if recipe_image:
        for key, value in recipe_image.dict().items():
            if value is not None:
                setattr(db_recipe_tag_recipe_asscociation, key, value)

    db.commit()
    db.refresh(db_recipe_tag_recipe_asscociation)

    return db_recipe_tag_recipe_asscociation

def delete_recipe_image(db: Session, recipe_image_id: UUID):
    db_recipe_image = get_recipe_image_by_id(db, recipe_image_id)
    
    db.delete(db_recipe_image)
    db.commit()