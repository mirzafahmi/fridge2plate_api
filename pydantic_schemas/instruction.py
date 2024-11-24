from .lowercase_base_model import LowercaseBaseModel
from datetime import datetime
from typing import List, Optional, Any, Text
from uuid import UUID 


class InstructionBase(LowercaseBaseModel):
    step_number: int
    description: Text

    model_config = {
        "transform_fields": ["description"]
    }

class InstructionCreate(InstructionBase):
    ...

class InstructionCreateSeeder(InstructionCreate):
    id: Optional[UUID] = None

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

class InstructionUpdate(InstructionBase):
    step_number: Optional[int] = None
    description: Optional[Text] = None
    recipe_id: Optional[UUID] = None

class InstructionsByRecipe(LowercaseBaseModel):
    recipe_id: UUID
    instructions: List[Instruction]

class InstructionResponse(LowercaseBaseModel):
    detail: str
    instructions: List[Instruction]