from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func, asc
from uuid import UUID
from fastapi import HTTPException, status

from db.models.recipe import Recipe
from pydantic_schemas.instruction import InstructionCreate, InstructionUpdate, Instruction, InstructionsByRecipe


def get_instructions_by_recipe(db: Session, recipe_id: UUID):
    instructions = db.query(Instruction).filter(Instruction.recipe_id == recipe_id).order_by(asc(Instruction.step_number)).all()

    return InstructionsByRecipe(
        recipe_id=recipe_id,
        instructions=[Instruction.from_orm(instruction) for instruction in instructions]
    )