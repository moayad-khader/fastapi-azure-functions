# 🚀 Centralized Swagger Documentation Setup

This guide explains how to use the new centralized Swagger documentation system that aggregates all microservices APIs into a single, unified documentation interface.

## 🎯 What's New

I've created a dedicated **API Gateway service** that provides:

- **Unified Swagger UI** at `/docs` showing all microservices APIs
- **Service switching** between individual service documentation
- **Automatic API aggregation** from all running microservices
- **Health monitoring** for all services
- **Beautiful, interactive documentation** with service tagging

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Auth Service  │    │  Org Service    │    │  API Gateway    │
│   Port: 8001    │    │   Port: 8002    │    │   Port: 8003    │
│                 │    │                 │    │                 │
│ /docs           │    │ /docs           │    │ /docs (unified) │
│ /openapi.json   │    │ /openapi.json   │    │ /openapi.json   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Nginx       │
                    │   Port: 80      │
                    │                 │
                    │ / → /docs       │
                    │ /docs → Gateway │
                    │ /auth → Auth    │
                    │ /org → Org      │
                    └─────────────────┘
```

## 🚀 Quick Start

### 1. Start All Services

```bash
# Make sure Docker is running, then:
docker-compose up -d

# Wait for all services to be healthy (about 30-60 seconds)
docker-compose ps
```

### 2. Access Unified Documentation

Open your browser and go to:

**🎉 http://localhost/docs**

This will show you a beautiful, unified documentation interface with:

- **Service selector buttons** at the top
- **All APIs** from all microservices in one place
- **Proper prefixing** (e.g., `/auth/login`, `/organization/create`)
- **Service-based tagging** for easy navigation

### 3. Alternative Access Methods

- **Direct API Gateway**: http://localhost:8003/docs
- **Individual Services**:
  - Auth Service: http://localhost:8001/docs
  - Organization Service: http://localhost:8002/docs
- **Service Information**: http://localhost/services
- **Health Check**: http://localhost/health

## 📋 Features

### Unified Documentation Interface

The main `/docs` endpoint provides:

- **Service Selector**: Switch between "All Services", "Auth Service", and "Organization Service"
- **Unified View**: See all APIs in one place with proper prefixing
- **Individual Views**: Click service buttons to see individual service docs
- **Real-time Updates**: Documentation updates when services restart

### API Aggregation

- **Automatic Discovery**: Finds and aggregates OpenAPI specs from all services
- **Path Prefixing**: All paths are properly prefixed (e.g., `/auth/v1/api/login`)
- **Schema Merging**: Schemas are prefixed to avoid naming conflicts
- **Tag Organization**: All operations are tagged by service

### Health Monitoring

- **Service Health**: Monitor the health of all microservices
- **Connection Status**: See which services are reachable
- **Response Times**: Monitor service response times

## 🔧 Configuration

### Adding New Services

To add a new microservice to the documentation:

1. **Update API Gateway configuration** in `services/api-gateway/src/app/docs/docs_controller.py`:

```python
self.services = {
    "auth-service": {
        "name": "Authentication Service",
        "url": "http://auth-service:8000",
        "openapi_url": "http://auth-service:8000/openapi.json",
        "prefix": "/auth"
    },
    "organization-service": {
        "name": "Organization Service", 
        "url": "http://organization-service:8000",
        "openapi_url": "http://organization-service:8000/openapi.json",
        "prefix": "/organization"
    },
    # Add your new service here:
    "your-new-service": {
        "name": "Your New Service",
        "url": "http://your-new-service:8000",
        "openapi_url": "http://your-new-service:8000/openapi.json",
        "prefix": "/your-prefix"
    }
}
```

2. **Add to docker-compose.yml** (if not already present)
3. **Update nginx.conf** for routing (if needed)
4. **Restart services**: `docker-compose restart api-gateway`

### Service Requirements

For a service to appear in the unified documentation, it must:

- **Expose `/openapi.json`** endpoint (FastAPI does this automatically)
- **Be reachable** from the API Gateway container
- **Return valid OpenAPI 3.0+ specification**

## 🧪 Testing

### Manual Testing

1. **Check service health**:
   ```bash
   curl http://localhost/health
   ```

2. **List available services**:
   ```bash
   curl http://localhost/services
   ```

3. **Get unified OpenAPI spec**:
   ```bash
   curl http://localhost/openapi.json
   ```

### Troubleshooting

#### Service Not Appearing in Documentation

1. **Check service health**: Visit http://localhost/health/services
2. **Verify OpenAPI endpoint**: `curl http://localhost:8001/openapi.json`
3. **Check logs**: `docker-compose logs api-gateway`
4. **Restart API Gateway**: `docker-compose restart api-gateway`

#### Documentation Not Loading

1. **Check all services are running**: `docker-compose ps`
2. **Verify network connectivity**: `docker-compose logs nginx`
3. **Check browser console** for JavaScript errors
4. **Try direct access**: http://localhost:8003/docs

## 📁 File Structure

The API Gateway service includes:

```
services/api-gateway/
├── src/
│   ├── main.py                 # Entry point
│   └── app/
│       ├── app.py             # FastAPI application
│       ├── docs/
│       │   └── docs_controller.py  # Documentation aggregation
│       └── health/
│           └── health_controller.py # Health monitoring
├── HttpTrigger/               # Azure Functions support
├── Dockerfile                 # Container configuration
├── requirements.txt           # Python dependencies
└── README.md                  # Detailed documentation
```

## 🎨 Customization

### Styling

The documentation interface can be customized by modifying the HTML template in `docs_controller.py`. The current design includes:

- **Dark header** with service selector
- **Green accent colors** for buttons and branding
- **Responsive design** for mobile and desktop
- **Professional styling** with hover effects

### Service Discovery

The service discovery is currently static but can be enhanced to:

- **Auto-discover services** via Docker API
- **Support service registration** via API
- **Dynamic configuration** via environment variables

## 🚀 Next Steps

With this setup, you now have:

✅ **Centralized documentation** at http://localhost/docs  
✅ **Service health monitoring**  
✅ **Easy service addition** process  
✅ **Professional documentation interface**  
✅ **Docker and Azure Functions support**  

### Recommended Enhancements

1. **Add authentication** to the documentation interface
2. **Implement service registration** API
3. **Add API versioning** support in aggregation
4. **Create documentation themes** for different environments
5. **Add API testing** capabilities directly in the interface

## 📞 Support

If you encounter any issues:

1. **Check the logs**: `docker-compose logs api-gateway`
2. **Verify service health**: http://localhost/health/services
3. **Review configuration** in `docs_controller.py`
4. **Restart services**: `docker-compose restart`

Enjoy your new centralized API documentation! 🎉
