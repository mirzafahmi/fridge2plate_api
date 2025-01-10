from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from utils.user import check_valid_user, get_current_user
from utils.instruction import get_instructions, get_instruction_by_id, get_instructions_by_recipe_id, check_instruction_by_step_number_duplication, validate_step_number, post_instruction, put_instruction, delete_instruction
from utils.recipe import get_recipe_by_id
from db.db_setup import get_db
from pydantic_schemas.instruction import InstructionResponse, InstructionsResponse, InstructionCreateV2, InstructionUpdate

router = APIRouter(
    prefix="/recipe_instructions",
    tags=["Recipe Instructions"]
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=InstructionsResponse)
async def read_instruction_by_recipe_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), skip: int=0, limit: int = 100):
    db_instructions = get_instructions(db, skip=skip, limit=limit)

    if not db_instructions:
        raise HTTPException(status_code=404, detail="Instruction list is empty")

    return {
        "detail": f"Instruction list is retrieved successfully",
        "instructions": db_instructions
    }

@router.get("/{instruction_id}", status_code=status.HTTP_200_OK, response_model=InstructionResponse)
async def read_instruction_by_recipe_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), instruction_id: UUID):
    db_instruction = get_instruction_by_id(db, instruction_id)

    if not db_instruction:
        raise HTTPException(
            status_code=404, 
            detail=f"ID {instruction_id} as Instruction is not found"
        )

    return {
        "detail": f"ID {instruction_id} as Instruction is retrieved successfully",
        "instruction": db_instruction
    }

@router.get("/by_recipe_id/{recipe_id}", status_code=status.HTTP_200_OK, response_model=InstructionsResponse)
async def read_instruction_by_recipe_id(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), recipe_id: UUID):
    instructions = get_instructions_by_recipe_id(db, recipe_id)

    if not instructions:
        raise HTTPException(
            status_code=404, 
            detail=f"Instruction list for ID {recipe_id} of recipe is empty"
        )

    return {
        "detail": f"Instruction list of ID {recipe_id} of recipe is retrieved successfully",
        "instructions": instructions
    }

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=InstructionResponse)
async def add_instruction(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), instruction: InstructionCreateV2):
    db_recipe = get_recipe_by_id(db, instruction.recipe_id)

    if not db_recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {instruction.recipe_id} as Recipe is not found"
        )
    
    db_instruction = check_instruction_by_step_number_duplication(db, instruction)

    if db_instruction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Step number {instruction.step_number} of Instruction for ID {instruction.recipe_id} of Recipe is already registered"
        )

    validate_step_number(db, instruction.recipe_id, instruction.step_number)

    instruction_create = post_instruction(db, instruction)
    result_message = f"{instruction.description} instruction as step number {instruction.step_number} of Instruction is created successfully for ID {instruction.recipe_id} of Recipe"

    return {"detail": result_message, "instruction": instruction_create}

@router.put("/{instruction_id}", status_code=status.HTTP_202_ACCEPTED, response_model=InstructionResponse)
async def change_instruction(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), instruction_id: UUID, instruction: InstructionUpdate):
    db_instruction = get_instruction_by_id(db , instruction_id)

    if not db_instruction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {instruction_id} as Instruction is not found"
        )

    if not any(value is not None for value in instruction.dict().values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must include at least one field to update"
        )

    instruction_update = put_instruction(db, instruction_id, instruction)
    result_message = f"ID {instruction_id} of Instruction is updated successfully for ID {db_instruction.recipe_id} of Recipe"

    return {"detail": result_message, "instruction": instruction_update}

@router.delete("/{instruction_id}", status_code=status.HTTP_200_OK)
async def remove_instruction(*, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user), instruction_id: UUID):
    db_instruction = get_instruction_by_id(db , instruction_id)

    if not db_instruction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"ID {instruction_id} as Instruction is not found"
        )

    delete_instruction(db, instruction_id)
    result_message = f"ID {instruction_id} as Instruction is deleted successfully for ID {db_instruction.recipe_id} of Recipe"

    return {"detail": result_message}
