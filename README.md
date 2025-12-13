# SaleScout – Product Price Monitoring & Alert System

Track Amazon and Flipkart product prices, view history, and get alerts when prices drop below your target.

## Features
- JWT auth: register, login, protected routes
- Trackers: create, list, update, delete; auto-fetch title/image via scraper
- Price history: view chart and table for each tracker
- Scrapers: Amazon + Flipkart with resilient selectors
- Background jobs: Celery worker + beat scheduler
- Alerts: Email when target reached or price drops ≥5% vs yesterday
- Frontend: React (Vite), TailwindCSS, Recharts
- Backend: FastAPI, SQLAlchemy, PostgreSQL
- Infra: Docker Compose with Postgres, Redis, Backend, Worker, Scheduler, Frontend

## Tech Stack
- **Frontend:** React (Vite), TailwindCSS, Axios, React Router, Recharts
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **Tasks:** Celery + Redis
- **Scraping:** Requests + BeautifulSoup4 (Playwright fallback stub for Amazon)
- **Auth:** JWT (python-jose, passlib)

## Getting Started (Local without Docker)
1) Prereqs: Python 3.11+, Node 18+, PostgreSQL, Redis
2) Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env   # then edit values
python -c "from database import init_db; init_db()"
uvicorn main:app --reload --port 8000
```
3) Frontend
```bash
cd frontend
npm install
npm run dev -- --host --port 5173
```
App: http://localhost:5173 (proxy to http://localhost:8000)
API docs: http://localhost:8000/docs

## Getting Started (Docker Compose)
```bash
./start-dev.sh
# or manually
# docker-compose up -d
```
Services:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

Stop: `docker-compose down`
Logs: `docker-compose logs -f`

## Environment Variables (.env)
See `.env.example` for all settings. Key values:
- `DATABASE_URL=postgresql://salescout_user:salescout_pass@db:5432/salescout_db`
- `SECRET_KEY` (set a strong value)
- `CELERY_BROKER_URL=redis://redis:6379/0`
- `CELERY_RESULT_BACKEND=redis://redis:6379/0`
- `SMTP_*` for email alerts
- `FRONTEND_URL=http://localhost:5173`

## API Overview
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `DELETE /auth/me`
- `GET /trackers`
- `POST /trackers`
- `GET /trackers/{id}`
- `PUT /trackers/{id}`
- `DELETE /trackers/{id}`
- `GET /trackers/{id}/history`

Auth header: `Authorization: Bearer <token>`

## Scraping
- Amazon: requests + BS4 with multiple selectors; Playwright fallback stub available
- Flipkart: requests + BS4 with multiple selectors
- If price not found, Celery retries (task retry)

## Background Jobs
- Celery worker: `celery -A tasks.check_price worker`
- Celery beat: `celery -A tasks.check_price beat`
- Scheduler enqueues due trackers every 5 minutes (configurable in `tasks/celeryconfig.py`)
- `check_price` task: scrape price, save history, update tracker, send alerts (target price or ≥5% drop vs yesterday)

## Frontend Notes
- AuthContext manages JWT in `localStorage`
- Axios interceptor injects `Authorization` header and handles 401 redirects
- Dashboard shows trackers; AddTrackerModal creates trackers; TrackerDetail shows Recharts line chart for history

## Deployment
- Use `deploy.sh` for a compose-based deployment build
- Ensure strong `SECRET_KEY`, correct `SMTP_*`, and production-ready env values
- Consider HTTPS termination in front (e.g., nginx/traefik) and persistent volumes for Postgres

## Testing Quick Checks
- Backend health: `curl http://localhost:8000/health`
- API docs: `http://localhost:8000/docs`
- Frontend load: `http://localhost:5173`

## Notes
- Replace placeholder secrets in `.env` before production
- Playwright is optional; install browser deps if enabling full JS rendering
