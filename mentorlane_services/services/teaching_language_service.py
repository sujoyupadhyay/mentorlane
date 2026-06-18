from typing import List, Optional
from models.teaching_language_model import TeachingLanguageResponse, TeachingLanguageCreate, TeachingLanguageUpdate
from repositories.teaching_language_repository import TeachingLanguageRepository, get_teaching_language_repository


class TeachingLanguageService:
    """Service layer for teaching languages business logic."""

    def __init__(self, repository: TeachingLanguageRepository):
        self.repository = repository

    def get_all_teaching_languages(self, skip: int = 0, limit: int = 100) -> dict:
        """
        Get all teaching languages with pagination and business logic.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            Dictionary containing teaching languages data and metadata
        """
        # Validate pagination parameters
        if skip < 0:
            raise ValueError("Skip parameter cannot be negative")
        if limit <= 0 or limit > 1000:
            raise ValueError("Limit parameter must be between 1 and 1000")
        
        # Fetch data from repository
        teaching_languages = self.repository.get_all_teaching_languages(skip=skip, limit=limit)
        
        # Add business logic/metadata
        return {
            "data": teaching_languages,
            "count": len(teaching_languages),
            "skip": skip,
            "limit": limit,
            "total": self._get_total_count()
        }

    def get_teaching_language_by_id(self, teaching_languages_id: str) -> TeachingLanguageResponse:
        """
        Get a specific teaching language by ID with validation.
        
        Args:
            teaching_languages_id: The UUID of the teaching language to fetch
            
        Returns:
            TeachingLanguageResponse object
            
        Raises:
            ValueError: If teaching_languages_id is invalid or teaching language not found
        """
        # Validate UUID format
        if not self._is_valid_uuid(teaching_languages_id):
            raise ValueError(f"Invalid teaching_languages_id format: {teaching_languages_id}")
        
        # Fetch from repository
        teaching_language = self.repository.get_teaching_language_by_id(teaching_languages_id)
        
        if not teaching_language:
            raise ValueError(f"Teaching language with ID {teaching_languages_id} not found")
        
        return teaching_language

    def get_active_teaching_languages(self, skip: int = 0, limit: int = 100) -> dict:
        """
        Get all active teaching languages with pagination.
        
        Args:
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            Dictionary containing active teaching languages data and metadata
        """
        # Validate pagination parameters
        if skip < 0:
            raise ValueError("Skip parameter cannot be negative")
        if limit <= 0 or limit > 1000:
            raise ValueError("Limit parameter must be between 1 and 1000")
        
        # Fetch data from repository
        teaching_languages = self.repository.get_active_teaching_languages(skip=skip, limit=limit)
        
        return {
            "data": teaching_languages,
            "count": len(teaching_languages),
            "skip": skip,
            "limit": limit,
            "active_count": len(teaching_languages)
        }

    def create_teaching_language(self, teaching_language: TeachingLanguageCreate) -> TeachingLanguageResponse:
        """
        Create a new teaching language with validation and business logic.
        
        Args:
            teaching_language: TeachingLanguageCreate object with the data to create
            
        Returns:
            TeachingLanguageResponse object of the created teaching language
            
        Raises:
            ValueError: If validation fails or teaching language already exists
        """
        # Validate teaching language name
        if not teaching_language.teaching_language or len(teaching_language.teaching_language.strip()) == 0:
            raise ValueError("Teaching language name cannot be empty")
        
        if len(teaching_language.teaching_language) > 20:
            raise ValueError("Teaching language name cannot exceed 20 characters")
        
        # Check if teaching language with same name already exists
        existing_languages = self.repository.get_all_teaching_languages(skip=0, limit=1000)
        for language in existing_languages:
            if language.teaching_language.lower() == teaching_language.teaching_language.lower():
                raise ValueError(f"Teaching language '{teaching_language.teaching_language}' already exists")
        
        # Create teaching language through repository
        return self.repository.create_teaching_language(teaching_language)

    def update_teaching_language(self, teaching_languages_id: str, teaching_language: TeachingLanguageUpdate) -> TeachingLanguageResponse:
        """
        Update an existing teaching language with validation.
        
        Args:
            teaching_languages_id: The UUID of the teaching language to update
            teaching_language: TeachingLanguageUpdate object with the data to update
            
        Returns:
            TeachingLanguageResponse object of the updated teaching language
            
        Raises:
            ValueError: If validation fails or teaching language not found
        """
        # Validate UUID format
        if not self._is_valid_uuid(teaching_languages_id):
            raise ValueError(f"Invalid teaching_languages_id format: {teaching_languages_id}")
        
        # Validate teaching language name if provided
        if teaching_language.teaching_language is not None:
            if len(teaching_language.teaching_language.strip()) == 0:
                raise ValueError("Teaching language name cannot be empty")
            
            if len(teaching_language.teaching_language) > 20:
                raise ValueError("Teaching language name cannot exceed 20 characters")
            
            # Check for duplicate name (excluding current record)
            existing_languages = self.repository.get_all_teaching_languages(skip=0, limit=1000)
            for language in existing_languages:
                if (language.teaching_languages_id != teaching_languages_id and 
                    language.teaching_language.lower() == teaching_language.teaching_language.lower()):
                    raise ValueError(f"Teaching language '{teaching_language.teaching_language}' already exists")
        
        # Update through repository
        updated_language = self.repository.update_teaching_language(teaching_languages_id, teaching_language)
        
        if not updated_language:
            raise ValueError(f"Teaching language with ID {teaching_languages_id} not found")
        
        return updated_language

    def delete_teaching_language(self, teaching_languages_id: str) -> bool:
        """
        Delete a teaching language with validation.
        
        Args:
            teaching_languages_id: The UUID of the teaching language to delete
            
        Returns:
            True if deleted successfully
            
        Raises:
            ValueError: If validation fails or teaching language not found
        """
        # Validate UUID format
        if not self._is_valid_uuid(teaching_languages_id):
            raise ValueError(f"Invalid teaching_languages_id format: {teaching_languages_id}")
        
        # Check if teaching language exists before deletion
        teaching_language = self.repository.get_teaching_language_by_id(teaching_languages_id)
        if not teaching_language:
            raise ValueError(f"Teaching language with ID {teaching_languages_id} not found")
        
        # Delete through repository
        success = self.repository.delete_teaching_language(teaching_languages_id)
        
        if not success:
            raise ValueError(f"Failed to delete teaching language with ID {teaching_languages_id}")
        
        return True

    def activate_teaching_language(self, teaching_languages_id: str) -> TeachingLanguageResponse:
        """
        Activate a teaching language (set IsActive to true).
        
        Args:
            teaching_languages_id: The UUID of the teaching language to activate
            
        Returns:
            TeachingLanguageResponse object of the updated teaching language
            
        Raises:
            ValueError: If teaching language not found
        """
        update_data = TeachingLanguageUpdate(IsActive=True)
        return self.update_teaching_language(teaching_languages_id, update_data)

    def deactivate_teaching_language(self, teaching_languages_id: str) -> TeachingLanguageResponse:
        """
        Deactivate a teaching language (set IsActive to false).
        
        Args:
            teaching_languages_id: The UUID of the teaching language to deactivate
            
        Returns:
            TeachingLanguageResponse object of the updated teaching language
            
        Raises:
            ValueError: If teaching language not found
        """
        update_data = TeachingLanguageUpdate(IsActive=False)
        return self.update_teaching_language(teaching_languages_id, update_data)

    def search_teaching_languages(self, search_term: str, skip: int = 0, limit: int = 100) -> dict:
        """
        Search teaching languages by name.
        
        Args:
            search_term: The search term to filter teaching language names
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            
        Returns:
            Dictionary containing search results and metadata
        """
        # Validate search term
        if not search_term or len(search_term.strip()) == 0:
            raise ValueError("Search term cannot be empty")
        
        # Get all teaching languages and filter
        all_languages = self.repository.get_all_teaching_languages(skip=0, limit=1000)
        filtered_languages = [
            language for language in all_languages 
            if search_term.lower() in language.teaching_language.lower()
        ]
        
        # Apply pagination
        paginated_languages = filtered_languages[skip:skip + limit]
        
        return {
            "data": paginated_languages,
            "count": len(paginated_languages),
            "skip": skip,
            "limit": limit,
            "total_results": len(filtered_languages),
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
        Get the total count of teaching languages.
        
        Returns:
            Total number of teaching languages
        """
        all_languages = self.repository.get_all_teaching_languages(skip=0, limit=1000)
        return len(all_languages)


# Helper function to get service instance
def get_teaching_language_service(db) -> TeachingLanguageService:
    """
    Get a TeachingLanguageService instance with the given database session.
    
    Args:
        db: Database session
        
    Returns:
        TeachingLanguageService instance
    """
    repository = get_teaching_language_repository(db)
    return TeachingLanguageService(repository)
