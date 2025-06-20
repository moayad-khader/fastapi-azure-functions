.PHONY: help build up down restart logs clean test health

# Default target
help:
	@echo "Available commands:"
	@echo "  build     - Build all Docker images"
	@echo "  up        - Start all services"
	@echo "  down      - Stop all services"
	@echo "  restart   - Restart all services"
	@echo "  logs      - View logs from all services"
	@echo "  clean     - Remove all containers, networks, and volumes"
	@echo "  test      - Run health checks on all services"
	@echo "  health    - Check health status of all services"

# Build all images
build:
	docker-compose build --no-cache

# Start all services
up:
	docker-compose up -d --build

# Stop all services
down:
	docker-compose down

# Restart all services
restart: down up

# View logs
logs:
	docker-compose logs -f

# Clean up everything
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

# Test all services
test:
	@echo "Testing Auth Service..."
	@curl -f http://localhost:8001/health || echo "Auth Service failed"
	@echo "Testing Organization Service..."
	@curl -f http://localhost:8002/health || echo "Organization Service failed"
	@echo "Testing AI Agent Service..."
	@curl -f http://localhost:8003/health || echo "AI Agent Service failed"
	@echo "Testing Nginx Gateway..."
	@curl -f http://localhost/health || echo "Nginx Gateway failed"

# Check health status
health:
	docker-compose ps

# Individual service commands
up-auth:
	docker-compose up -d auth-service

up-org:
	docker-compose up -d organization-service

up-ai:
	docker-compose up -d ai-agent-service

up-nginx:
	docker-compose up -d nginx

# Development commands
dev:
	docker-compose up --build

dev-logs:
	docker-compose logs -f auth-service organization-service ai-agent-service

# Production commands
prod-up:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-down:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
