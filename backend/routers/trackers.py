"""
Tracker routes for managing product price tracking.
"""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Tracker, PriceHistory, User
from schemas import (
    TrackerCreate,
    TrackerUpdate,
    TrackerResponse,
    TrackerDetailResponse,
    PriceHistoryResponse,
)
from auth import get_current_user

router = APIRouter(prefix="/trackers", tags=["Trackers"])


@router.get("", response_model=List[TrackerResponse])
def list_trackers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all trackers for the current user."""
    trackers = db.query(Tracker).filter(Tracker.user_id == current_user.id).all()
    return [TrackerResponse.model_validate(t) for t in trackers]


@router.post("", response_model=TrackerResponse, status_code=status.HTTP_201_CREATED)
def create_tracker(
    tracker_data: TrackerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new tracker for a product URL.
    Title and image extraction will be filled by scraper tasks.
    """
    # Placeholder title until scraper fills details
    placeholder_title = "Pending title fetch"
    new_tracker = Tracker(
        user_id=current_user.id,
        product_url=tracker_data.product_url,
        product_title=placeholder_title,
        image_url=None,
        target_price=tracker_data.target_price,
        polling_interval_minutes=tracker_data.polling_interval_minutes,
        active=True,
        last_price=None,
        last_checked_at=None,
    )
    db.add(new_tracker)
    db.commit()
    db.refresh(new_tracker)
    return TrackerResponse.model_validate(new_tracker)


@router.get("/{tracker_id}", response_model=TrackerDetailResponse)
def get_tracker(
    tracker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get tracker details including price history.
    """
    tracker = db.query(Tracker).filter(
        Tracker.id == tracker_id,
        Tracker.user_id == current_user.id
    ).first()
    if not tracker:
        raise HTTPException(status_code=404, detail="Tracker not found")

    # Load price history ordered by newest first
    history = (
        db.query(PriceHistory)
        .filter(PriceHistory.tracker_id == tracker.id)
        .order_by(PriceHistory.checked_at.desc())
        .all()
    )

    tracker.price_history = history  # attach for response
    return TrackerDetailResponse.model_validate(tracker)


@router.put("/{tracker_id}", response_model=TrackerResponse)
def update_tracker(
    tracker_id: int,
    tracker_data: TrackerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update tracker settings (target price, polling interval, active state).
    """
    tracker = db.query(Tracker).filter(
        Tracker.id == tracker_id,
        Tracker.user_id == current_user.id
    ).first()
    if not tracker:
        raise HTTPException(status_code=404, detail="Tracker not found")

    if tracker_data.target_price is not None:
        tracker.target_price = tracker_data.target_price
    if tracker_data.polling_interval_minutes is not None:
        tracker.polling_interval_minutes = tracker_data.polling_interval_minutes
    if tracker_data.active is not None:
        tracker.active = tracker_data.active

    tracker.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(tracker)
    return TrackerResponse.model_validate(tracker)


@router.delete("/{tracker_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tracker(
    tracker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a tracker and its price history.
    """
    tracker = db.query(Tracker).filter(
        Tracker.id == tracker_id,
        Tracker.user_id == current_user.id
    ).first()
    if not tracker:
        raise HTTPException(status_code=404, detail="Tracker not found")

    db.delete(tracker)
    db.commit()
    return None
