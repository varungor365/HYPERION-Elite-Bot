#!/bin/bash

# 🚀 Simple Docker Run - HYPERION Elite Bot 24/7
# Quick single-command deployment

echo "🚀 HYPERION Elite Bot - Simple Docker 24/7 Deployment"
echo "====================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running! Please start Docker first."
    exit 1
fi

# Stop existing container if running
echo "🛑 Stopping existing container (if any)..."
docker stop hyperion-elite-bot-simple 2>/dev/null || true
docker rm hyperion-elite-bot-simple 2>/dev/null || true

# Build the image
echo "🏗️  Building Docker image..."
docker build -f Dockerfile.production -t hyperion-elite-bot:latest .

# Run container with 24/7 settings
echo "🚀 Starting bot container 24/7..."
docker run -d \
  --name hyperion-elite-bot-simple \
  --restart always \
  --memory=1g \
  --cpus="1.0" \
  --health-cmd="python3 -c \"import requests; requests.get('https://api.telegram.org/bot7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM/getMe', timeout=10)\"" \
  --health-interval=60s \
  --health-timeout=15s \
  --health-retries=5 \
  --health-start-period=30s \
  -v hyperion-hits:/app/hits \
  -v hyperion-logs:/app/logs \
  -v hyperion-temp:/app/temp \
  -e PYTHONUNBUFFERED=1 \
  -e TZ=UTC \
  hyperion-elite-bot:latest

# Wait for container to start
echo "⏳ Waiting for container to start..."
sleep 10

# Check status
echo "📊 Container Status:"
docker ps --filter name=hyperion-elite-bot-simple

# Show logs
echo "📋 Startup Logs:"
docker logs --tail=15 hyperion-elite-bot-simple

# Check if container is running
if docker ps --filter name=hyperion-elite-bot-simple --filter status=running | grep -q hyperion-elite-bot-simple; then
    echo ""
    echo "🎉 SUCCESS! HYPERION Elite Bot is running 24/7!"
    echo ""
    echo "🛠️ Management Commands:"
    echo "  • View logs: docker logs -f hyperion-elite-bot-simple"
    echo "  • Stop bot: docker stop hyperion-elite-bot-simple"
    echo "  • Start bot: docker start hyperion-elite-bot-simple"
    echo "  • Restart: docker restart hyperion-elite-bot-simple"
    echo "  • Status: docker ps --filter name=hyperion-elite-bot-simple"
    echo ""
    echo "📱 Telegram: @megacheckk_bot"
    echo "🔑 Send /start to activate!"
else
    echo ""
    echo "❌ Container failed to start! Check logs:"
    docker logs hyperion-elite-bot-simple
fi