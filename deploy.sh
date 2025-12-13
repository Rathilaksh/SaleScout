#!/bin/bash

# SaleScout Production Deployment Script

echo "🚀 Deploying SaleScout to Production..."

# Check environment
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create it from .env.example"
    exit 1
fi

# Build and start services
echo "📦 Building and starting services..."
docker-compose -f docker-compose.yml up -d --build

# Wait for database
echo "⏳ Waiting for database..."
sleep 15

# Run migrations (if needed)
echo "🔄 Initializing database..."
docker-compose exec backend python -c "from database import init_db; init_db()"

echo "✅ SaleScout deployed successfully!"
echo ""
echo "📝 Access the application at your configured domain"
echo "🔍 View logs: docker-compose logs -f"
echo "🛑 Stop services: docker-compose down"
