from sqlalchemy.orm import Session
from uuid import UUID

from db.models.recipe import RecipeImage
from pydantic_schemas.recipe_image import RecipeImageCreate, RecipeImageUpdate


def get_recipe_images(db: Session, skip: int=0, limit: int = 100):
    return db.query(RecipeImage).offset(skip).limit(limit).all()

def get_recipe_image_by_id(db: Session, recipe_image_id: UUID):
    return db.query(RecipeImage).filter(RecipeImage.id == recipe_image_id).first()

def get_recipe_images_by_recipe_id(db: Session, recipe_id: UUID):
    return db.query(RecipeImage).filter(RecipeImage.recipe_id == recipe_id).all()

def post_recipe_image(db: Session, recipe_image: RecipeImageCreate):
    created_images = []

    for image in recipe_image.image:
        db_recipe_image_post = RecipeImage(
                image=image,
                recipe_id=recipe_image.recipe_id
            )

        db.add(db_recipe_image_post)
        created_images.append(db_recipe_image_post)

    db.commit()

    for img in created_images:
        db.refresh(img)

    return created_images

def put_recipe_image(db: Session, recipe_image_id: UUID, recipe_image: RecipeImageUpdate):
    db_recipe_image = get_recipe_image_by_id(db, recipe_image_id)
    
    if recipe_image:
        for key, value in recipe_image.dict().items():
            if value is not None:
                setattr(db_recipe_image, key, value)

    db.commit()
    db.refresh(db_recipe_image)

    return db_recipe_image

def delete_recipe_image(db: Session, recipe_image_id: UUID):
    db_recipe_image = get_recipe_image_by_id(db, recipe_image_id)
    
    db.delete(db_recipe_image)
    db.commit()