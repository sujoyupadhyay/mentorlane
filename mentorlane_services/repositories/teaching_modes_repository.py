from sqlalchemy import Column, String, Boolean
from core.database import Base, get_db
from models.teaching_modes_model import TeachingModeResponse, TeachingModeCreate, TeachingModeUpdate
from typing import List, Optional
import uuid


# SQLAlchemy ORM Model for teaching_modes table
class TeachingModeORM(Base):
    """SQLAlchemy ORM model for teaching_modes table."""
    __tablename__ = "teaching_modes"

    teaching_mode_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    teaching_mode = Column(String(20), nullable=False)
    IsActive = Column(Boolean, nullable=False, default=False)


class TeachingModeRepository:
    """Repository for teaching_modes database operations."""

    def __init__(self, db):
        self.db = db

    def get_all_teaching_modes(self, skip: int = 0, limit: int = 100) -> List[TeachingModeResponse]:
        """
        Fetch all teaching modes from the database.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of TeachingModeResponse objects
        """
        try:
            teaching_modes = self.db.query(TeachingModeORM).offset(skip).limit(limit).all()
            return [TeachingModeResponse.model_validate(mode) for mode in teaching_modes]
        except Exception as e:
            self.db.rollback()
            raise e

    def get_teaching_mode_by_id(self, teaching_mode_id: str) -> Optional[TeachingModeResponse]:
        """
        Fetch a specific teaching mode by ID.
        
        Args:
            teaching_mode_id: The UUID of the teaching mode to fetch
            
        Returns:
            TeachingModeResponse object if found, None otherwise
        """
        try:
            teaching_mode = self.db.query(TeachingModeORM).filter(
                TeachingModeORM.teaching_mode_id == teaching_mode_id
            ).first()
            
            if teaching_mode:
                return TeachingModeResponse.model_validate(teaching_mode)
            return None
        except Exception as e:
            self.db.rollback()
            raise e

    def get_active_teaching_modes(self, skip: int = 0, limit: int = 100) -> List[TeachingModeResponse]:
        """
        Fetch all active teaching modes from the database.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            List of TeachingModeResponse objects
        """
        try:
            teaching_modes = self.db.query(TeachingModeORM).filter(
                TeachingModeORM.IsActive == True
            ).offset(skip).limit(limit).all()
            return [TeachingModeResponse.model_validate(mode) for mode in teaching_modes]
        except Exception as e:
            self.db.rollback()
            raise e

    def create_teaching_mode(self, teaching_mode: TeachingModeCreate) -> TeachingModeResponse:
        """
        Create a new teaching mode.
        
        Args:
            teaching_mode: TeachingModeCreate object with the data to create
            
        Returns:
            TeachingModeResponse object of the created teaching mode
        """
        try:
            db_teaching_mode = TeachingModeORM(
                teaching_mode=teaching_mode.teaching_mode,
                IsActive=teaching_mode.IsActive
            )
            self.db.add(db_teaching_mode)
            self.db.commit()
            self.db.refresh(db_teaching_mode)
            return TeachingModeResponse.model_validate(db_teaching_mode)
        except Exception as e:
            self.db.rollback()
            raise e

    def update_teaching_mode(self, teaching_mode_id: str, teaching_mode: TeachingModeUpdate) -> Optional[TeachingModeResponse]:
        """
        Update an existing teaching mode.
        
        Args:
            teaching_mode_id: The UUID of the teaching mode to update
            teaching_mode: TeachingModeUpdate object with the data to update
            
        Returns:
            TeachingModeResponse object if updated successfully, None if not found
        """
        try:
            db_teaching_mode = self.db.query(TeachingModeORM).filter(
                TeachingModeORM.teaching_mode_id == teaching_mode_id
            ).first()
            
            if not db_teaching_mode:
                return None
            
            update_data = teaching_mode.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_teaching_mode, key, value)
            
            self.db.commit()
            self.db.refresh(db_teaching_mode)
            return TeachingModeResponse.model_validate(db_teaching_mode)
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_teaching_mode(self, teaching_mode_id: str) -> bool:
        """
        Delete a teaching mode by ID.
        
        Args:
            teaching_mode_id: The UUID of the teaching mode to delete
            
        Returns:
            True if deleted successfully, False if not found
        """
        try:
            db_teaching_mode = self.db.query(TeachingModeORM).filter(
                TeachingModeORM.teaching_mode_id == teaching_mode_id
            ).first()
            
            if not db_teaching_mode:
                return False
            
            self.db.delete(db_teaching_mode)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise e


# Helper function to get repository instance
def get_teaching_mode_repository(db):
    """Get a TeachingModeRepository instance with the given database session."""
    return TeachingModeRepository(db)
