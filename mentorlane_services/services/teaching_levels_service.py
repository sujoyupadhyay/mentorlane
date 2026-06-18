from typing import List, Optional
from models.teaching_levels_model import TeachingLevelResponse, TeachingLevelCreate, TeachingLevelUpdate
from repositories.teaching_levels_repository import TeachingLevelRepository, get_teaching_level_repository


class TeachingLevelService:
    """Service layer for teaching levels business logic."""

    def __init__(self, repository: TeachingLevelRepository):
        self.repository = repository

    def get_all_teaching_levels(self, skip: int = 0, limit: int = 100) -> dict:
        """
        Get all teaching levels with pagination and business logic.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            Dictionary containing teaching levels data and metadata
        """
        # Validate pagination parameters
        if skip < 0:
            raise ValueError("Skip parameter cannot be negative")
        if limit <= 0 or limit > 1000:
            raise ValueError("Limit parameter must be between 1 and 1000")
        
        # Fetch data from repository
        teaching_levels = self.repository.get_all_teaching_levels(skip=skip, limit=limit)
        
        # Add business logic/metadata
        return {
            "data": teaching_levels,
            "count": len(teaching_levels),
            "skip": skip,
            "limit": limit,
            "total": self._get_total_count()
        }

    def get_teaching_level_by_id(self, teaching_levels_id: str) -> TeachingLevelResponse:
        """
        Get a specific teaching level by ID with validation.
        
        Args:
            teaching_levels_id: The UUID of the teaching level to fetch
            
        Returns:
            TeachingLevelResponse object
            
        Raises:
            ValueError: If teaching_levels_id is invalid or teaching level not found
        """
        # Validate UUID format
        if not self._is_valid_uuid(teaching_levels_id):
            raise ValueError(f"Invalid teaching_levels_id format: {teaching_levels_id}")
        
        # Fetch from repository
        teaching_level = self.repository.get_teaching_level_by_id(teaching_levels_id)
        
        if not teaching_level:
            raise ValueError(f"Teaching level with ID {teaching_levels_id} not found")
        
        return teaching_level

    def get_active_teaching_levels(self, skip: int = 0, limit: int = 100) -> dict:
        """
        Get all active teaching levels with pagination.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            Dictionary containing active teaching levels data and metadata
        """
        # Validate pagination parameters
        if skip < 0:
            raise ValueError("Skip parameter cannot be negative")
        if limit <= 0 or limit > 1000:
            raise ValueError("Limit parameter must be between 1 and 1000")
        
        # Fetch data from repository
        teaching_levels = self.repository.get_active_teaching_levels(skip=skip, limit=limit)
        
        return {
            "data": teaching_levels,
            "count": len(teaching_levels),
            "skip": skip,
            "limit": limit,
            "active_count": len(teaching_levels)
        }

    def create_teaching_level(self, teaching_level: TeachingLevelCreate) -> TeachingLevelResponse:
        """
        Create a new teaching level with validation and business logic.
        
        Args:
            teaching_level: TeachingLevelCreate object with the data to create
            
        Returns:
            TeachingLevelResponse object of the created teaching level
            
        Raises:
            ValueError: If validation fails or teaching level already exists
        """
        # Validate teaching level name
        if not teaching_level.teaching_level_name or len(teaching_level.teaching_level_name.strip()) == 0:
            raise ValueError("Teaching level name cannot be empty")
        
        if len(teaching_level.teaching_level_name) > 20:
            raise ValueError("Teaching level name cannot exceed 20 characters")
        
        # Validate teaching level description
        if not teaching_level.teaching_level_description or len(teaching_level.teaching_level_description.strip()) == 0:
            raise ValueError("Teaching level description cannot be empty")
        
        if len(teaching_level.teaching_level_description) > 200:
            raise ValueError("Teaching level description cannot exceed 200 characters")
        
        # Check if teaching level with same name already exists
        existing_levels = self.repository.get_all_teaching_levels(skip=0, limit=1000)
        for level in existing_levels:
            if level.teaching_level_name.lower() == teaching_level.teaching_level_name.lower():
                raise ValueError(f"Teaching level '{teaching_level.teaching_level_name}' already exists")
        
        # Create teaching level through repository
        return self.repository.create_teaching_level(teaching_level)

    def update_teaching_level(self, teaching_levels_id: str, teaching_level: TeachingLevelUpdate) -> TeachingLevelResponse:
        """
        Update an existing teaching level with validation.
        
        Args:
            teaching_levels_id: The UUID of the teaching level to update
            teaching_level: TeachingLevelUpdate object with the data to update
            
        Returns:
            TeachingLevelResponse object of the updated teaching level
            
        Raises:
            ValueError: If validation fails or teaching level not found
        """
        # Validate UUID format
        if not self._is_valid_uuid(teaching_levels_id):
            raise ValueError(f"Invalid teaching_levels_id format: {teaching_levels_id}")
        
        # Validate teaching level name if provided
        if teaching_level.teaching_level_name is not None:
            if len(teaching_level.teaching_level_name.strip()) == 0:
                raise ValueError("Teaching level name cannot be empty")
            
            if len(teaching_level.teaching_level_name) > 20:
                raise ValueError("Teaching level name cannot exceed 20 characters")
            
            # Check for duplicate name (excluding current record)
            existing_levels = self.repository.get_all_teaching_levels(skip=0, limit=1000)
            for level in existing_levels:
                if (level.teaching_levels_id != teaching_levels_id and 
                    level.teaching_level_name.lower() == teaching_level.teaching_level_name.lower()):
                    raise ValueError(f"Teaching level '{teaching_level.teaching_level_name}' already exists")
        
        # Validate teaching level description if provided
        if teaching_level.teaching_level_description is not None:
            if len(teaching_level.teaching_level_description.strip()) == 0:
                raise ValueError("Teaching level description cannot be empty")
            
            if len(teaching_level.teaching_level_description) > 200:
                raise ValueError("Teaching level description cannot exceed 200 characters")
        
        # Update through repository
        updated_level = self.repository.update_teaching_level(teaching_levels_id, teaching_level)
        
        if not updated_level:
            raise ValueError(f"Teaching level with ID {teaching_levels_id} not found")
        
        return updated_level

    def delete_teaching_level(self, teaching_levels_id: str) -> bool:
        """
        Delete a teaching level with validation.
        
        Args:
            teaching_levels_id: The UUID of the teaching level to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            ValueError: If validation fails or teaching level not found
        """
        # Validate UUID format
        if not self._is_valid_uuid(teaching_levels_id):
            raise ValueError(f"Invalid teaching_levels_id format: {teaching_levels_id}")
        
        # Check if teaching level exists before deletion
        teaching_level = self.repository.get_teaching_level_by_id(teaching_levels_id)
        if not teaching_level:
            raise ValueError(f"Teaching level with ID {teaching_levels_id} not found")
        
        # Delete through repository
        success = self.repository.delete_teaching_level(teaching_levels_id)
        
        if not success:
            raise ValueError(f"Failed to delete teaching level with ID {teaching_levels_id}")
        
        return True

    def activate_teaching_level(self, teaching_levels_id: str) -> TeachingLevelResponse:
        """
        Activate a teaching level (set IsActive to true).
        
        Args:
            teaching_levels_id: The UUID of the teaching level to activate
            
        Returns:
            TeachingLevelResponse object of the updated teaching level
            
        Raises:
            ValueError: If teaching level not found
        """
        update_data = TeachingLevelUpdate(IsActive=True)
        return self.update_teaching_level(teaching_levels_id, update_data)

    def deactivate_teaching_level(self, teaching_levels_id: str) -> TeachingLevelResponse:
        """
        Deactivate a teaching level (set IsActive to false).
        
        Args:
            teaching_levels_id: The UUID of the teaching level to deactivate
            
        Returns:
            TeachingLevelResponse object of the updated teaching level
            
        Raises:
            ValueError: If teaching level not found
        """
        update_data = TeachingLevelUpdate(IsActive=False)
        return self.update_teaching_level(teaching_levels_id, update_data)

    def search_teaching_levels(self, search_term: str, skip: int = 0, limit: int = 100) -> dict:
        """
        Search teaching levels by name or description.
        
        Args:
            search_term: The search term to filter teaching level names or descriptions
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            Dictionary containing search results and metadata
        """
        # Validate search term
        if not search_term or len(search_term.strip()) == 0:
            raise ValueError("Search term cannot be empty")
        
        # Get all teaching levels and filter
        all_levels = self.repository.get_all_teaching_levels(skip=0, limit=1000)
        filtered_levels = [
            level for level in all_levels 
            if (search_term.lower() in level.teaching_level_name.lower() or 
                search_term.lower() in level.teaching_level_description.lower())
        ]
        
        # Apply pagination
        paginated_levels = filtered_levels[skip:skip + limit]
        
        return {
            "data": paginated_levels,
            "count": len(paginated_levels),
            "skip": skip,
            "limit": limit,
            "total_results": len(filtered_levels),
            "search_term": search_term
        }

    def _is_valid_uuid(self, uuid_string: str) -> bool:
        """
        Validate if a string is a valid UUID format.
        
        Args:
            uuid_string: The string to validate
            
        Returns:
            True if valid UUID format, False otherwise
        """
        import uuid as uuid_lib
        try:
            uuid_lib.UUID(uuid_string)
            return True
        except ValueError:
            return False

    def _get_total_count(self) -> int:
        """
        Get the total count of teaching levels.
        
        Returns:
            Total number of teaching levels
        """
        all_levels = self.repository.get_all_teaching_levels(skip=0, limit=1000)
        return len(all_levels)


# Helper function to get service instance
def get_teaching_level_service(db) -> TeachingLevelService:
    """
    Get a TeachingLevelService instance with the given database session.
    
    Args:
        db: Database session
        
    Returns:
        TeachingLevelService instance
    """
    repository = get_teaching_level_repository(db)
    return TeachingLevelService(repository)
