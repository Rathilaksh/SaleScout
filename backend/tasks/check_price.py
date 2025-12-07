"""
Celery tasks for price checking and scheduling.
"""
from datetime import datetime, timedelta
from typing import Optional

from celery import Celery
from sqlalchemy.orm import Session

from config import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
    PRICE_DROP_ALERT_THRESHOLD,
)
from database import SessionLocal
from models import Tracker, PriceHistory, User
from scraper import scrape_amazon, scrape_flipkart
from utils import (
    get_platform_from_url,
    calculate_price_change_percentage,
    format_price,
)
from utils.notifications import send_email_notification

celery_app = Celery(
    "salescout",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)
celery_app.config_from_object("tasks.celeryconfig")


def _get_db_session() -> Session:
    return SessionLocal()


def _scrape_price(tracker: Tracker) -> Optional[float]:
    platform = get_platform_from_url(tracker.product_url)
    if platform == "amazon":
        data = scrape_amazon(tracker.product_url)
    elif platform == "flipkart":
        data = scrape_flipkart(tracker.product_url)
    else:
        return None
    # Update title/image if available
    if data.get("title"):
        tracker.product_title = data["title"]
    if data.get("image_url"):
        tracker.image_url = data["image_url"]
    return data.get("price")


@celery_app.task(name="tasks.check_price.check_price", bind=True, max_retries=3, default_retry_delay=120)
def check_price(self, tracker_id: int):
    """
    Check price for a tracker, store history, update tracker, and send alerts.
    """
    db = _get_db_session()
    try:
        tracker = db.query(Tracker).filter(Tracker.id == tracker_id, Tracker.active == True).first()  # noqa: E712
        if not tracker:
            return "Tracker not found or inactive"

        old_price = tracker.last_price
        price = _scrape_price(tracker)

        if price is None:
            # Retry if price could not be fetched
            raise self.retry(exc=Exception("Price not found"))

        # Save price history
        history = PriceHistory(
            tracker_id=tracker.id,
            price=price,
            checked_at=datetime.utcnow(),
        )
        db.add(history)

        # Update tracker
        tracker.last_price = price
        tracker.last_checked_at = datetime.utcnow()
        db.commit()
        db.refresh(tracker)

        # Send notifications
        user = db.query(User).filter(User.id == tracker.user_id).first()
        if user:
            # Target price alert
            if price <= tracker.target_price:
                send_email_notification(
                    user_email=user.email,
                    product_title=tracker.product_title,
                    old_price=old_price,
                    new_price=price,
                    url=tracker.product_url,
                    reason="Target price reached",
                )

            # Price drop alert (>= threshold vs yesterday)
            yesterday = datetime.utcnow() - timedelta(days=1)
            prev_entry = (
                db.query(PriceHistory)
                .filter(
                    PriceHistory.tracker_id == tracker.id,
                    PriceHistory.checked_at <= yesterday,
                )
                .order_by(PriceHistory.checked_at.desc())
                .first()
            )
            if prev_entry:
                drop_pct = calculate_price_change_percentage(prev_entry.price, price)
                if drop_pct <= -PRICE_DROP_ALERT_THRESHOLD:
                    send_email_notification(
                        user_email=user.email,
                        product_title=tracker.product_title,
                        old_price=prev_entry.price,
                        new_price=price,
                        url=tracker.product_url,
                        reason=f"Price dropped {abs(drop_pct)}% since yesterday",
                    )

        return "Price checked"
    finally:
        db.close()


@celery_app.task(name="tasks.check_price.enqueue_due_trackers")
def enqueue_due_trackers():
    """
    Periodic task to enqueue price checks for trackers whose interval has elapsed.
    Runs every 5 minutes via Celery beat.
    """
    db = _get_db_session()
    try:
        now = datetime.utcnow()
        trackers = db.query(Tracker).filter(Tracker.active == True).all()  # noqa: E712
        queued = 0
        for tracker in trackers:
            if not tracker.last_checked_at:
                check_price.delay(tracker.id)
                queued += 1
                continue
            elapsed = now - tracker.last_checked_at
            if elapsed >= timedelta(minutes=tracker.polling_interval_minutes):
                check_price.delay(tracker.id)
                queued += 1
        return f"Enqueued {queued} tracker checks"
    finally:
        db.close()
