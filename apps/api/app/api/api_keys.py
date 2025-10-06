"""
API keys API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict

from app.api.deps import get_db
from app.services.api_key_service import (
    save_api_key,
    get_all_api_keys,
    delete_api_key
)

router = APIRouter(prefix="/api/settings/api-keys", tags=["api-keys"])

class APIKeyCreate(BaseModel):
    provider: str
    key: str

@router.get("/")
async def get_api_keys(db: Session = Depends(get_db)) -> Dict[str, str]:
    """Get all API keys (for frontend display)"""
    try:
        return get_all_api_keys(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get API keys: {str(e)}")

@router.post("/")
async def create_or_update_api_key(body: APIKeyCreate, db: Session = Depends(get_db)):
    """Create or update an API key"""
    valid_providers = ['anthropic', 'openai', 'google', 'qwen']
    if body.provider not in valid_providers:
        raise HTTPException(status_code=400, detail="Invalid provider")
    
    if not body.key or not body.key.strip():
        raise HTTPException(status_code=400, detail="API key cannot be empty")
    
    try:
        save_api_key(db, body.provider, body.key.strip())
        return {"message": "API key saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save API key: {str(e)}")

@router.delete("/{provider}")
async def delete_api_key_endpoint(provider: str, db: Session = Depends(get_db)):
    """Delete an API key"""
    valid_providers = ['anthropic', 'openai', 'google', 'qwen']
    if provider not in valid_providers:
        raise HTTPException(status_code=400, detail="Invalid provider")
    
    try:
        success = delete_api_key(db, provider)
        if not success:
            raise HTTPException(status_code=404, detail="API key not found")
        return {"message": "API key deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete API key: {str(e)}")
