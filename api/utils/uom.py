from sqlalchemy.orm import Session
from typing import Optional

from db.models.recipe import UOM
from pydantic_schemas.uom import UOMCreate


def get_uoms(db: Session, skip: int=0, limit: int = 100):
    return db.query(UOM).offset(skip).limit(limit).all()


def get_uom_by_id(db: Session, uom_id: int):
    return db.query(UOM).filter(UOM.id == uom_id).first()


def get_uom_by_name(db: Session, uom_name: str):
    return db.query(UOM).filter(UOM.name == uom_name).first()


def create_uom(db: Session, uom: UOMCreate):
    db_uom = UOM(name=uom.name, unit=uom.unit, weightage=uom.weightage)
    db.add(db_uom)
    db.commit()
    db.refresh(db_uom)

    return db_uom


def update_uom(
    db: Session, 
    uom_name: str, 
    uom: Optional[UOMCreate],
    new_name: Optional[str] = None,
    new_unit: Optional[str] = None,
    new_weightage: Optional[float] = None
):
    db_uom = get_uom_by_name(db, uom_name)
    
    if db_uom:
        
        if uom:
            for key, value in uom.dict().items():
                setattr(db_uom, key, value)

        if new_name:
            db_uom.name = new_name
        
        if new_unit:
            db_uom.unit = new_unit
        
        if new_weightage:
            db_uom.weightage = new_weightage

        db.commit()
        db.refresh(db_uom)

        return db_uom
    else:
        raise HTTPException(status_code=404, detail=f"UOM with name {uom_name} not found")


def delete_uom(db: Session, uom_name: str):
    db_uom = get_uom_by_name(db, uom_name)
    
    if not db_uom:
        raise HTTPException(status_code=404, detail=f"UOM with name {uom_name} not found")

    db.delete(db_uom)
    db.commit()