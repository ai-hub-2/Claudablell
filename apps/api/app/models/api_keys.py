"""
API keys model for storing AI provider API keys
"""
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(String(36), primary_key=True, index=True)
    provider = Column(String(50), nullable=False, index=True)  # anthropic, openai, google, qwen
    key = Column(Text, nullable=False)  # Encrypted API key
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_used = Column(DateTime(timezone=True), nullable=True)
    
    # Unique constraint to prevent multiple keys per provider
    __table_args__ = (
        # UniqueConstraint('provider', name='uq_provider_api_key'),
    )
