from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func, asc
from uuid import UUID
from fastapi import HTTPException, status

from db.models.user import Follower, User

def toggle_follow(db: Session, user_id: UUID, following_id: UUID):
    follow_entry = db.query(Follower).filter_by(user_id=following_id, follower_id=user_id).first()

    if follow_entry:
        db.delete(follow_entry)
        db.commit()
        return "unfollowed"
    else:
        new_follow = Follower(user_id=following_id, follower_id=user_id)
        db.add(new_follow)
        db.commit()
        db.refresh(new_follow)
        return "followed"

def get_followers(db: Session, user_id: UUID, limit: int = 10, offset: int = 0):
    followers = (
        db.query(User)
        .join(Follower, User.id == Follower.follower_id)
        .filter(Follower.user_id == user_id)
        .order_by(Follower.created_date.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return followers

def get_following(db: Session, user_id: UUID, limit: int = 10, offset: int = 0):
    following = (
        db.query(User)
        .join(Follower, User.id == Follower.user_id)
        .filter(Follower.follower_id == user_id)
        .order_by(Follower.created_date.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return following

def get_followers_count(db: Session, user_id: UUID):
    return db.query(Follower).filter(Follower.user_id == user_id).count()

def get_following_count(db: Session, user_id: UUID):
    return db.query(Follower).filter(Follower.follower_id == user_id).count()
