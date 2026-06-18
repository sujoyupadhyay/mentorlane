from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os

# Define API key header name
API_KEY_NAME = "X-API-Key"
# Create API key header security scheme
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Get API keys from environment variable (comma-separated)
API_KEYS = os.getenv("API_KEYS", "").split(",") if os.getenv("API_KEYS") else []

# Default API key for development (should be changed in production)
DEFAULT_API_KEY = "mentorlane"

# Add default API key if no API keys are configured
if not API_KEYS:
    API_KEYS.append(DEFAULT_API_KEY)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Validate the API key from the request header.
    
    Args:
        api_key_header: The API key from the X-API-Key header
        
    Returns:
        The validated API key
        
    Raises:
        HTTPException: If the API key is invalid or missing
    """
    if api_key_header in API_KEYS:
        return api_key_header
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
        headers={"WWW-Authenticate": "ApiKey"},
    )


def is_api_key_configured() -> bool:
    """
    Check if API keys are properly configured.
    
    Returns:
        True if API keys are configured (not using default), False otherwise
    """
    return len(API_KEYS) > 1 or (len(API_KEYS) == 1 and API_KEYS[0] != DEFAULT_API_KEY)
