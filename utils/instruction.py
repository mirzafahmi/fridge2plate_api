from sqlalchemy.orm import Session
from sqlalchemy import asc, func
from uuid import UUID
from fastapi import HTTPException, status

from db.models.recipe import RecipeInstruction
from pydantic_schemas.instruction import InstructionCreate, InstructionUpdate

def get_instructions(db: Session, skip: int=0, limit: int = 100):
    return db.query(RecipeInstruction).offset(skip).limit(limit).all()

def get_instruction_by_id(db: Session, instruction_id: UUID):
    return db.query(RecipeInstruction).filter(RecipeInstruction.id == instruction_id).first()

def get_instructions_by_recipe_id(db: Session, recipe_id: UUID):
    return db.query(RecipeInstruction).filter(RecipeInstruction.recipe_id == recipe_id).order_by(asc(RecipeInstruction.step_number)).all()

def check_instruction_by_step_number_duplication(db: Session, instruction: InstructionCreate):
    return db.query(RecipeInstruction).filter_by(recipe_id=instruction.recipe_id, step_number=instruction.step_number).first()

def validate_step_number(db: Session, recipe_id: UUID, new_step_number: int):
    # Get the current highest step_number for the recipe
    max_step_number = (
        db.query(func.max(RecipeInstruction.step_number))
        .filter(RecipeInstruction.recipe_id == recipe_id)
        .scalar()
    )

    if max_step_number is None:
        if new_step_number != 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Step numbers must start at 1 for a new recipe.",
            )
    else:
        if new_step_number != max_step_number + 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Step number {new_step_number} is invalid. The next step should be {max_step_number + 1}.",
            )

def post_instruction(db: Session, instruction: InstructionCreate):
    instruction_data = {key: value for key, value in instruction.dict().items() if value is not None}
    db_instruction = RecipeInstruction(**instruction_data)

    db.add(db_instruction)
    db.commit()
    db.refresh(db_instruction)

    return db_instruction

def put_instruction(db: Session, instruction_id: UUID, instruction:InstructionUpdate):
    db_instruction = get_instruction_by_id(db, instruction_id)

    if instruction:
        for key, value in instruction.dict().items():
            if value is not None:
                setattr(db_instruction, key, value)

    db.commit()
    db.refresh(db_instruction)

    return db_instruction

def delete_instruction(db: Session, instruction_id: UUID):
    db_instruction = get_instruction_by_id(db, instruction_id)
    
    db.delete(db_instruction)
    db.commit()