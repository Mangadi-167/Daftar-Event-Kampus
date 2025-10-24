from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

ADMIN_API_KEY = "admin-secret-key-12345"

def get_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key == ADMIN_API_KEY:
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing Admin API Key"
        )