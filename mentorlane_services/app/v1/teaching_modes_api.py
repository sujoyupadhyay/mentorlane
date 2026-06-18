from fastapi import APIRouter, Depends, HTTPException
from core.database import get_db
from core.security import get_api_key
from services.teaching_modes_service import get_teaching_mode_service
from models.teaching_modes_model import TeachingModeResponse, TeachingModeCreate, TeachingModeUpdate

# Create API router for teaching modes
router = APIRouter(prefix="/api/v1/teaching-modes", tags=["Teaching Modes"])

# Teaching Modes endpoints
@router.get(
    "/",
    summary="Get all teaching modes",
    description="Retrieve all teaching modes from the database"
)
def get_teaching_modes(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get all teaching modes with pagination support."""
    service = get_teaching_mode_service(db)
    return service.get_all_teaching_modes(skip=skip, limit=limit)

@router.get(
    "/active",
    summary="Get active teaching modes",
    description="Retrieve only active teaching modes from the database"
)
def get_active_teaching_modes(
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get active teaching modes with pagination support."""
    service = get_teaching_mode_service(db)
    return service.get_active_teaching_modes(skip=skip, limit=limit)

@router.get(
    "/{teaching_mode_id}",
    summary="Get teaching mode by ID",
    description="Retrieve a specific teaching mode by its UUID",
    responses={
        200: {"description": "Teaching mode found"},
        404: {"description": "Teaching mode not found"}
    }
)
def get_teaching_mode(
    teaching_mode_id: str,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Get a specific teaching mode by UUID."""
    service = get_teaching_mode_service(db)
    try:
        return service.get_teaching_mode_by_id(teaching_mode_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    "/",
    summary="Create new teaching mode",
    description="Create a new teaching mode in the database",
    responses={
        201: {"description": "Teaching mode created successfully"},
        400: {"description": "Invalid input data"}
    }
)
def create_teaching_mode(
    teaching_mode: TeachingModeCreate,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Create a new teaching mode."""
    service = get_teaching_mode_service(db)
    try:
        return service.create_teaching_mode(teaching_mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put(
    "/{teaching_mode_id}",
    summary="Update teaching mode",
    description="Update an existing teaching mode",
    responses={
        200: {"description": "Teaching mode updated successfully"},
        404: {"description": "Teaching mode not found"}
    }
)
def update_teaching_mode(
    teaching_mode_id: str,
    teaching_mode: TeachingModeUpdate,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Update an existing teaching mode."""
    service = get_teaching_mode_service(db)
    try:
        return service.update_teaching_mode(teaching_mode_id, teaching_mode)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete(
    "/{teaching_mode_id}",
    summary="Delete teaching mode",
    description="Delete a teaching mode by UUID",
    responses={
        200: {"description": "Teaching mode deleted successfully"},
        404: {"description": "Teaching mode not found"}
    }
)
def delete_teaching_mode(
    teaching_mode_id: str,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Delete a teaching mode by UUID."""
    service = get_teaching_mode_service(db)
    try:
        service.delete_teaching_mode(teaching_mode_id)
        return {"message": "Teaching mode deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    "/{teaching_mode_id}/activate",
    summary="Activate teaching mode",
    description="Set a teaching mode as active",
    responses={
        200: {"description": "Teaching mode activated successfully"},
        404: {"description": "Teaching mode not found"}
    }
)
def activate_teaching_mode(
    teaching_mode_id: str,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Activate a teaching mode."""
    service = get_teaching_mode_service(db)
    try:
        return service.activate_teaching_mode(teaching_mode_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    "/{teaching_mode_id}/deactivate",
    summary="Deactivate teaching mode",
    description="Set a teaching mode as inactive",
    responses={
        200: {"description": "Teaching mode deactivated successfully"},
        404: {"description": "Teaching mode not found"}
    }
)
def deactivate_teaching_mode(
    teaching_mode_id: str,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Deactivate a teaching mode."""
    service = get_teaching_mode_service(db)
    try:
        return service.deactivate_teaching_mode(teaching_mode_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get(
    "/search/{search_term}",
    summary="Search teaching modes",
    description="Search teaching modes by name"
)
def search_teaching_modes(
    search_term: str,
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Search teaching modes by name."""
    service = get_teaching_mode_service(db)
    try:
        return service.search_teaching_modes(search_term, skip=skip, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
