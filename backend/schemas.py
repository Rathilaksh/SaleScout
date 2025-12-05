"""
Pydantic schemas for request/response validation.
These ensure type safety and automatic API documentation.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# ============================================================================
# User Schemas
# ============================================================================

class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class UserLogin(UserBase):
    """Schema for user login."""
    password: str


class UserResponse(UserBase):
    """Schema for user response (no password)."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Price History Schemas
# ============================================================================

class PriceHistoryBase(BaseModel):
    """Base price history schema."""
    price: float


class PriceHistoryCreate(PriceHistoryBase):
    """Schema for creating price history entry."""
    tracker_id: int


class PriceHistoryResponse(PriceHistoryBase):
    """Schema for price history response."""
    id: int
    tracker_id: int
    checked_at: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Tracker Schemas
# ============================================================================

class TrackerBase(BaseModel):
    """Base tracker schema with common fields."""
    product_url: str
    product_title: str
    image_url: Optional[str] = None
    target_price: float
    polling_interval_minutes: int = Field(default=60, ge=5, le=1440)


class TrackerCreate(BaseModel):
    """Schema for creating a tracker with just the product URL."""
    product_url: str = Field(..., description="Amazon or Flipkart product URL")
    target_price: float = Field(..., gt=0, description="Target price threshold")
    polling_interval_minutes: int = Field(default=60, ge=5, le=1440)


class TrackerUpdate(BaseModel):
    """Schema for updating tracker settings."""
    target_price: Optional[float] = Field(None, gt=0)
    polling_interval_minutes: Optional[int] = Field(None, ge=5, le=1440)
    active: Optional[bool] = None


class TrackerResponse(TrackerBase):
    """Schema for tracker response."""
    id: int
    user_id: int
    last_price: Optional[float]
    last_checked_at: Optional[datetime]
    active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TrackerDetailResponse(TrackerResponse):
    """Extended tracker response with price history."""
    price_history: List[PriceHistoryResponse] = []

    class Config:
        from_attributes = True


# ============================================================================
# Authentication Schemas
# ============================================================================

class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenPayload(BaseModel):
    """Schema for JWT token payload."""
    sub: str  # subject (user email)
    exp: int  # expiration time


# ============================================================================
# Error Response Schemas
# ============================================================================

class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str
    code: Optional[str] = None
