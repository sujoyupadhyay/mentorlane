from sqlalchemy import Column, String, Boolean
from core.database import Base, get_db
from models.teaching_levels_model import TeachingLevelResponse, TeachingLevelCreate, TeachingLevelUpdate
from typing import List, Optional
import uuid


# SQLAlchemy ORM Model for teaching_levels table
class TeachingLevelORM(Base):
    """SQLAlchemy ORM model for teaching_levels table."""
    __tablename__ = "teaching_levels"

    teaching_levels_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    teaching_level_name = Column(String(20), nullable=False)
    teaching_level_description = Column(String(200), nullable=False)
    IsActive = Column(Boolean, nullable=False, default=False)


class TeachingLevelRepository:
    """Repository for teaching_levels database operations."""

    def __init__(self, db):
        self.db = db

    def get_all_teaching_levels(self, skip: int = 0, limit: int = 100) -> List[TeachingLevelResponse]:
        """
        Fetch all teaching levels from the database.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of TeachingLevelResponse objects
        """
        try:
            teaching_levels = self.db.query(TeachingLevelORM).offset(skip).limit(limit).all()
            return [TeachingLevelResponse.model_validate(level) for level in teaching_levels]
        except Exception as e:
            self.db.rollback()
            raise e

    def get_teaching_level_by_id(self, teaching_levels_id: str) -> Optional[TeachingLevelResponse]:
        """
        Fetch a specific teaching level by ID.
        
        Args:
            teaching_levels_id: The UUID of the teaching level to fetch
            
        Returns:
            TeachingLevelResponse object if found, None otherwise
        """
        try:
            teaching_level = self.db.query(TeachingLevelORM).filter(
                TeachingLevelORM.teaching_levels_id == teaching_levels_id
            ).first()
            
            if teaching_level:
                return TeachingLevelResponse.model_validate(teaching_level)
            return None
        except Exception as e:
            self.db.rollback()
            raise e

    def get_active_teaching_levels(self, skip: int = 0, limit: int = 100) -> List[TeachingLevelResponse]:
        """
        Fetch all active teaching levels from the database.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of TeachingLevelResponse objects
        """
        try:
            teaching_levels = self.db.query(TeachingLevelORM).filter(
                TeachingLevelORM.IsActive == True
            ).offset(skip).limit(limit).all()
            return [TeachingLevelResponse.model_validate(level) for level in teaching_levels]
        except Exception as e:
            self.db.rollback()
            raise e

    def create_teaching_level(self, teaching_level: TeachingLevelCreate) -> TeachingLevelResponse:
        """
        Create a new teaching level.
        
        Args:
            teaching_level: TeachingLevelCreate object with the data to create
            
        Returns:
            TeachingLevelResponse object of the created teaching level
        """
        try:
            db_teaching_level = TeachingLevelORM(
                teaching_level_name=teaching_level.teaching_level_name,
                teaching_level_description=teaching_level.teaching_level_description,
                IsActive=teaching_level.IsActive
            )
            self.db.add(db_teaching_level)
            self.db.commit()
            self.db.refresh(db_teaching_level)
            return TeachingLevelResponse.model_validate(db_teaching_level)
        except Exception as e:
            self.db.rollback()
            raise e

    def update_teaching_level(self, teaching_levels_id: str, teaching_level: TeachingLevelUpdate) -> Optional[TeachingLevelResponse]:
        """
        Update an existing teaching level.
        
        Args:
            teaching_levels_id: The UUID of the teaching level to update
            teaching_level: TeachingLevelUpdate object with the data to update
            
        Returns:
            TeachingLevelResponse object if updated successfully, None if not found
        """
        try:
            db_teaching_level = self.db.query(TeachingLevelORM).filter(
                TeachingLevelORM.teaching_levels_id == teaching_levels_id
            ).first()
            
            if not db_teaching_level:
                return None
            
            update_data = teaching_level.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_teaching_level, key, value)
            
            self.db.commit()
            self.db.refresh(db_teaching_level)
            return TeachingLevelResponse.model_validate(db_teaching_level)
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_teaching_level(self, teaching_levels_id: str) -> bool:
        """
        Delete a teaching level by ID.
        
        Args:
            teaching_levels_id: The UUID of the teaching level to delete
            
        Returns:
            True if deleted successfully, False if not found
        """
        try:
            db_teaching_level = self.db.query(TeachingLevelORM).filter(
                TeachingLevelORM.teaching_levels_id == teaching_levels_id
            ).first()
            
            if not db_teaching_level:
                return False
            
            self.db.delete(db_teaching_level)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e


# Helper function to get repository instance
def get_teaching_level_repository(db):
    """Get a TeachingLevelRepository instance with the given database session."""
    return TeachingLevelRepository(db)
