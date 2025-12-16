# SaleScout Backend

## Structure
```
backend/
  main.py              # FastAPI app entry point
  config.py            # Environment configuration
  database.py          # SQLAlchemy setup
  models.py            # Database models
  schemas.py           # Pydantic schemas
  auth.py              # JWT authentication
  routers/             # API route handlers
    users.py           # User auth routes
    trackers.py        # Tracker CRUD routes
    price_history.py   # Price history routes
  scraper/             # Web scraping modules
    amazon_scraper.py
    flipkart_scraper.py
  tasks/               # Celery background tasks
    celeryconfig.py
    check_price.py     # Price checking task
  utils/               # Utility functions
    helpers.py
    notifications.py   # Email notifications
```

## Running Locally
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## API Documentation
Once running, visit: http://localhost:8000/docs
