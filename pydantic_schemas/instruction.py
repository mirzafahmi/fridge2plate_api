from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Text, Any
from pydantic import constr, validator
from uuid import UUID 


class InstructionBase(LowercaseBaseModel):
    step_number: int
    description: constr(strip_whitespace=True, min_length=3)

    @validator("step_number")
    def validate_step_number(cls, value):
        if value <= 0:
            raise ValueError("step_number must be a positive integer")
        return value

    model_config = {
        "transform_fields": ["description"]
    }

class InstructionCreate(InstructionBase):
    ...

class InstructionCreateV2(InstructionBase):
    recipe_id: UUID

class InstructionCreateSeeder(InstructionCreate):
    id: Optional[UUID] = None

class InstructionUpdate(LowercaseBaseModel):
    description: constr(strip_whitespace=True, min_length=3)

class Instruction(LowercaseBaseModel):
    id: UUID
    step_number: int
    description: Text
    recipe_id: UUID

    class Config:
        from_attributes = True

class InstructionLite(LowercaseBaseModel):
    step_number: int
    description: Text

    class Config:
        from_attributes = True

class InstructionsByRecipe(LowercaseBaseModel):
    recipe_id: UUID
    instructions: List[Instruction]

    def model_post_init(self, __context: Any) -> None:
        self.instructions = sorted(
            self.instructions, 
            key=lambda instruction: (instruction.recipe_id, instruction.step_number)
        )

class InstructionResponse(LowercaseBaseModel):
    detail: str
    instruction: Instruction

class InstructionsResponse(LowercaseBaseModel):
    detail: str
    instructions: List[Instruction]