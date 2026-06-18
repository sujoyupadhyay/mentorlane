from pydantic import BaseModel, Field
from typing import Optional


class TeachingLevelBase(BaseModel):
    """Base Pydantic model for TeachingLevel."""
    teaching_level_name: str = Field(..., max_length=20, description="Teaching level name")
    teaching_level_description: str = Field(..., max_length=200, description="Teaching level description")
    IsActive: bool = Field(..., description="Whether the teaching level is active")


class TeachingLevelCreate(TeachingLevelBase):
    """Pydantic model for creating a new teaching level."""
    pass


class TeachingLevelUpdate(BaseModel):
    """Pydantic model for updating an existing teaching level."""
    teaching_level_name: Optional[str] = Field(None, max_length=20, description="Teaching level name")
    teaching_level_description: Optional[str] = Field(None, max_length=200, description="Teaching level description")
    IsActive: Optional[bool] = Field(None, description="Whether the teaching level is active")


class TeachingLevelResponse(TeachingLevelBase):
    """Pydantic model for teaching level response."""
    teaching_levels_id: str = Field(..., description="Unique identifier (UUID) for the teaching level")

    class Config:
        from_attributes = True
