from sqlalchemy.orm import Session
from sqlalchemy import asc
from uuid import UUID

from db.models.recipe import Instruction


def get_instructions_by_recipe_id(db: Session, recipe_id: UUID):
    instructions = db.query(Instruction).filter(Instruction.recipe_id == recipe_id).order_by(asc(Instruction.step_number)).all()

    return instructions