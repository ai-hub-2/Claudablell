"""
AI Key Manager - Centralized service for getting API keys from database
"""
import os
from sqlalchemy.orm import Session
from app.services.api_key_service import get_api_key

def get_ai_api_key(db: Session, provider: str) -> str | None:
    """
    Get API key for AI provider from database or environment variables
    Priority: Database > Environment Variables
    """
    # First try to get from database
    db_key = get_api_key(db, provider)
    if db_key:
        return db_key
    
    # Fallback to environment variables
    env_key_map = {
        'anthropic': 'ANTHROPIC_API_KEY',
        'openai': 'OPENAI_API_KEY', 
        'google': 'GOOGLE_API_KEY',
        'qwen': 'QWEN_API_KEY'
    }
    
    env_var = env_key_map.get(provider)
    if env_var:
        return os.getenv(env_var)
    
    return None

def get_anthropic_key(db: Session) -> str | None:
    """Get Anthropic API key"""
    return get_ai_api_key(db, 'anthropic')

def get_openai_key(db: Session) -> str | None:
    """Get OpenAI API key"""
    return get_ai_api_key(db, 'openai')

def get_google_key(db: Session) -> str | None:
    """Get Google API key"""
    return get_ai_api_key(db, 'google')

def get_qwen_key(db: Session) -> str | None:
    """Get Qwen API key"""
    return get_ai_api_key(db, 'qwen')

