# 🛒 SaleScout – Product Price Monitoring & Alert System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![✨ Features

- 🔐 **JWT Authentication** - Register, login, protected routes
- 📊 **Product Tracking** - Create, list, update, delete trackers with auto-fetch title/image
- 📈 **Price History** - Interactive charts showing price trends over time
- 🕷️ **Smart Scraping** - Amazon + Flipkart with resilient selectors and retry logic
- ⚙️ **Background Jobs** - Celery worker + beat scheduler for automated price checks
- 📧 **Email Alerts** - Notifications when target price reached or ≥5% drop vs yesterday
- 🎨 **Modern UI** - React (Vite), TailwindCSS, Recharts
- 🚀 **Production Ready** - FastAPI, SQLAlchemy, PostgreSQL
- 🐳 **Docker Compose** - One-command setup with all services
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
🐳 Getting Started (Docker Compose - Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Rathilaksh/SaleScout.git
cd SaleScout

# 2. Configure environment
cp .env.example .env
# Edit .env with your settings (SMTP, SECRET_KEY, etc.)

# 3. Start all services
./start-dev.sh
# or manually: docker-compose up -d
```

**Services will be available at:**
- 🌐 Frontend: http://localhost:5173
- ⚡ Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs
- 🗄️ PostgreSQL: localhost:5432
- 🔴 Redis: localhost:6379

**Useful Commands:**
```bash
docker-compose logs -f              # View logs
docker-compose logs -f backend      # View backend logs only
docker-compose down                 # Stop all services
docker-compose down -v              # Stop and remove volumes
./health-check.sh                   # Run health checks
``
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

## 🧪 Testing & Troubleshooting

### Quick Health Checks
```bash
./health-check.sh                           # Run automated health checks
curl http://localhost:8000/health           # Backend health
curl http://localhost:8000/docs             # API documentation
curl http://localhost:5173                  # Frontend
```

### Common Issues

**Backend won't start:**
```bash
docker-compose logs backend
# Check DATABASE_URL and ensure PostgreSQL is ready
```

**Celery worker not processing tasks:**
```bash
docker-compose logs worker
# Verify CELERY_BROKER_URL points to Redis
```

**Frontend can't reach backend:**
- Check that backend is running on port 8000
- Verify Vite proxy configuration in `frontend/vite.config.js`
- Check CORS settings in `backend/main.py`

**Email notifications not working:**
- Verify SMTP credentials in `.env`
- For Gmail: Use App Password, not regular password
- Check `docker-compose logs worker` for SMTP errors

**Scraping returns no data:**
- Amazon/Flipkart may change selectors; update `backend/scraper/*.py`
- Check for rate limiting or blocked requests
- Consider adding delays between requests

## 📝 Important Notes

- ⚠️ **Security**: Replace placeholder secrets in `.env` before production deployment
- 🔑 **SMTP Setup**: For Gmail, enable 2FA and create an App Password
- 🌐 **Playwright**: Optional; install browser deps if enabling full JS rendering for dynamic pages
- 📊 **Price Checking**: Default interval is 60 minutes; adjust per tracker or globally in Celery config
- 💾 **Data Persistence**: Docker volumes ensure data survives container restarts

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/), [React](https://reactjs.org/), and [Celery](https://docs.celeryq.dev/)
- Scraping powered by [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- Charts by [Recharts](https://recharts.org/)

---

Made with ❤️ for smart shoppers
