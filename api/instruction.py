from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.instruction import get_instructions_by_recipe_id
from db.db_setup import get_db
from pydantic_schemas.instruction import InstructionResponse

router = APIRouter(
    prefix="/instruction",
    tags=["Instruction"])

@router.get("/by_recipe_id/{recipe_id}", status_code=status.HTTP_200_OK, response_model=InstructionResponse)
async def read_instruction_by_recipe_id(*, db: Session = Depends(get_db), recipe_id: UUID):
    instructions = get_instructions_by_recipe_id(db, recipe_id)

    if not instructions:
        raise HTTPException(status_code=404, detail=f"Instruction list for ID {recipe_id} of recipe is empty")

    return {
        "detail": f"Instruction list of ID {recipe_id} of recipe is retrieved successfully",
        "instructions": instructions
    }
