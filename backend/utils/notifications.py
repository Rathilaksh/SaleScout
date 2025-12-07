"""
Email notification utilities for SaleScout.
"""
import aiosmtplib
from email.message import EmailMessage

from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SMTP_FROM_EMAIL
from utils import format_price


async def _send_email_async(msg: EmailMessage):
    await aiosmtplib.send(
        msg,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASSWORD,
        start_tls=True,
    )


def send_email_notification(
    user_email: str,
    product_title: str,
    old_price: float | None,
    new_price: float,
    url: str,
    reason: str,
):
    """
    Send an email notification to the user about price change/alert.
    Synchronously dispatches an async SMTP send.
    """
    subject = f"SaleScout Alert: {reason}"
    body_lines = [
        f"Product: {product_title}",
        f"Current Price: {format_price(new_price)}",
    ]
    if old_price is not None:
        body_lines.append(f"Previous Price: {format_price(old_price)}")
    body_lines.append(f"Link: {url}")
    body_lines.append("\nYou are receiving this because you set a tracker in SaleScout.")

    msg = EmailMessage()
    msg["From"] = SMTP_FROM_EMAIL
    msg["To"] = user_email
    msg["Subject"] = subject
    msg.set_content("\n".join(body_lines))

    # Run async send in a simple loop to avoid event loop issues in Celery workers
    try:
        import asyncio

        asyncio.run(_send_email_async(msg))
    except Exception as exc:  # noqa: BLE001
        # Log or print failure; in real deployment, hook into logging/monitoring
        print(f"Email send failed: {exc}")
