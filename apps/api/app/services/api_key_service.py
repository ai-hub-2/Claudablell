"""
API key service for managing AI provider API keys
"""
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.api_keys import APIKey
from app.core.crypto import secret_box

def save_api_key(db: Session, provider: str, key: str) -> APIKey:
    """Save or update an API key for a provider"""
    # Check if key already exists for this provider
    existing_key = db.query(APIKey).filter(APIKey.provider == provider).first()
    
    if existing_key:
        # Update existing key
        existing_key.key = secret_box.encrypt(key)
        existing_key.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_key)
        return existing_key
    else:
        # Create new key
        api_key = APIKey(
            id=str(uuid.uuid4()),
            provider=provider,
            key=secret_box.encrypt(key)
        )
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
        return api_key

def get_api_key(db: Session, provider: str) -> str | None:
    """Get decrypted API key for a provider"""
    api_key = db.query(APIKey).filter(APIKey.provider == provider).first()
    if api_key:
        return secret_box.decrypt(api_key.key)
    return None

def get_all_api_keys(db: Session) -> dict[str, str]:
    """Get all API keys as a dictionary"""
    try:
        api_keys = db.query(APIKey).all()
        result = {}
        for key in api_keys:
            try:
                result[key.provider] = secret_box.decrypt(key.key)
            except Exception as e:
                print(f"Failed to decrypt key for provider {key.provider}: {e}")
                # Try to delete the corrupted key
                try:
                    db.delete(key)
                    db.commit()
                    print(f"Deleted corrupted key for provider {key.provider}")
                except Exception as delete_error:
                    print(f"Failed to delete corrupted key: {delete_error}")
                continue
        return result
    except Exception as e:
        print(f"Error in get_all_api_keys: {e}")
        return {}

def delete_api_key(db: Session, provider: str) -> bool:
    """Delete API key for a provider"""
    api_key = db.query(APIKey).filter(APIKey.provider == provider).first()
    if api_key:
        db.delete(api_key)
        db.commit()
        return True
    return False

def update_last_used(db: Session, provider: str) -> None:
    """Update last used timestamp for an API key"""
    api_key = db.query(APIKey).filter(APIKey.provider == provider).first()
    if api_key:
        api_key.last_used = datetime.utcnow()
        db.commit()
