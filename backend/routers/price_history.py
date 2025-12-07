"""
Routes for price history retrieval.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Tracker, PriceHistory, User
from schemas import PriceHistoryResponse
from auth import get_current_user

router = APIRouter(prefix="/trackers", tags=["Price History"])


@router.get("/{tracker_id}/history", response_model=List[PriceHistoryResponse])
def get_price_history(
    tracker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get price history entries for a tracker owned by the current user.
    """
    tracker = db.query(Tracker).filter(
        Tracker.id == tracker_id,
        Tracker.user_id == current_user.id
    ).first()
    if not tracker:
        raise HTTPException(status_code=404, detail="Tracker not found")

    history = (
        db.query(PriceHistory)
        .filter(PriceHistory.tracker_id == tracker.id)
        .order_by(PriceHistory.checked_at.desc())
        .all()
    )
    return [PriceHistoryResponse.model_validate(h) for h in history]
