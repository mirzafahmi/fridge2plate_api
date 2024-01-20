from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query 
from sqlalchemy.orm import Session

from api.utils.uom import *
from db.db_setup import get_db
from pydantic_schemas.uom import UOM, UOMCreate, UOMCreatedResponse


router = APIRouter(tags=["Unit of Measurements (UOM)"])

@router.get("/uom_list", response_model=List[UOM])
async def read_uom_list(db: Session = Depends(get_db), skip: int=0, limit: int = 100):
    uom = get_uoms(db, skip=skip, limit=limit)

    if not uom:
        raise HTTPException(
            status_code=404, 
            detail="UOM list is empty"
        )

    return uom


@router.get("/uom_id/{uom_id}", response_model=UOM)
async def read_uom_by_id(*, db: Session = Depends(get_db), uom_id: int):
    uom_by_id = get_uom_by_id(db, uom_id=uom_id)

    if uom_by_id is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{uom_id} id for UOM is not found"
        )

    return uom_by_id


@router.get("/uom_name/{uom_name}", response_model=UOM)
async def read_uom_by_name(*, db: Session = Depends(get_db), uom_name: str):
    uom_by_name = get_uom_by_name(db, uom_name=uom_name)

    if uom_by_name is None:
        raise HTTPException(
            status_code=404, 
            detail=f"{uom_name} name for UOM is not found"
        )

    return uom_by_name


@router.post("/uom_create", status_code=201)
async def add_uom(*, db: Session = Depends(get_db), uom: UOMCreate):
    uom_by_name = get_uom_by_name(db, uom_name=uom.name)
    
    if uom_by_name:
        raise HTTPException(
            status_code=400, 
            detail=f"{uom.name} as UOM is already registered"
        )

    uom_create = create_uom(db=db, uom=uom)

    result_message = f"{uom.name} as UOM is successfully created"
    data = get_uom_by_name(db, uom_name=uom.name)

    return {"result": result_message, "data": data}


@router.put("/uom_update/{uom_name}", status_code=202)
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
            status_code=404, 
            detail=f"{uom_name} as UOM is not registered"
        )

    # Assuming you have a function that updates the UOM based on the new name
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



@router.delete("/uom_delete/{uom_name}", status_code=200)
async def remove_uom(*, db: Session = Depends(get_db), uom_name: str):
    uom_by_name = get_uom_by_name(db, uom_name=uom_name)

    if uom_by_name is None:
        raise HTTPException(status_code=404, detail="UOM is not found")

    delete_uom(db=db, uom_name=uom_name)
    result_message = f"{uom_name} as UOM is successfully deleted"

    return {"result": result_message}