# Azure Functions FastAPI Microservices Boilerplate

A comprehensive boilerplate for building microservices using Azure Functions and FastAPI with Docker Compose support.

## 🏗️ Architecture

This project consists of two main microservices with shared components:

- **Auth Service** (Port 8001) - Authentication and authorization with API versioning
- **Organization Service** (Port 8002) - Organization management with Service Bus integration
- **API Gateway** (Port 8003) - Centralized documentation and service aggregation
- **Shared Components** - Common utilities, authentication, and core functionality
- **Infrastructure** - Azure Bicep templates for cloud deployment
- **Nginx Proxy** - Reverse proxy for service routing and load balancing

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
  - API Docs: http://localhost:8001/docs
  - API v1: http://localhost:8001/v1/api/
  - API v2: http://localhost:8001/v2/api/

- **Organization Service**: http://localhost:8002
  - Health: http://localhost:8002/health
  - API Docs: http://localhost:8002/docs
  - API: http://localhost:8002/api/

#### Via Nginx Reverse Proxy:
- **Gateway**: http://localhost
  - Auth Service: http://localhost/auth/
  - Organization Service: http://localhost/organization/
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
JWT_SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# services/organization-service/.env
DEBUG=true
COSMOS_DB_ENDPOINT=your-cosmos-endpoint
AZURE_SERVICE_BUS_CONNECTION_STRING=your-service-bus-connection-string
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

## 🛠️ Makefile Commands

This project includes a Makefile for common operations:

```bash
# View all available commands
make help

# Build all Docker images
make build

# Start all services in detached mode
make up

# Stop all services
make down

# Restart all services
make restart

# View logs from all services
make logs

# Clean up everything (containers, networks, volumes)
make clean

# Run health checks on all services
make test

# Check health status
make health

# Development mode (with logs)
make dev
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

## ☁️ Azure Deployment

This project includes Azure Bicep templates for cloud deployment:

### Infrastructure Components

- **Azure Functions** - Serverless compute for microservices
- **Azure Cosmos DB** - NoSQL database for data storage
- **Azure Service Bus** - Message queuing for service communication
- **Azure API Management** - API gateway and management

### Deployment Steps

1. **Prerequisites**:
   ```bash
   # Install Azure CLI
   az login
   az account set --subscription "your-subscription-id"
   ```

2. **Deploy Infrastructure**:
   ```bash
   # Deploy using Bicep templates
   az deployment group create \
     --resource-group your-rg \
     --template-file infrastructure/main.bicep \
     --parameters @infrastructure/parameters.json
   ```

3. **Deploy Functions**:
   ```bash
   # Deploy auth service
   cd services/auth-service
   func azure functionapp publish your-auth-function-app

   # Deploy organization service
   cd ../organization-service
   func azure functionapp publish your-org-function-app
   ```

### Production Considerations

- **Environment-specific configurations**
- **Azure Key Vault for secrets management**
- **Application Insights for monitoring**
- **Azure Front Door for load balancing**
- **Security hardening and compliance**

## 📝 API Documentation

### 🚀 Unified Documentation (NEW!)

**Access all microservices APIs in one place**: <http://localhost/docs>

The new API Gateway provides:
- **Centralized Swagger UI** with all microservices APIs
- **Service switching** between individual and unified views
- **Real-time API aggregation** from all running services
- **Health monitoring** and service discovery
- **Professional documentation interface** with service tagging

### Individual Service Documentation

Each service also provides its own interactive API documentation:

- **Auth Service**: <http://localhost:8001/docs>
  - Supports API versioning (v1 and v2)
  - JWT-based authentication
  - User management endpoints
- **Organization Service**: <http://localhost:8002/docs>
  - Organization CRUD operations
  - Service Bus integration
- **API Gateway**: <http://localhost:8003/docs>
  - Documentation aggregation service
  - Health monitoring endpoints

> 💡 **Tip**: Use the unified documentation at <http://localhost/docs> for the best experience!

## 🏗️ Project Structure

```
azure_functions_fastapi_microservices_boilerplate/
├── services/                    # Microservices
│   ├── auth-service/           # Authentication service
│   │   ├── src/               # Source code
│   │   ├── HttpTrigger/       # Azure Functions trigger
│   │   ├── Dockerfile         # Container configuration
│   │   └── requirements.txt   # Python dependencies
│   ├── organization-service/  # Organization management service
│   │   ├── src/               # Source code
│   │   ├── HttpTrigger/       # Azure Functions HTTP trigger
│   │   ├── ServiceBusListener/ # Service Bus trigger
│   │   ├── Dockerfile         # Container configuration
│   │   └── requirements.txt   # Python dependencies
│   └── shared/                # Shared components
│       ├── authentication/    # Auth utilities
│       ├── core/             # Core utilities
│       └── utils/            # Common utilities
├── infrastructure/                     # Infrastructure as Code
│   ├── main.bicep            # Main Bicep template
│   └── modules/              # Bicep modules
│       ├── apim.bicep        # API Management
│       ├── cosmos.bicep      # Cosmos DB
│       └── servicebus.bicep  # Service Bus
├── docs/                     # Documentation
│   ├── architecture.md      # Architecture overview
│   └── adr/                 # Architecture Decision Records
├── docker-compose.yml        # Docker Compose configuration
├── nginx.conf               # Nginx reverse proxy config
└── Makefile                 # Development commands
```

## 🔧 Features

### Authentication Service
- **API Versioning** - Support for v1 and v2 APIs
- **JWT Authentication** - Secure token-based auth
- **User Management** - Registration, login, profile management
- **Password Security** - Hashing, reset, change functionality
- **Role-based Access Control** - Admin and user roles

### Organization Service
- **CRUD Operations** - Full organization management
- **Service Bus Integration** - Asynchronous message processing
- **Event-driven Architecture** - Reactive service design

### Shared Components
- **Common Authentication** - Reusable auth utilities
- **Core Utilities** - Shared business logic
- **Standardized Responses** - Consistent API responses

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the project structure
4. Add tests for new functionality
5. Test with Docker Compose (`make test`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Submit a pull request

### Development Guidelines

- Follow the established project structure
- Use type hints in Python code
- Write comprehensive tests
- Update documentation for new features
- Follow PEP 8 coding standards
- Use meaningful commit messages

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Azure Functions Python Developer Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Azure Bicep Documentation](https://docs.microsoft.com/en-us/azure/azure-resource-manager/bicep/)


---

**Built with ❤️ using FastAPI, Azure Functions, and Docker**
