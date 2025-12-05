"""
Initialization file for models and database.
This ensures all models are registered with SQLAlchemy.
"""
from database import Base
from models import User, Tracker, PriceHistory

__all__ = ["Base", "User", "Tracker", "PriceHistory"]
