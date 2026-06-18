from pydantic import BaseModel, Field
from typing import Optional


class TeachingModeBase(BaseModel):
    """Base Pydantic model for TeachingMode."""
    teaching_mode: str = Field(..., max_length=20, description="Teaching mode name")
    IsActive: bool = Field(..., description="Whether the teaching mode is active")


class TeachingModeCreate(TeachingModeBase):
    """Pydantic model for creating a new teaching mode."""
    pass


class TeachingModeUpdate(BaseModel):
    """Pydantic model for updating an existing teaching mode."""
    teaching_mode: Optional[str] = Field(None, max_length=20, description="Teaching mode name")
    IsActive: Optional[bool] = Field(None, description="Whether the teaching mode is active")


class TeachingModeResponse(TeachingModeBase):
    """Pydantic model for teaching mode response."""
    teaching_mode_id: str = Field(..., description="Unique identifier (UUID) for the teaching mode")

    class Config:
        from_attributes = True
