from fastapi import APIRouter, Depends, HTTPException
from core.database import get_db
from core.security import get_api_key
from services.teaching_language_service import get_teaching_language_service
from models.teaching_language_model import TeachingLanguageResponse, TeachingLanguageCreate, TeachingLanguageUpdate

# Create API router for teaching languages
router = APIRouter(prefix="/api/v1/teaching-languages", tags=["Teaching Languages"])

# Teaching Languages endpoints
@router.get(
    "/",
    summary="Get all teaching languages",
    description="Retrieve all teaching languages from the database"
)
def get_teaching_languages(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get all teaching languages with pagination support."""
    service = get_teaching_language_service(db)
    return service.get_all_teaching_languages(skip=skip, limit=limit)

@router.get(
    "/active",
    summary="Get active teaching languages",
    description="Retrieve only active teaching languages from the database"
)
def get_active_teaching_languages(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get active teaching languages with pagination support."""
    service = get_teaching_language_service(db)
    return service.get_active_teaching_languages(skip=skip, limit=limit)

@router.get(
    "/{teaching_languages_id}",
    summary="Get teaching language by ID",
    description="Retrieve a specific teaching language by its UUID",
    responses={
        200: {"description": "Teaching language found"},
        404: {"description": "Teaching language not found"}
    }
)
def get_teaching_language(
    teaching_languages_id: str,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get a specific teaching language by UUID."""
    service = get_teaching_language_service(db)
    try:
        return service.get_teaching_language_by_id(teaching_languages_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    "/",
    summary="Create new teaching language",
    description="Create a new teaching language in the database",
    responses={
        201: {"description": "Teaching language created successfully"},
        400: {"description": "Invalid input data"}
    }
)
def create_teaching_language(
    teaching_language: TeachingLanguageCreate,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Create a new teaching language."""
    service = get_teaching_language_service(db)
    try:
        return service.create_teaching_language(teaching_language)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put(
    "/{teaching_languages_id}",
    summary="Update teaching language",
    description="Update an existing teaching language",
    responses={
        200: {"description": "Teaching language updated successfully"},
        404: {"description": "Teaching language not found"}
    }
)
def update_teaching_language(
    teaching_languages_id: str,
    teaching_language: TeachingLanguageUpdate,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Update an existing teaching language."""
    service = get_teaching_language_service(db)
    try:
        return service.update_teaching_language(teaching_languages_id, teaching_language)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete(
    "/{teaching_languages_id}",
    summary="Delete teaching language",
    description="Delete a teaching language by UUID",
    responses={
        200: {"description": "Teaching language deleted successfully"},
        404: {"description": "Teaching language not found"}
    }
)
def delete_teaching_language(
    teaching_languages_id: str,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Delete a teaching language by UUID."""
    service = get_teaching_language_service(db)
    try:
        service.delete_teaching_language(teaching_languages_id)
        return {"message": "Teaching language deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    "/{teaching_languages_id}/activate",
    summary="Activate teaching language",
    description="Set a teaching language as active",
    responses={
        200: {"description": "Teaching language activated successfully"},
        404: {"description": "Teaching language not found"}
    }
)
def activate_teaching_language(
    teaching_languages_id: str,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Activate a teaching language."""
    service = get_teaching_language_service(db)
    try:
        return service.activate_teaching_language(teaching_languages_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    "/{teaching_languages_id}/deactivate",
    summary="Deactivate teaching language",
    description="Set a teaching language as inactive",
    responses={
        200: {"description": "Teaching language deactivated successfully"},
        404: {"description": "Teaching language not found"}
    }
)
def deactivate_teaching_language(
    teaching_languages_id: str,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Deactivate a teaching language."""
    service = get_teaching_language_service(db)
    try:
        return service.deactivate_teaching_language(teaching_languages_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get(
    "/search/{search_term}",
    summary="Search teaching languages",
    description="Search teaching languages by name"
)
def search_teaching_languages(
    search_term: str,
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Search teaching languages by name."""
    service = get_teaching_language_service(db)
    try:
        return service.search_teaching_languages(search_term, skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
