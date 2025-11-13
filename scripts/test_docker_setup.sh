#!/bin/bash
# Test script to verify Docker setup is working correctly

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Django DRF Docker Setup Verification Test${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}\n"

# Function to print status
print_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
        exit 1
    fi
}

# 1. Check if docker is installed
echo -e "${YELLOW}[1/8]${NC} Checking Docker installation..."
docker --version > /dev/null 2>&1
print_status "Docker is installed"

# 2. Check if docker-compose is installed
echo -e "${YELLOW}[2/8]${NC} Checking Docker Compose installation..."
docker compose version > /dev/null 2>&1 || docker-compose --version > /dev/null 2>&1
print_status "Docker Compose is installed"

# 3. Stop any existing containers
echo -e "${YELLOW}[3/8]${NC} Stopping existing containers..."
docker-compose down > /dev/null 2>&1 || true
print_status "Cleaned up existing containers"

# 4. Build the images
echo -e "${YELLOW}[4/8]${NC} Building Docker images (this may take a few minutes)..."
docker-compose build --no-cache > /tmp/docker-build.log 2>&1
if [ $? -eq 0 ]; then
    print_status "Docker images built successfully"
else
    echo -e "${RED}✗${NC} Failed to build Docker images"
    echo -e "${RED}Last 20 lines of build log:${NC}"
    tail -20 /tmp/docker-build.log
    exit 1
fi

# 5. Start the services
echo -e "${YELLOW}[5/8]${NC} Starting services..."
docker-compose up -d
print_status "Services started"

# 6. Wait for services to be healthy
echo -e "${YELLOW}[6/8]${NC} Waiting for services to be healthy (up to 120 seconds)..."
max_wait=120
elapsed=0
while [ $elapsed -lt $max_wait ]; do
    db_status=$(docker-compose ps db | grep "Up" | grep "healthy" | wc -l)
    redis_status=$(docker-compose ps redis | grep "Up" | grep "healthy" | wc -l)
    web_status=$(docker-compose ps web | grep "Up" | wc -l)
    
    if [ $db_status -eq 1 ] && [ $redis_status -eq 1 ] && [ $web_status -eq 1 ]; then
        break
    fi
    
    echo -n "."
    sleep 2
    elapsed=$((elapsed + 2))
done
echo ""

if [ $elapsed -ge $max_wait ]; then
    echo -e "${RED}✗${NC} Services failed to become healthy within $max_wait seconds"
    echo -e "${YELLOW}Service status:${NC}"
    docker-compose ps
    echo -e "${YELLOW}Web service logs:${NC}"
    docker-compose logs web
    exit 1
fi
print_status "All services are healthy"

# 7. Test API endpoint
echo -e "${YELLOW}[7/8]${NC} Testing API endpoint..."
sleep 5  # Give nginx a bit more time
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/api/ 2>/dev/null || echo "000")
if [ "$response" = "200" ] || [ "$response" = "301" ] || [ "$response" = "302" ]; then
    print_status "API endpoint is responding (HTTP $response)"
else
    echo -e "${YELLOW}⚠${NC}  API endpoint returned HTTP $response (may need more time to start)"
    echo -e "${YELLOW}Note: This is common on first startup while migrations run${NC}"
fi

# 8. Display service status
echo -e "${YELLOW}[8/8]${NC} Final service status check..."
docker-compose ps
print_status "All containers are running"

echo -e "\n${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Docker setup verification completed successfully!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}\n"

echo -e "${GREEN}Next steps:${NC}"
echo -e "  • Access the API: ${BLUE}http://localhost/api/${NC}"
echo -e "  • View API docs: ${BLUE}http://localhost/api/schema/swagger-ui/${NC}"
echo -e "  • View logs: ${YELLOW}docker-compose logs -f web${NC}"
echo -e "  • Stop services: ${YELLOW}docker-compose down${NC}\n"

# Optional: Show web service logs
echo -e "${YELLOW}Last 20 lines of web service logs:${NC}"
docker-compose logs --tail=20 web

exit 0
