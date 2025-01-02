from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func, asc
from uuid import UUID
from fastapi import HTTPException, status

from db.models.user import Badge
from pydantic_schemas.badge import BadgeCreate, BadgeUpdate


def get_badges(db: Session, skip: int=0, limit: int = 100):
    return db.query(Badge).order_by(asc(Badge.name)).offset(skip).limit(limit).all()

def get_badge_by_id(db: Session, badge_id: UUID):
    return db.query(Badge).filter(Badge.id == badge_id).first()

def get_badge_by_name(db: Session, badge_name: str):
    return db.query(Badge).filter(Badge.name == badge_name).first()

def check_unique_badge_name(db: Session, badge_name: str):
    return db.query(Badge).filter(func.lower(Badge.name) == func.lower(badge_name)).first()

def post_badge(db: Session, badge: BadgeCreate):
    badge_data = {key: value for key, value in badge.dict().items() if value is not None}
    db_badge = Badge(**badge_data)

    db.add(db_badge)
    db.commit()
    db.refresh(db_badge)

    return db_badge

def update_badge(db: Session, badge_id: UUID, badge: BadgeUpdate):
    db_badge = get_badge_by_id(db, badge_id)

    if db_badge:
        if badge:
            if badge.name and badge.name != db_badge.name:
                if check_unique_badge_name(db, badge.name):
                    raise HTTPException(
                        status_code=400, 
                        detail=f"'{badge.name}' as Badge is already registered"
                    )
            for key, value in badge.dict().items():
                if value is not None:
                    setattr(db_badge, key, value)

        db.commit()
        db.refresh(db_badge)

        return db_badge
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Badge with id {badge_id} not found"
        )

def delete_badge(db: Session, badge_id: UUID):
    db_badge = get_badge_by_id(db, badge_id)

    ##TODO check cascade delete of asscoc table
    
    db.commit()
    
    db.delete(db_badge)
    db.commit()