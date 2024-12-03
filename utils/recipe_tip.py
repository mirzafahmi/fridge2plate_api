from sqlalchemy.orm import Session
from sqlalchemy import asc, func
from uuid import UUID
from fastapi import HTTPException, status

from db.models.recipe import RecipeTip
from pydantic_schemas.recipe_tip import RecipeTipCreate, RecipeTipUpdate


def get_recipe_tips(db: Session, skip: int=0, limit: int = 100):
    return db.query(RecipeTip).offset(skip).limit(limit).all()

def get_recipe_tip_by_id(db: Session, recipe_tip_id: UUID):
    return db.query(RecipeTip).filter(RecipeTip.id == recipe_tip_id).first()

def get_recipe_tips_by_recipe_id(db: Session, recipe_id: UUID):
    return db.query(RecipeTip).filter(RecipeTip.recipe_id == recipe_id).all()

def check_recipe_tip_duplication(db: Session, recipe_id: UUID, recipe_tip_description: str):
    return db.query(RecipeTip).filter(
        RecipeTip.description == recipe_tip_description,
        RecipeTip.recipe_id == recipe_id
    ).first()

def post_recipe_tip(db: Session, recipe_tip: RecipeTipCreate):
    created_recipe_tips = []

    for tip in recipe_tip.description:
        db_recipe_tip_post = RecipeTip(
                description=tip,
                recipe_id=recipe_tip.recipe_id
            )

        db.add(db_recipe_tip_post)
        created_recipe_tips.append(db_recipe_tip_post)

    db.commit()

    for tip in created_recipe_tips:
        db.refresh(tip)

    return created_recipe_tips

def put_recipe_tip(db: Session, recipe_tip_id: UUID, recipe_tip:RecipeTipUpdate):
    db_recipe_tip = get_recipe_tip_by_id(db, recipe_tip_id)

    if recipe_tip:
        for key, value in recipe_tip.dict().items():
            if value is not None:
                setattr(db_recipe_tip, key, value)

    db.commit()
    db.refresh(db_recipe_tip)

    return db_recipe_tip

def delete_recipe_tip(db: Session, recipe_tip_id: UUID):
    db_recipe_tip = get_recipe_tip_by_id(db, recipe_tip_id)
    
    db.delete(db_recipe_tip)
    db.commit()