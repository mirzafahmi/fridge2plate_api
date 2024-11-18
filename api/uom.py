from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from utils.uom import *
from db.db_setup import get_db
from pydantic_schemas.uom import UOM, UOMCreate, UOMCreatedResponse


router = APIRouter(
    prefix="/uoms",
    tags=["Unit of Measurements (UOM)"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UOM])
async def read_uom_list(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    uom = get_uoms(db, skip=skip, limit=limit)

    if not uom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="UOM list is empty"
        )

    return uom


@router.get("/{uom_id}", status_code=status.HTTP_200_OK, response_model=UOM)
async def read_uom_by_id(*, db: Session = Depends(get_db), uom_id: int):
    uom_by_id = get_uom_by_id(db, uom_id=uom_id)

    if uom_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{uom_id} id for UOM is not found"
        )

    return uom_by_id


@router.get("/by_name/{uom_name}", status_code=status.HTTP_200_OK, response_model=UOM)
async def read_uom_by_name(*, db: Session = Depends(get_db), uom_name: str):
    uom_by_name = get_uom_by_name(db, uom_name=uom_name)

    if uom_by_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{uom_name} name for UOM is not found"
        )

    return uom_by_name


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_uom(*, db: Session = Depends(get_db), uom: UOMCreate):
    uom_by_name = get_uom_by_name(db, uom_name=uom.name)
    
    if uom_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"{uom.name} as UOM is already registered"
        )

    uom_create = create_uom(db=db, uom=uom)

    result_message = f"{uom.name} as UOM is successfully created"
    data = get_uom_by_name(db, uom_name=uom.name)

    return {"result": result_message, "data": data}


@router.put("/{uom_name}", status_code=status.HTTP_202_ACCEPTED)
async def change_uom(
    *,
    db: Session = Depends(get_db),
    uom_name: str,
    new_name: Optional[str] = Query(None, title="New Name"),
    new_unit: Optional[str] = Query(None, title="New Unit"),
    new_weightage: Optional[float] = Query(None, title="New Weightage"),
    uom: Optional[UOMCreate] = None
):
    uom_by_name = get_uom_by_name(db, uom_name=uom_name)

    if not uom_by_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"{uom_name} as UOM is not registered"
        )

    uom_update = update_uom(
        db=db,
        uom_name=uom_name,
        uom=uom,
        new_name=new_name,
        new_unit=new_unit,
        new_weightage=new_weightage,
    )

    result_message = f"UOM is successfully updated from {uom_name} to {new_name}"
    data = get_uom_by_name(db, uom_name=new_name)

    return {"result": result_message, "data": data}



@router.delete("/{uom_name}", status_code=status.HTTP_200_OK)
async def remove_uom(*, db: Session = Depends(get_db), uom_name: str):
    uom_by_name = get_uom_by_name(db, uom_name=uom_name)

    if uom_by_name is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="UOM is not found"
        )

    delete_uom(db=db, uom_name=uom_name)
    result_message = f"{uom_name} as UOM is successfully deleted"

    return {"result": result_message}