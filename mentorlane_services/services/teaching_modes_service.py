from typing import List, Optional
from models.teaching_modes_model import TeachingModeResponse, TeachingModeCreate, TeachingModeUpdate
from repositories.teaching_modes_repository import TeachingModeRepository, get_teaching_mode_repository


class TeachingModeService:
    """Service layer for teaching modes business logic."""

    def __init__(self, repository: TeachingModeRepository):
        self.repository = repository

    def get_all_teaching_modes(self, skip: int = 0, limit: int = 100) -> dict:
        """
        Get all teaching modes with pagination and business logic.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            Dictionary containing teaching modes data and metadata
        """
        # Validate pagination parameters
        if skip < 0:
            raise ValueError("Skip parameter cannot be negative")
        if limit <= 0 or limit > 1000:
            raise ValueError("Limit parameter must be between 1 and 1000")
        
        # Fetch data from repository
        teaching_modes = self.repository.get_all_teaching_modes(skip=skip, limit=limit)
        
        # Add business logic/metadata
        return {
            "data": teaching_modes,
            "count": len(teaching_modes),
            "skip": skip,
            "limit": limit,
            "total": self._get_total_count()
        }

    def get_teaching_mode_by_id(self, teaching_mode_id: str) -> TeachingModeResponse:
        """
        Get a specific teaching mode by ID with validation.
        
        Args:
            teaching_mode_id: The UUID of the teaching mode to fetch
            
        Returns:
            TeachingModeResponse object
            
        Raises:
            ValueError: If teaching_mode_id is invalid or teaching mode not found
        """
        # Validate UUID format
        if not self._is_valid_uuid(teaching_mode_id):
            raise ValueError(f"Invalid teaching_mode_id format: {teaching_mode_id}")
        
        # Fetch from repository
        teaching_mode = self.repository.get_teaching_mode_by_id(teaching_mode_id)
        
        if not teaching_mode:
            raise ValueError(f"Teaching mode with ID {teaching_mode_id} not found")
        
        return teaching_mode

    def get_active_teaching_modes(self, skip: int = 0, limit: int = 100) -> dict:
        """
        Get all active teaching modes with pagination.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            Dictionary containing active teaching modes data and metadata
        """
        # Validate pagination parameters
        if skip < 0:
            raise ValueError("Skip parameter cannot be negative")
        if limit <= 0 or limit > 1000:
            raise ValueError("Limit parameter must be between 1 and 1000")
        
        # Fetch data from repository
        teaching_modes = self.repository.get_active_teaching_modes(skip=skip, limit=limit)
        
        return {
            "data": teaching_modes,
            "count": len(teaching_modes),
            "skip": skip,
            "limit": limit,
            "active_count": len(teaching_modes)
        }

    def create_teaching_mode(self, teaching_mode: TeachingModeCreate) -> TeachingModeResponse:
        """
        Create a new teaching mode with validation and business logic.
        
        Args:
            teaching_mode: TeachingModeCreate object with the data to create
            
        Returns:
            TeachingModeResponse object of the created teaching mode
            
        Raises:
            ValueError: If validation fails or teaching mode already exists
        """
        # Validate teaching mode name
        if not teaching_mode.teaching_mode or len(teaching_mode.teaching_mode.strip()) == 0:
            raise ValueError("Teaching mode name cannot be empty")
        
        if len(teaching_mode.teaching_mode) > 20:
            raise ValueError("Teaching mode name cannot exceed 20 characters")
        
        # Check if teaching mode with same name already exists
        existing_modes = self.repository.get_all_teaching_modes(skip=0, limit=1000)
        for mode in existing_modes:
            if mode.teaching_mode.lower() == teaching_mode.teaching_mode.lower():
                raise ValueError(f"Teaching mode '{teaching_mode.teaching_mode}' already exists")
        
        # Create teaching mode through repository
        return self.repository.create_teaching_mode(teaching_mode)

    def update_teaching_mode(self, teaching_mode_id: str, teaching_mode: TeachingModeUpdate) -> TeachingModeResponse:
        """
        Update an existing teaching mode with validation.
        
        Args:
            teaching_mode_id: The UUID of the teaching mode to update
            teaching_mode: TeachingModeUpdate object with the data to update
            
        Returns:
            TeachingModeResponse object of the updated teaching mode
            
        Raises:
            ValueError: If validation fails or teaching mode not found
        """
        # Validate UUID format
        if not self._is_valid_uuid(teaching_mode_id):
            raise ValueError(f"Invalid teaching_mode_id format: {teaching_mode_id}")
        
        # Validate teaching mode name if provided
        if teaching_mode.teaching_mode is not None:
            if len(teaching_mode.teaching_mode.strip()) == 0:
                raise ValueError("Teaching mode name cannot be empty")
            
            if len(teaching_mode.teaching_mode) > 20:
                raise ValueError("Teaching mode name cannot exceed 20 characters")
            
            # Check for duplicate name (excluding current record)
            existing_modes = self.repository.get_all_teaching_modes(skip=0, limit=1000)
            for mode in existing_modes:
                if (mode.teaching_mode_id != teaching_mode_id and 
                    mode.teaching_mode.lower() == teaching_mode.teaching_mode.lower()):
                    raise ValueError(f"Teaching mode '{teaching_mode.teaching_mode}' already exists")
        
        # Update through repository
        updated_mode = self.repository.update_teaching_mode(teaching_mode_id, teaching_mode)
        
        if not updated_mode:
            raise ValueError(f"Teaching mode with ID {teaching_mode_id} not found")
        
        return updated_mode

    def delete_teaching_mode(self, teaching_mode_id: str) -> bool:
        """
        Delete a teaching mode with validation.
        
        Args:
            teaching_mode_id: The UUID of the teaching mode to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            ValueError: If validation fails or teaching mode not found
        """
        # Validate UUID format
        if not self._is_valid_uuid(teaching_mode_id):
            raise ValueError(f"Invalid teaching_mode_id format: {teaching_mode_id}")
        
        # Check if teaching mode exists before deletion
        teaching_mode = self.repository.get_teaching_mode_by_id(teaching_mode_id)
        if not teaching_mode:
            raise ValueError(f"Teaching mode with ID {teaching_mode_id} not found")
        
        # Delete through repository
        success = self.repository.delete_teaching_mode(teaching_mode_id)
        
        if not success:
            raise ValueError(f"Failed to delete teaching mode with ID {teaching_mode_id}")
        
        return True

    def activate_teaching_mode(self, teaching_mode_id: str) -> TeachingModeResponse:
        """
        Activate a teaching mode (set IsActive to true).
        
        Args:
            teaching_mode_id: The UUID of the teaching mode to activate
            
        Returns:
            TeachingModeResponse object of the updated teaching mode
            
        Raises:
            ValueError: If teaching mode not found
        """
        update_data = TeachingModeUpdate(IsActive=True)
        return self.update_teaching_mode(teaching_mode_id, update_data)

    def deactivate_teaching_mode(self, teaching_mode_id: str) -> TeachingModeResponse:
        """
        Deactivate a teaching mode (set IsActive to false).
        
        Args:
            teaching_mode_id: The UUID of the teaching mode to deactivate
            
        Returns:
            TeachingModeResponse object of the updated teaching mode
            
        Raises:
            ValueError: If teaching mode not found
        """
        update_data = TeachingModeUpdate(IsActive=False)
        return self.update_teaching_mode(teaching_mode_id, update_data)

    def search_teaching_modes(self, search_term: str, skip: int = 0, limit: int = 100) -> dict:
        """
        Search teaching modes by name.
        
        Args:
            search_term: The search term to filter teaching mode names
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            Dictionary containing search results and metadata
        """
        # Validate search term
        if not search_term or len(search_term.strip()) == 0:
            raise ValueError("Search term cannot be empty")
        
        # Get all teaching modes and filter
        all_modes = self.repository.get_all_teaching_modes(skip=0, limit=1000)
        filtered_modes = [
            mode for mode in all_modes 
            if search_term.lower() in mode.teaching_mode.lower()
        ]
        
        # Apply pagination
        paginated_modes = filtered_modes[skip:skip + limit]
        
        return {
            "data": paginated_modes,
            "count": len(paginated_modes),
            "skip": skip,
            "limit": limit,
            "total_results": len(filtered_modes),
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
        Get the total count of teaching modes.
        
        Returns:
            Total number of teaching modes
        """
        all_modes = self.repository.get_all_teaching_modes(skip=0, limit=1000)
        return len(all_modes)


# Helper function to get service instance
def get_teaching_mode_service(db) -> TeachingModeService:
    """
    Get a TeachingModeService instance with the given database session.
    
    Args:
        db: Database session
        
    Returns:
        TeachingModeService instance
    """
    repository = get_teaching_mode_repository(db)
    return TeachingModeService(repository)
