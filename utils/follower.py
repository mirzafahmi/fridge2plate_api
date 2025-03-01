from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import exists, case
from typing import Optional, List
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
    FollowerAlias = aliased(Follower)

    followers = (
        db.query(
            User,
            exists()
            .where(FollowerAlias.user_id == User.id)
            .where(FollowerAlias.follower_id == user_id)
            .correlate(User)
            .label("is_following")
        )
        .join(Follower, User.id == Follower.follower_id)
        .filter(Follower.user_id == user_id)
        .order_by(Follower.created_date.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    return followers

def get_following(db: Session, user_id: UUID, limit: int = 10, offset: int = 0):
    FollowerAlias = aliased(Follower)

    following = (
        db.query(
            User,
            exists()
            .where(FollowerAlias.follower_id == user_id)  
            .where(FollowerAlias.user_id == User.id) 
            .correlate(User)
            .label("is_following")
        )
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

def get_follow_stats(db: Session, user_id: UUID):
    counts = (
        db.query(
            func.count(case((Follower.user_id == user_id, 1))).label("followers_count"),
            func.count(case((Follower.follower_id == user_id, 1))).label("followings_count"),
        )
        .one()
    )

    return {"followers_count": counts.followers_count, "followings_count": counts.followings_count}

def get_follow_counts(db: Session, user_ids: List[UUID]):
    counts = (
        db.query(
            User.id.label("user_id"),
            func.coalesce(
                db.query(func.count()).filter(Follower.user_id == User.id, Follower.user_id.in_(user_ids)).scalar_subquery(),
                0
            ).label("followers_count"),
            func.coalesce(
                db.query(func.count()).filter(Follower.follower_id == User.id, Follower.follower_id.in_(user_ids)).scalar_subquery(),
                0
            ).label("followings_count"),
        )
        .filter(User.id.in_(user_ids))
        .all()
    )

    result = {
        row.user_id: {
            "followers_count": row.followers_count, 
            "followings_count": row.followings_count
        } 
        for row in counts
    }
    return result


def get_follow_status(db: Session, user_id: UUID):
    return db.query(Follower).filter_by()