from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status

from db.models.recipe import RecipeTagRecipeAssociation
from pydantic_schemas.recipe_tag_recipe_association import RecipeTagRecipeAssociationCreate, RecipeTagRecipeAssociationUpdate

def get_recipe_tag_recipe_association(db: Session, skip: int=0, limit: int = 100):
    return db.query(RecipeTagRecipeAssociation).offset(skip).limit(limit).all()

def get_recipe_tag_recipe_association_by_id(db: Session, recipe_tag_recipe_association_id: UUID):
    return db.query(RecipeTagRecipeAssociation).filter(RecipeTagRecipeAssociation.id == recipe_tag_recipe_association_id).first()

def get_recipe_tag_recipe_association_by_recipe_id(db: Session, recipe_id: UUID):
    return db.query(RecipeTagRecipeAssociation).filter(RecipeTagRecipeAssociation.recipe_id == recipe_id).all()

def check_recipe_tag_recipe_association_by_recipe_tag_duplication(db: Session, recipe_tag_recipe_association: RecipeTagRecipeAssociationCreate):
    return db.query(RecipeTagRecipeAssociation).filter_by(recipe_id=recipe_tag_recipe_association.recipe_id, recipe_tag_id=recipe_tag_recipe_association.recipe_tag_id).first()

def post_recipe_tag_recipe_association(db: Session, recipe_tag_recipe_association: RecipeTagRecipeAssociationCreate):
    recipe_tag_recipe_association_data = {key: value for key, value in recipe_tag_recipe_association.dict().items() if value is not None}
    db_association = RecipeTagRecipeAssociation(**recipe_tag_recipe_association_data)

    db.add(db_association)
    db.commit()
    db.refresh(db_association)

    return db_association

def put_recipe_tag_recipe_association(db: Session, recipe_tag_recipe_association_id: UUID, recipe_tag_recipe_association:RecipeTagRecipeAssociationUpdate):
    db_recipe_tag_recipe_asscociation = get_recipe_tag_recipe_association_by_id(db, recipe_tag_recipe_association_id)

    if recipe_tag_recipe_association:
        for key, value in recipe_tag_recipe_association.dict().items():
            if value is not None:
                setattr(db_recipe_tag_recipe_asscociation, key, value)

    db.commit()
    db.refresh(db_recipe_tag_recipe_asscociation)

    return db_recipe_tag_recipe_asscociation

def delete_recipe_tag_recipe_association(db: Session, recipe_tag_recipe_association_id: UUID):
    db_recipe_tag_recipe_association = get_recipe_tag_recipe_association_by_id(db, recipe_tag_recipe_association_id)
    
    db.delete(db_recipe_tag_recipe_association)
    db.commit()