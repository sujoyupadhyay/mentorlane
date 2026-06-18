from fastapi import APIRouter, Depends, HTTPException
from core.database import get_db
from core.security import get_api_key
from services.teaching_levels_service import get_teaching_level_service
from models.teaching_levels_model import TeachingLevelResponse, TeachingLevelCreate, TeachingLevelUpdate

# Create API router for teaching levels
router = APIRouter(prefix="/api/v1/teaching-levels", tags=["Teaching Levels"])

# Teaching Levels endpoints
@router.get(
    "/",
    summary="Get all teaching levels",
    description="Retrieve all teaching levels from the database"
)
def get_teaching_levels(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get all teaching levels with pagination support."""
    service = get_teaching_level_service(db)
    return service.get_all_teaching_levels(skip=skip, limit=limit)

@router.get(
    "/active",
    summary="Get active teaching levels",
    description="Retrieve only active teaching levels from the database"
)
def get_active_teaching_levels(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get active teaching levels with pagination support."""
    service = get_teaching_level_service(db)
    return service.get_active_teaching_levels(skip=skip, limit=limit)

@router.get(
    "/{teaching_levels_id}",
    summary="Get teaching level by ID",
    description="Retrieve a specific teaching level by its UUID",
    responses={
        200: {"description": "Teaching level found"},
        404: {"description": "Teaching level not found"}
    }
)
def get_teaching_level(
    teaching_levels_id: str,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get a specific teaching level by UUID."""
    service = get_teaching_level_service(db)
    try:
        return service.get_teaching_level_by_id(teaching_levels_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    "/",
    summary="Create new teaching level",
    description="Create a new teaching level in the database",
    responses={
        201: {"description": "Teaching level created successfully"},
        400: {"description": "Invalid input data"}
    }
)
def create_teaching_level(
    teaching_level: TeachingLevelCreate,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Create a new teaching level."""
    service = get_teaching_level_service(db)
    try:
        return service.create_teaching_level(teaching_level)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put(
    "/{teaching_levels_id}",
    summary="Update teaching level",
    description="Update an existing teaching level",
    responses={
        200: {"description": "Teaching level updated successfully"},
        404: {"description": "Teaching level not found"}
    }
)
def update_teaching_level(
    teaching_levels_id: str,
    teaching_level: TeachingLevelUpdate,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Update an existing teaching level."""
    service = get_teaching_level_service(db)
    try:
        return service.update_teaching_level(teaching_levels_id, teaching_level)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete(
    "/{teaching_levels_id}",
    summary="Delete teaching level",
    description="Delete a teaching level by UUID",
    responses={
        200: {"description": "Teaching level deleted successfully"},
        404: {"description": "Teaching level not found"}
    }
)
def delete_teaching_level(
    teaching_levels_id: str,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Delete a teaching level by UUID."""
    service = get_teaching_level_service(db)
    try:
        service.delete_teaching_level(teaching_levels_id)
        return {"message": "Teaching level deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    "/{teaching_levels_id}/activate",
    summary="Activate teaching level",
    description="Set a teaching level as active",
    responses={
        200: {"description": "Teaching level activated successfully"},
        404: {"description": "Teaching level not found"}
    }
)
def activate_teaching_level(
    teaching_levels_id: str,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Activate a teaching level."""
    service = get_teaching_level_service(db)
    try:
        return service.activate_teaching_level(teaching_levels_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    "/{teaching_levels_id}/deactivate",
    summary="Deactivate teaching level",
    description="Set a teaching level as inactive",
    responses={
        200: {"description": "Teaching level deactivated successfully"},
        404: {"description": "Teaching level not found"}
    }
)
def deactivate_teaching_level(
    teaching_levels_id: str,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Deactivate a teaching level."""
    service = get_teaching_level_service(db)
    try:
        return service.deactivate_teaching_level(teaching_levels_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get(
    "/search/{search_term}",
    summary="Search teaching levels",
    description="Search teaching levels by name or description"
)
def search_teaching_levels(
    search_term: str,
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db)
):
    """Search teaching levels by name or description."""
    service = get_teaching_level_service(db)
    try:
        return service.search_teaching_levels(search_term, skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
