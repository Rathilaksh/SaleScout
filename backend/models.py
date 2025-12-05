"""
SQLAlchemy ORM models for SaleScout.
Defines User, Tracker, and PriceHistory tables.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """
    User model - stores authentication and user profile data.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship: one user can have many trackers
    trackers = relationship("Tracker", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Tracker(Base):
    """
    Tracker model - stores product tracking information.
    """
    __tablename__ = "trackers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Product information
    product_url = Column(String(500), nullable=False)
    product_title = Column(String(500), nullable=False)
    image_url = Column(String(500), nullable=True)
    
    # Price tracking
    target_price = Column(Float, nullable=False)
    last_price = Column(Float, nullable=True)
    last_checked_at = Column(DateTime, nullable=True)
    
    # Configuration
    polling_interval_minutes = Column(Integer, default=60, nullable=False)
    active = Column(Boolean, default=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="trackers")
    price_history = relationship("PriceHistory", back_populates="tracker", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tracker(id={self.id}, product_title={self.product_title}, last_price={self.last_price})>"


class PriceHistory(Base):
    """
    PriceHistory model - stores historical price data for each tracker.
    """
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    tracker_id = Column(Integer, ForeignKey("trackers.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Price data
    price = Column(Float, nullable=False)
    checked_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationship
    tracker = relationship("Tracker", back_populates="price_history")

    def __repr__(self):
        return f"<PriceHistory(id={self.id}, tracker_id={self.tracker_id}, price={self.price})>"
