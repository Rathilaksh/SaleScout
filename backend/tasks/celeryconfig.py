"""
Celery configuration for SaleScout.
Defines broker, backend, and beat schedule.
"""
from datetime import timedelta
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

# Basic Celery configuration
broker_url = CELERY_BROKER_URL
result_backend = CELERY_RESULT_BACKEND

# Recommended serialization settings
accept_content = ["json"]
task_serializer = "json"
result_serializer = "json"

# Timezone settings
enable_utc = True
timezone = "UTC"

# Beat schedule: every 5 minutes enqueue due trackers
beat_schedule = {
    "enqueue-due-trackers": {
        "task": "tasks.check_price.enqueue_due_trackers",
        "schedule": timedelta(minutes=5),
    },
}
