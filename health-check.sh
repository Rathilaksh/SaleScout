#!/bin/bash

echo "🧪 Running SaleScout Health Checks..."

# Check if services are running
echo -e "\n1️⃣ Checking if Docker services are running..."
docker-compose ps

# Backend health check
echo -e "\n2️⃣ Testing Backend Health..."
curl -s http://localhost:8000/health | jq . || echo "Backend not responding"

# Frontend check
echo -e "\n3️⃣ Testing Frontend..."
curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 && echo " - Frontend OK" || echo " - Frontend not responding"

# Database connection
echo -e "\n4️⃣ Checking Database..."
docker-compose exec -T db pg_isready -U salescout_user && echo "Database OK" || echo "Database not ready"

# Redis check
echo -e "\n5️⃣ Checking Redis..."
docker-compose exec -T redis redis-cli ping && echo "Redis OK" || echo "Redis not ready"

# Celery worker check
echo -e "\n6️⃣ Checking Celery Worker..."
docker-compose logs --tail=10 worker | grep -q "ready" && echo "Worker OK" || echo "Check worker logs"

# Celery beat check
echo -e "\n7️⃣ Checking Celery Beat..."
docker-compose logs --tail=10 scheduler | grep -q "beat" && echo "Scheduler OK" || echo "Check scheduler logs"

echo -e "\n✅ Health check complete!"
