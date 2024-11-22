from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.uom import *
from utils.user import check_valid_user
from db.db_setup import get_db
from pydantic_schemas.uom import UOM, UOMCreate, UOMUpdate, UOMResponse, UOMsResponse


router = APIRouter(
    prefix="/uoms",
    tags=["Unit of Measurements (UOM)"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=UOMsResponse)
async def read_uom_list(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    uoms = get_uoms(db, skip=skip, limit=limit)

    if not uoms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="UOM list is empty"
        )

    return {
        "detail": "UOM list is retrieved successfully",
        "uoms": uoms
    }

@router.get("/{uom_id}", status_code=status.HTTP_200_OK, response_model=UOMResponse)
async def read_uom_by_id(*, db: Session = Depends(get_db), uom_id: UUID):
    uom_by_id = get_uom_by_id(db, uom_id)

    if uom_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {uom_id} as UOM is not found"
        )

    return {
        "detail": f"Id {uom_id} as UOM is retrieved successfully",
        "uom": uom_by_id
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UOMResponse)
async def add_uom(*, db: Session = Depends(get_db), uom: UOMCreate):
    uom_by_name = get_uom_by_name(db, uom.name)
    
    if uom_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{uom.name} as UOM is already registered"
        )
    
    uom_by_unit = get_uom_by_unit(db, uom.unit)

    if uom_by_unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{uom.unit} as UOM unit is already registered"
        )

    check_valid_user(db, uom)

    uom_create = post_uom(db, uom)

    result_message = f"{uom.name} as UOM is successfully created"

    return {"detail": result_message, "uom": uom_create}

@router.put("/{uom_id}", status_code=status.HTTP_202_ACCEPTED, response_model=UOMResponse)
async def change_uom(*,db: Session = Depends(get_db), uom_id: UUID, uom: UOMUpdate):
    uom_by_id = get_uom_by_id(db, uom_id)

    if not uom_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {uom_id} as UOM is not found"
        )

    uom_by_unit = get_uom_by_unit(db, uom.unit)

    if uom_by_unit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{uom.unit} as UOM unit is already registered"
        )
        
    check_valid_user(db, uom)

    uom_update = put_uom(db, uom_id, uom)

    result_message = f"Id {uom_id} as UOM is successfully updated"

    return {"detail": result_message, "uom": uom_update}

@router.delete("/{uom_id}", status_code=status.HTTP_200_OK)
async def remove_uom(*, db: Session = Depends(get_db), uom_id: UUID):
    uom_by_id = get_uom_by_id(db, uom_id)

    if not uom_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Id {uom_id} as UOM is not found"
        )

    delete_uom(db, uom_id)
    result_message = f"Id {uom_id} as UOM is successfully deleted"

    return {"detail": result_message}






@router.get("/by_name/{uom_name}", status_code=status.HTTP_200_OK, response_model=UOM, deprecated=True)
async def read_uom_by_name(*, db: Session = Depends(get_db), uom_name: str):
    uom_by_name = get_uom_by_name(db, uom_name=uom_name)

    if uom_by_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{uom_name} name as UOM is not found"
        )

    return uom_by_name