# Authentication Service

A microservice for user authentication and authorization, built with FastAPI and Azure Functions, following the activepieces-inspired project structure.

## Features

- User registration and login
- JWT token-based authentication
- Password management (change, reset)
- User profile management
- Role-based access control
- Health checks and monitoring
- Comprehensive error handling and logging

## Project Structure

```
src/
├── main.py                          # Entry point
├── app/
│   ├── app.py                       # FastAPI app configuration
│   ├── authentication/              # Authentication domain
│   │   ├── authentication_controller.py
│   │   ├── authentication_service.py
│   │   ├── authentication_models.py
│   │   └── schemas/
│   │       ├── requests.py
│   │       └── responses.py
│   ├── user/                        # User management domain
│   │   ├── user_controller.py
│   │   ├── user_service.py
│   │   └── schemas/
│   ├── health/                      # Health checks
│   │   └── health_controller.py
│   └── core/                        # Service-specific utilities
│       └── dependencies.py
└── tests/                           # Test files
```

## API Endpoints

The Authentication Service supports multiple API versions for backward compatibility and feature enhancement.

### API Versioning
- **v1**: Legacy API with basic authentication features
- **v2**: Enhanced API with additional security features and detailed responses
- **Default**: v1 (for backward compatibility)

### Version Specification
- URL Path: `/v1/api/...` or `/v2/api/...`
- Header: `X-API-Version: v1` or `X-API-Version: v2`
- Accept Header: `Accept: application/vnd.api+json;version=1`

### Authentication Endpoints

#### v1 Endpoints (Legacy)
- `POST /v1/api/login` - User login
- `POST /v1/api/register` - User registration
- `POST /v1/api/refresh` - Refresh access token
- `POST /v1/api/change-password` - Change password
- `POST /v1/api/forgot-password` - Request password reset
- `POST /v1/api/reset-password` - Reset password
- `POST /v1/api/logout` - User logout
- `GET /v1/api/me` - Get current user info

#### v2 Endpoints (Enhanced)
- `POST /v2/api/login` - Enhanced login with device tracking and 2FA support
- `POST /v2/api/register` - Enhanced registration with extended profile fields
- `POST /v2/api/refresh` - Enhanced token refresh with device tracking
- `POST /v2/api/change-password` - Enhanced password change with device logout option
- `POST /v2/api/forgot-password` - Enhanced password reset with multiple delivery methods
- `POST /v2/api/reset-password` - Enhanced password reset with device logout option
- `POST /v2/api/logout` - Enhanced logout with device-specific options
- `GET /v2/api/me` - Enhanced user info with detailed profile and security data
- `GET /v2/api/security` - Security information and active sessions (v2 exclusive)

### User Management
- `GET /users/` - List users (admin only)
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user (admin only)

### Health Checks
- `GET /health/` - Basic health check
- `GET /health/ready` - Readiness check
- `GET /health/live` - Liveness check

## Environment Variables

```bash
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application Configuration
APP_NAME=Authentication Service
APP_VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO

# Database Configuration (when implemented)
DATABASE_URL=postgresql://user:password@localhost:5432/auth_db

# Azure Configuration
AZURE_STORAGE_CONNECTION_STRING=your-storage-connection-string
AZURE_SERVICE_BUS_CONNECTION_STRING=your-service-bus-connection-string
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables (create a `.env` file or set them in your environment)

3. Run the service locally:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

Run tests with pytest:
```bash
cd src
pytest tests/ -v
```

## Docker

Build and run with Docker:
```bash
docker build -t auth-service .
docker run -p 8000:8000 auth-service
```

## Azure Functions Deployment

The service is designed to work with Azure Functions. The `HttpTrigger` directory contains the Azure Functions configuration.

1. Deploy using Azure CLI:
```bash
func azure functionapp publish your-function-app-name
```

2. Or use the Azure portal for deployment

## Authentication Flow

1. **Registration**: User registers with email and password
2. **Login**: User authenticates and receives JWT tokens
3. **Authorization**: Protected endpoints verify JWT tokens
4. **Token Refresh**: Use refresh token to get new access token
5. **Logout**: Revoke refresh token (when implemented with database)

## Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Role-based access control
- Request logging and monitoring
- Input validation and sanitization
- Rate limiting (to be implemented)

## Error Handling

The service uses standardized error responses:

```json
{
  "success": false,
  "message": "Error description",
  "status_code": 400,
  "details": {
    "field": "Additional error details"
  }
}
```

## Logging

All operations are logged with structured logging:
- Request/response logging
- Authentication attempts
- Error tracking
- Performance metrics

## Development

### Adding New Endpoints

1. Create request/response schemas in `schemas/`
2. Add business logic to the service class
3. Create controller endpoints
4. Add tests
5. Update documentation

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for all public methods
- Keep functions small and focused
- Use meaningful variable names

## Contributing

1. Follow the established project structure
2. Write tests for new features
3. Update documentation
4. Follow the coding standards
5. Submit pull requests for review

## License

[Your License Here]
