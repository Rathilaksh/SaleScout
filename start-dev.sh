#!/bin/bash

# SaleScout Development Setup Script

echo "🚀 Starting SaleScout Development Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please edit it with your configuration."
fi

# Start services
echo "📦 Starting Docker containers..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 10

echo "✅ SaleScout is running!"
echo ""
echo "📝 Access the application:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🔍 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
