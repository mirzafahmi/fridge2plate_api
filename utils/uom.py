from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func, asc
from uuid import UUID
from fastapi import HTTPException, status

from db.models.recipe import UOM, IngredientRecipeAssociation
from pydantic_schemas.uom import UOMCreate, UOMUpdate


def get_uoms(db: Session, skip: int=0, limit: int = 100):
    return db.query(UOM).order_by(asc(UOM.name)).offset(skip).limit(limit).all()

def get_uom_by_id(db: Session, uom_id: UUID):
    return db.query(UOM).filter(UOM.id == uom_id).first()

def get_uom_by_name(db: Session, uom_name: str):
    return db.query(UOM).filter(UOM.name == uom_name).first()

def get_uom_by_unit(db: Session, uom_unit: str):
    return db.query(UOM).filter(UOM.unit == uom_unit).first()

def check_unique_uom_name(db: Session, uom_name: str):
    return db.query(UOM).filter(func.lower(UOM.name) == func.lower(uom_name)).first()

def post_uom(db: Session, uom: UOMCreate):
    uom_data = {key: value for key, value in uom.dict().items() if value is not None}
    db_uom = UOM(**uom_data)

    db.add(db_uom)
    db.commit()
    db.refresh(db_uom)

    return db_uom

def put_uom(db: Session, uom_id: UUID, uom: UOMUpdate):
    db_uom = get_uom_by_id(db, uom_id)
    
    if db_uom:
        if uom.name and uom.name != db_uom.name:
            if check_unique_uom_name(db, uom.name):
                raise HTTPException(
                            status_code=400, 
                            detail=f"{uom.name} as UOM is already registered"
                        )
        for key, value in uom.dict().items():
            if value is not None:
                setattr(db_uom, key, value)
        db.commit()
        db.refresh(db_uom)

        return db_uom
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Id {uom_id} as UOM is not found"
        )

def delete_uom(db: Session, uom_id: UUID):
    db_uom = get_uom_by_id(db, uom_id)
    
    db.query(IngredientRecipeAssociation).filter(IngredientRecipeAssociation.uom_id == db_uom.id).update({
        IngredientRecipeAssociation.uom_id: None
    })

    db.commit()

    db.delete(db_uom)
    db.commit()