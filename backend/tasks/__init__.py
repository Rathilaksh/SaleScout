"""
Tasks package initialization.
"""
from .check_price import celery_app

__all__ = ["celery_app"]
