"""
Router package initialization.
"""
from .users import router as users_router
from .trackers import router as trackers_router
from .price_history import router as price_history_router

__all__ = [
	"users_router",
	"trackers_router",
	"price_history_router",
]
