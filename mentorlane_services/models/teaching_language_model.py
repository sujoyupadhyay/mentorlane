from pydantic import BaseModel, Field
from typing import Optional


class TeachingLanguageBase(BaseModel):
    """Base Pydantic model for TeachingLanguage."""
    teaching_language: str = Field(..., max_length=20, description="Teaching language name")
    IsActive: bool = Field(..., description="Whether the teaching language is active")


class TeachingLanguageCreate(TeachingLanguageBase):
    """Pydantic model for creating a new teaching language."""
    pass


class TeachingLanguageUpdate(BaseModel):
    """Pydantic model for updating an existing teaching language."""
    teaching_language: Optional[str] = Field(None, max_length=20, description="Teaching language name")
    IsActive: Optional[bool] = Field(None, description="Whether the teaching language is active")


class TeachingLanguageResponse(TeachingLanguageBase):
    """Pydantic model for teaching language response."""
    teaching_languages_id: str = Field(..., description="Unique identifier (UUID) for the teaching language")

    class Config:
        from_attributes = True
