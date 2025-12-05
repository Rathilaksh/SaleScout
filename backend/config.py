"""
Configuration management for SaleScout backend.
Loads environment variables and provides config to the application.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://salescout_user:salescout_pass@localhost:5432/salescout_db"
)

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Celery Configuration
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Email Configuration (SMTP)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "your-email@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your-app-password")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "noreply@salescout.com")

# Application Configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Scraper Configuration
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3

# Price Alert Threshold (percentage)
PRICE_DROP_ALERT_THRESHOLD = 5  # Alert if price drops by 5% or more
