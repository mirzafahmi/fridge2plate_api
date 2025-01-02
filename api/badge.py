from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.badge import *
from utils.user import check_valid_user, get_current_user
from db.db_setup import get_db
from pydantic_schemas.badge import Badge, BadgeCreate, BadgeUpdate, BadgeResponse, BadgesResponse


router = APIRouter(
    prefix='/badges', 
    tags=["Badges"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=BadgesResponse)
async def read_badges(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), skip: int=0, limit: int = 100):
    badges = get_badges(db, skip=skip, limit=limit)
    
    if not badges:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Badge list is empty"
        )

    return {
        "detail": "Badge list is retrieved successfully",
        "badges": badges
    }

@router.get("/{badge_id}", status_code=status.HTTP_200_OK, response_model=BadgeResponse)
async def read_badge_by_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), badge_id: UUID):
    badge_by_id = get_badge_by_id(db, badge_id)

    if badge_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {badge_id} as Badge is not found"
        )
    
    return {
        "detail": f"Id {badge_id} as Badge is retrieved successfully",
        "badge": badge_by_id
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BadgeResponse)
async def add_badge(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), badge: BadgeCreate):
    badge_by_name = get_badge_by_name(db, badge.name)
    
    if badge_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{badge.name} as Badge is already registered"
        )

    print(badge_by_name)
    check_valid_user(db, badge)

    badge_create = post_badge(db, badge)

    result_message = f"{badge.name} as Badge is created successfully"

    return {"detail": result_message, "badge": badge_create}

@router.put("/{badge_id}", status_code=status.HTTP_202_ACCEPTED, response_model=BadgeResponse)
async def change_badge_by_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), badge_id: UUID, badge: BadgeUpdate):
    db_badge = get_badge_by_id(db, badge_id=badge_id)
    
    if not db_badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {badge_id} as Badge is not found"
        )

    check_valid_user(db, badge)

    badge_update = update_badge(db, badge_id, badge)
    result_message = f"Id {badge_id} as Badge is updated successfully"

    return {"detail": result_message, "badge": badge_update}

@router.delete("/{badge_id}", status_code=status.HTTP_200_OK)
async def remove_badge_by_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), badge_id: UUID):
    db_badge = get_badge_by_id(db, badge_id)

    if not db_badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {badge_id} as Badge is not found"
        )

    delete_badge(db, badge_id)
    result_message = f"Id {badge_id} as Badge is deleted successfully"

    return {"detail": result_message}