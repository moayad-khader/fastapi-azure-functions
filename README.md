# Azure Functions FastAPI Microservices Boilerplate

A comprehensive boilerplate for building microservices using Azure Functions and FastAPI with Docker Compose support.

## 🏗️ Architecture

This project consists of three microservices:

- **Auth Service** (Port 8001) - Authentication and authorization
- **Organization Service** (Port 8002) - Organization management
- **AI Agent Service** (Port 8003) - AI-powered agent functionality

## 🚀 Quick Start with Docker Compose

### Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)

### Running the Services

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd azure_functions_fastapi_microservices_boilerplate
   ```

2. **Build and start all services**:
   ```bash
   docker-compose up --build
   ```

3. **Start services in detached mode**:
   ```bash
   docker-compose up -d --build
   ```

4. **View logs**:
   ```bash
   # All services
   docker-compose logs -f
   
   # Specific service
   docker-compose logs -f auth-service
   ```

5. **Stop services**:
   ```bash
   docker-compose down
   ```

### Service Endpoints

#### Direct Service Access:
- **Auth Service**: http://localhost:8001
  - Health: http://localhost:8001/health
  - Docs: http://localhost:8001/docs
  
- **Organization Service**: http://localhost:8002
  - Health: http://localhost:8002/health
  - Docs: http://localhost:8002/docs
  
- **AI Agent Service**: http://localhost:8003
  - Health: http://localhost:8003/health
  - Docs: http://localhost:8003/docs

#### Via Nginx Reverse Proxy:
- **Gateway**: http://localhost
  - Auth Service: http://localhost/auth/
  - Organization Service: http://localhost/organization/
  - AI Agent Service: http://localhost/ai-agent/
  - Overall Health: http://localhost/health

## 🛠️ Development

### Local Development with Docker Compose

The Docker Compose setup includes volume mounts for hot reloading during development:

```bash
# Start in development mode
docker-compose up --build

# Make changes to your code - the services will automatically reload
```

### Individual Service Development

You can also run individual services:

```bash
# Build and run only auth service
docker-compose up --build auth-service

# Run specific services
docker-compose up auth-service organization-service
```

### Environment Variables

Create `.env` files for each service to customize configuration:

```bash
# services/auth-service/.env
DEBUG=true
LOG_LEVEL=debug

# services/organization-service/.env
DEBUG=true
COSMOS_DB_ENDPOINT=your-cosmos-endpoint

# services/ai-agent-service/.env
DEBUG=true
SERVICE_BUS_CONNECTION=your-service-bus-connection
```

## 📦 Docker Commands

### Useful Docker Compose Commands

```bash
# Build without cache
docker-compose build --no-cache

# View running containers
docker-compose ps

# Execute commands in running containers
docker-compose exec auth-service bash

# View resource usage
docker-compose top

# Remove all containers and networks
docker-compose down --remove-orphans

# Remove containers, networks, and volumes
docker-compose down -v
```

### Individual Docker Commands

```bash
# Build individual service
docker build -t auth-service ./services/auth-service

# Run individual container
docker run -p 8001:8000 auth-service
```

## 🔧 Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure ports 8001, 8002, 8003, and 80 are available
2. **Build failures**: Try `docker-compose build --no-cache`
3. **Permission issues**: Ensure Docker has proper permissions

### Health Checks

All services include health checks. Monitor service health:

```bash
# Check health status
docker-compose ps

# View health check logs
docker-compose logs nginx
```

### Debugging

```bash
# Access service logs
docker-compose logs -f [service-name]

# Access service shell
docker-compose exec [service-name] bash

# Inspect service configuration
docker-compose config
```

## 🚀 Production Deployment

For production deployment, consider:

1. **Environment-specific configurations**
2. **Secrets management**
3. **Load balancing**
4. **Monitoring and logging**
5. **Security hardening**

## 📝 API Documentation

Each service provides interactive API documentation via FastAPI's automatic docs:

- Auth Service: http://localhost:8001/docs
- Organization Service: http://localhost:8002/docs  
- AI Agent Service: http://localhost:8003/docs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker Compose
5. Submit a pull request
