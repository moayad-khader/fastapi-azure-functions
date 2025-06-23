# API Gateway Service

A centralized API Gateway service that provides unified Swagger documentation for all microservices in the system.

## Features

- **Unified Documentation**: Aggregates OpenAPI specifications from all microservices
- **Interactive Swagger UI**: Beautiful, interactive documentation interface
- **Service Discovery**: Automatically discovers and documents available services
- **Health Monitoring**: Monitors health status of all connected microservices
- **Service Switching**: Easy navigation between individual service documentation

## Architecture

The API Gateway acts as a documentation aggregator that:

1. **Fetches OpenAPI specs** from all registered microservices
2. **Merges specifications** into a unified document with proper prefixing
3. **Serves interactive documentation** via Swagger UI
4. **Provides service health monitoring** for operational visibility

## Endpoints

### Documentation
- `GET /docs` - Unified Swagger UI for all microservices
- `GET /openapi.json` - Unified OpenAPI specification
- `GET /services` - Information about all registered services

### Health & Monitoring
- `GET /health` - API Gateway health check
- `GET /health/services` - Health status of all microservices

### Gateway-specific
- `GET /gateway/docs` - API Gateway's own documentation
- `GET /gateway/redoc` - API Gateway's ReDoc documentation

## Configuration

The API Gateway automatically discovers services based on the configuration in `src/app/docs/docs_controller.py`:

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
    }
}
```

## Usage

### Local Development

1. **Start all services** using Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. **Access unified documentation**:
   - Main documentation: http://localhost/docs
   - Services info: http://localhost/services
   - Health check: http://localhost/health

### Adding New Services

To add a new microservice to the documentation:

1. **Update the services configuration** in `docs_controller.py`
2. **Ensure the service** exposes `/openapi.json` endpoint
3. **Add routing** in `nginx.conf` if needed
4. **Restart the API Gateway** service

### Features of the Unified Documentation

- **Service Selector**: Switch between viewing all services or individual service docs
- **Prefixed Paths**: All endpoints are properly prefixed (e.g., `/auth/login`, `/organization/create`)
- **Tagged Operations**: All operations are tagged by service for easy navigation
- **Schema Merging**: Schemas are prefixed to avoid naming conflicts
- **Real-time Updates**: Documentation updates when services are restarted

## Docker

The API Gateway runs on port 8003 in the Docker Compose setup:

```yaml
api-gateway:
  build:
    context: ./services
    dockerfile: api-gateway/Dockerfile
  ports:
    - "8003:8000"
  depends_on:
    - auth-service
    - organization-service
```

## Azure Functions

The service is also configured to run as an Azure Function with the HTTP trigger in the `HttpTrigger/` directory.

## Environment Variables

- `LOG_LEVEL`: Logging level (default: INFO)
- `APP_VERSION`: Application version (default: 1.0.0)

## Development

### Running Locally

```bash
cd services/api-gateway
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

The service includes health checks and service discovery endpoints that can be tested:

```bash
# Test health
curl http://localhost:8003/health

# Test services discovery
curl http://localhost:8003/services

# Test unified OpenAPI spec
curl http://localhost:8003/openapi.json
```

## Troubleshooting

### Service Not Appearing in Documentation

1. **Check service health**: Visit `/health/services` to see if the service is reachable
2. **Verify OpenAPI endpoint**: Ensure the service exposes `/openapi.json`
3. **Check configuration**: Verify the service is properly configured in `docs_controller.py`
4. **Review logs**: Check API Gateway logs for connection errors

### Documentation Not Loading

1. **Check network connectivity** between API Gateway and microservices
2. **Verify service URLs** in the configuration
3. **Check CORS settings** if accessing from a browser
4. **Review browser console** for JavaScript errors

## Contributing

When adding new features:

1. **Update service configuration** for new microservices
2. **Add proper error handling** for service discovery
3. **Update documentation** and README files
4. **Test with all services** running and some services down
