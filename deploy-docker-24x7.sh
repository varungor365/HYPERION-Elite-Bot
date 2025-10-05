#!/bin/bash

# 🚀 HYPERION Elite Bot - 24/7 Docker Deployment Script
# This script sets up the bot to run 24/7 in Docker

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_header() { echo -e "${BLUE}$1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }

echo -e "${BLUE}"
cat << "EOF"
████████████████████████████████████████████████████████████████
█                                                              █
█    🚀 HYPERION ELITE BOT - 24/7 DOCKER DEPLOYMENT 🚀       █
█                                                              █
█         Production Ready • Auto-Restart • Monitoring        █
█                                                              █
████████████████████████████████████████████████████████████████
EOF
echo -e "${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed!"
    print_header "📦 Installing Docker..."
    
    # Install Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    
    print_success "Docker installed! Please logout and login again, then re-run this script."
    exit 0
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null 2>&1; then
    print_error "Docker Compose is not installed!"
    print_header "📦 Installing Docker Compose..."
    
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    
    print_success "Docker Compose installed!"
fi

print_success "Docker and Docker Compose are ready!"

# Create production Docker Compose file
print_header "📝 Creating 24/7 Docker Configuration..."

cat > docker-compose.24x7.yml << 'EOF'
version: '3.8'

services:
  hyperion-bot:
    build:
      context: .
      dockerfile: Dockerfile.production
    container_name: hyperion-elite-bot-24x7
    restart: always
    
    environment:
      - PYTHONUNBUFFERED=1
      - PYTHONDONTWRITEBYTECODE=1
      - TZ=UTC
    
    volumes:
      - hyperion-hits:/app/hits
      - hyperion-logs:/app/logs
      - hyperion-temp:/app/temp
    
    networks:
      - hyperion-network
    
    # Resource limits for stable operation
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 256M
    
    # Health check every minute
    healthcheck:
      test: ["CMD", "python3", "-c", "import requests; requests.get('https://api.telegram.org/bot7090420579:AAEmOwaErySWXdgT7jyXybYmjbOMKFOy3pM/getMe', timeout=10)"]
      interval: 60s
      timeout: 15s
      retries: 5
      start_period: 30s
    
    # Log rotation for 24/7 operation
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Auto-updater for maintenance
  watchtower:
    image: containrrr/watchtower
    container_name: hyperion-watchtower
    restart: unless-stopped
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=3600
    networks:
      - hyperion-network

volumes:
  hyperion-hits:
  hyperion-logs:
  hyperion-temp:

networks:
  hyperion-network:
    driver: bridge
EOF

print_success "Docker configuration created!"

# Build and start the containers
print_header "🏗️  Building Docker Image..."
docker-compose -f docker-compose.24x7.yml build --no-cache

print_header "🚀 Starting 24/7 Bot Container..."
docker-compose -f docker-compose.24x7.yml up -d

# Wait a moment for containers to start
sleep 10

# Check status
print_header "📊 Checking Container Status..."
docker-compose -f docker-compose.24x7.yml ps

# Show logs
print_header "📋 Bot Startup Logs..."
docker-compose -f docker-compose.24x7.yml logs --tail=20 hyperion-bot

# Create management scripts
print_header "🛠️  Creating Management Scripts..."

cat > docker-start.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting HYPERION Elite Bot 24/7..."
docker-compose -f docker-compose.24x7.yml up -d
docker-compose -f docker-compose.24x7.yml ps
EOF

cat > docker-stop.sh << 'EOF'
#!/bin/bash
echo "⏹️ Stopping HYPERION Elite Bot..."
docker-compose -f docker-compose.24x7.yml down
EOF

cat > docker-restart.sh << 'EOF'
#!/bin/bash
echo "🔄 Restarting HYPERION Elite Bot..."
docker-compose -f docker-compose.24x7.yml restart hyperion-bot
sleep 5
docker-compose -f docker-compose.24x7.yml logs --tail=10 hyperion-bot
EOF

cat > docker-logs.sh << 'EOF'
#!/bin/bash
echo "📋 HYPERION Elite Bot Live Logs (Press Ctrl+C to exit)"
docker-compose -f docker-compose.24x7.yml logs -f hyperion-bot
EOF

cat > docker-status.sh << 'EOF'
#!/bin/bash
echo "📊 HYPERION Elite Bot 24/7 Status"
echo "=================================="
docker-compose -f docker-compose.24x7.yml ps
echo ""
echo "🏥 Health Status:"
docker inspect hyperion-elite-bot-24x7 --format='{{.State.Health.Status}}' 2>/dev/null || echo "N/A"
echo ""
echo "📈 Resource Usage:"
docker stats hyperion-elite-bot-24x7 --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" 2>/dev/null || echo "Container not running"
echo ""
echo "📋 Recent Logs:"
docker-compose -f docker-compose.24x7.yml logs --tail=5 hyperion-bot
EOF

cat > docker-update.sh << 'EOF'
#!/bin/bash
echo "📥 Updating HYPERION Elite Bot..."
git pull origin main
docker-compose -f docker-compose.24x7.yml build --no-cache
docker-compose -f docker-compose.24x7.yml up -d
echo "✅ Update complete!"
EOF

chmod +x docker-*.sh

print_success "Management scripts created!"

# Final status check
sleep 5
CONTAINER_STATUS=$(docker inspect hyperion-elite-bot-24x7 --format='{{.State.Status}}' 2>/dev/null || echo "not found")

if [[ "$CONTAINER_STATUS" == "running" ]]; then
    print_success "🎉 HYPERION Elite Bot is running 24/7!"
else
    print_error "Container failed to start. Checking logs..."
    docker-compose -f docker-compose.24x7.yml logs hyperion-bot
    exit 1
fi

# Success message
echo -e "\n${GREEN}"
cat << "EOF"
████████████████████████████████████████████████████████████████
█                                                              █
█        🎉 24/7 DOCKER DEPLOYMENT SUCCESSFUL! 🎉            █
█                                                              █
████████████████████████████████████████████████████████████████
EOF
echo -e "${NC}\n"

print_success "Bot is running 24/7 in Docker with auto-restart!"

echo -e "\n${BLUE}🛠️ Management Commands:${NC}"
echo "   • Start Bot: ./docker-start.sh"
echo "   • Stop Bot: ./docker-stop.sh"
echo "   • Restart Bot: ./docker-restart.sh"
echo "   • View Logs: ./docker-logs.sh"
echo "   • Check Status: ./docker-status.sh"
echo "   • Update Bot: ./docker-update.sh"

echo -e "\n${BLUE}📱 Telegram Bot: @megacheckk_bot${NC}"
echo -e "${BLUE}🔑 Token: 7090420579:AAEmOwaBr... (pre-configured)${NC}"

echo -e "\n${YELLOW}🔔 24/7 Features Enabled:${NC}"
echo "   • ✅ Auto-restart on failure"
echo "   • ✅ Health monitoring every minute"
echo "   • ✅ Log rotation (max 30MB)"
echo "   • ✅ Resource limits (1GB RAM, 1 CPU)"
echo "   • ✅ Auto-updater (Watchtower)"
echo "   • ✅ Persistent storage volumes"

echo -e "\n${GREEN}🚀 Your bot is now running 24/7! Send /start to @megacheckk_bot${NC}"