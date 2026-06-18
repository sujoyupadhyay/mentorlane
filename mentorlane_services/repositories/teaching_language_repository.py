from sqlalchemy import Column, String, Boolean
from core.database import Base, get_db
from models.teaching_language_model import TeachingLanguageResponse, TeachingLanguageCreate, TeachingLanguageUpdate
from typing import List, Optional
import uuid


# SQLAlchemy ORM Model for teaching_languages table
class TeachingLanguageORM(Base):
    """SQLAlchemy ORM model for teaching_languages table."""
    __tablename__ = "teaching_languages"

    teaching_languages_id = Column(String(11), primary_key=True, default=lambda: str(uuid.uuid4()))
    teaching_language = Column(String(20), nullable=False)
    IsActive = Column(Boolean, nullable=False, default=False)


class TeachingLanguageRepository:
    """Repository for teaching_languages database operations."""

    def __init__(self, db):
        self.db = db

    def get_all_teaching_languages(self, skip: int = 0, limit: int = 100) -> List[TeachingLanguageResponse]:
        """
        Fetch all teaching languages from the database.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of TeachingLanguageResponse objects
        """
        try:
            teaching_languages = self.db.query(TeachingLanguageORM).offset(skip).limit(limit).all()
            return [TeachingLanguageResponse.model_validate(lang) for lang in teaching_languages]
        except Exception as e:
            self.db.rollback()
            raise e

    def get_teaching_language_by_id(self, teaching_languages_id: str) -> Optional[TeachingLanguageResponse]:
        """
        Fetch a specific teaching language by ID.
        
        Args:
            teaching_languages_id: The UUID of the teaching language to fetch
            
        Returns:
            TeachingLanguageResponse object if found, None otherwise
        """
        try:
            teaching_language = self.db.query(TeachingLanguageORM).filter(
                TeachingLanguageORM.teaching_languages_id == teaching_languages_id
            ).first()
            
            if teaching_language:
                return TeachingLanguageResponse.model_validate(teaching_language)
            return None
        except Exception as e:
            self.db.rollback()
            raise e

    def get_active_teaching_languages(self, skip: int = 0, limit: int = 100) -> List[TeachingLanguageResponse]:
        """
        Fetch all active teaching languages from the database.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of TeachingLanguageResponse objects
        """
        try:
            teaching_languages = self.db.query(TeachingLanguageORM).filter(
                TeachingLanguageORM.IsActive == True
            ).offset(skip).limit(limit).all()
            return [TeachingLanguageResponse.model_validate(lang) for lang in teaching_languages]
        except Exception as e:
            self.db.rollback()
            raise e

    def create_teaching_language(self, teaching_language: TeachingLanguageCreate) -> TeachingLanguageResponse:
        """
        Create a new teaching language.
        
        Args:
            teaching_language: TeachingLanguageCreate object with the data to create
            
        Returns:
            TeachingLanguageResponse object of the created teaching language
        """
        try:
            db_teaching_language = TeachingLanguageORM(
                teaching_language=teaching_language.teaching_language,
                IsActive=teaching_language.IsActive
            )
            self.db.add(db_teaching_language)
            self.db.commit()
            self.db.refresh(db_teaching_language)
            return TeachingLanguageResponse.model_validate(db_teaching_language)
        except Exception as e:
            self.db.rollback()
            raise e

    def update_teaching_language(self, teaching_languages_id: str, teaching_language: TeachingLanguageUpdate) -> Optional[TeachingLanguageResponse]:
        """
        Update an existing teaching language.
        
        Args:
            teaching_languages_id: The UUID of the teaching language to update
            teaching_language: TeachingLanguageUpdate object with the data to update
            
        Returns:
            TeachingLanguageResponse object if updated successfully, None if not found
        """
        try:
            db_teaching_language = self.db.query(TeachingLanguageORM).filter(
                TeachingLanguageORM.teaching_languages_id == teaching_languages_id
            ).first()
            
            if not db_teaching_language:
                return None
            
            update_data = teaching_language.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_teaching_language, key, value)
            
            self.db.commit()
            self.db.refresh(db_teaching_language)
            return TeachingLanguageResponse.model_validate(db_teaching_language)
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_teaching_language(self, teaching_languages_id: str) -> bool:
        """
        Delete a teaching language by ID.
        
        Args:
            teaching_languages_id: The UUID of the teaching language to delete
            
        Returns:
            True if deleted successfully, False if not found
        """
        try:
            db_teaching_language = self.db.query(TeachingLanguageORM).filter(
                TeachingLanguageORM.teaching_languages_id == teaching_languages_id
            ).first()
            
            if not db_teaching_language:
                return False
            
            self.db.delete(db_teaching_language)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e


# Helper function to get repository instance
def get_teaching_language_repository(db):
    """Get a TeachingLanguageRepository instance with the given database session."""
    return TeachingLanguageRepository(db)
