from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func, asc
from uuid import UUID
from fastapi import HTTPException, status

from db.models.recipe import RecipeUserAssociation
from pydantic_schemas.recipe_user_association import RecipeAction

def get_or_create_recipe_user_association(db: Session, recipe_id: UUID, user_id: UUID):
    association = db.query(RecipeUserAssociation).filter_by(recipe_id = recipe_id, user_id = user_id).first()

    if not association:
        association = RecipeUserAssociation(recipe_id=recipe_id, user_id=user_id)
        db.add(association)
        db.commit()
        db.refresh(association)

    return association

def toggle_action(db: Session, association: RecipeUserAssociation, action: RecipeAction):
    if action == RecipeAction.liked:
        association.liked = not association.liked
        association.liked_date = func.now() if association.liked else None
    elif action == RecipeAction.bookmarked:
        association.bookmarked = not association.bookmarked
        association.bookmarked_date = func.now() if association.bookmarked else None
    elif action == RecipeAction.cooked:
        association.cooked = not association.cooked
        association.cooked_date = func.now() if association.cooked else None

    db.commit()
    db.refresh(association)

    return association

def get_cooked_recipes(db: Session, user_id: UUID):
    return db.query(RecipeUserAssociation).filter_by(user_id=user_id, cooked=True).all()

def get_bookmarked_recipes(db: Session, user_id: UUID):
    return db.query(RecipeUserAssociation).filter_by(user_id=user_id, bookmarked=True).all()

def get_liked_recipes(db: Session, user_id: UUID):
    return db.query(RecipeUserAssociation).filter_by(user_id=user_id, liked=True).all()

def get_user_recipe_actions(db: Session, user_id: UUID):
    user_associations = db.query(RecipeUserAssociation).filter_by(user_id=user_id).all()

    recipes_by_action = {
        "cooked": [],
        "bookmarked": [],
        "liked": []
    }

    # Filter the recipes based on their respective actions
    for association in user_associations:
        if association.cooked:
            recipes_by_action["cooked"].append(association)
        if association.bookmarked:
            recipes_by_action["bookmarked"].append(association)
        if association.liked:
            recipes_by_action["liked"].append(association)

    return recipes_by_action

def get_user_interactions(db: Session, user_id: UUID):
    interactions = db.query(
        func.count().filter(RecipeUserAssociation.user_id == user_id, RecipeUserAssociation.cooked == True).label("cooked_count"),
        func.count().filter(RecipeUserAssociation.user_id == user_id, RecipeUserAssociation.liked == True).label("liked_count"),
        func.count().filter(RecipeUserAssociation.user_id == user_id, RecipeUserAssociation.bookmarked == True).label("bookmarked_count")
    ).first()

    return {
        "cooked_count": interactions.cooked_count,
        "liked_count": interactions.liked_count,
        "bookmarked_count": interactions.bookmarked_count
    }

def get_users_interactions(db: Session, user_ids: list[UUID]):
    interactions = (
        db.query(
            RecipeUserAssociation.user_id,
            func.count().filter(RecipeUserAssociation.cooked == True).label("cooked_count"),
            func.count().filter(RecipeUserAssociation.liked == True).label("liked_count"),
            func.count().filter(RecipeUserAssociation.bookmarked == True).label("bookmarked_count"),
        )
        .filter(RecipeUserAssociation.user_id.in_(user_ids))
        .group_by(RecipeUserAssociation.user_id)
        .all()
    )

    return {
        interaction.user_id: {
            "cooked_count": interaction.cooked_count,
            "liked_count": interaction.liked_count,
            "bookmarked_count": interaction.bookmarked_count,
        }
        for interaction in interactions
    }
