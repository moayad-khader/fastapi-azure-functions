# Activepieces-Inspired Project Structure Guide

This document outlines the new project structure inspired by the [activepieces TypeScript repository](https://github.com/activepieces/activepieces/tree/main/packages/server/api/src), adapted for Python Azure Functions microservices.

## Overview

The new structure follows domain-driven design principles with consistent patterns across all services, making the codebase more maintainable, scalable, and easier to understand.

## Project Structure

```
services/
├── shared/                           # Shared utilities across services
│   ├── core/                        # Core utilities and base classes
│   ├── database/                    # Database configuration and models
│   ├── authentication/              # Shared auth utilities
│   └── utils/                       # General utilities
│
├── auth-service/                    # Authentication service
│   ├── HttpTrigger/                 # Azure Function trigger
│   ├── src/
│   │   ├── main.py                  # Entry point
│   │   ├── app/
│   │   │   ├── app.py               # App configuration
│   │   │   ├── authentication/      # Auth domain module
│   │   │   ├── user/                # User management
│   │   │   ├── health/              # Health checks
│   │   │   └── core/                # Service-specific utilities
│   │   └── tests/                   # Tests
│   └── requirements.txt
│
└── [other-services]/                # Similar structure for other services
```

## Key Patterns

### 1. Domain-Driven Structure
Each business domain gets its own module with consistent file organization:

```
domain_module/
├── __init__.py
├── domain_controller.py            # API endpoints
├── domain_service.py               # Business logic
├── domain_models.py                # Data models
├── domain_utils.py                 # Domain-specific utilities
└── schemas/                        # Pydantic schemas
    ├── __init__.py
    ├── requests.py                  # Request schemas
    └── responses.py                 # Response schemas
```

### 2. Shared Infrastructure
Common functionality is centralized in the `shared/` directory:

- **Core**: Base classes, exceptions, middleware
- **Authentication**: JWT handling, decorators, permissions
- **Utils**: Logging, configuration, helpers

### 3. Consistent Naming Conventions
- Controllers: `{domain}_controller.py`
- Services: `{domain}_service.py`
- Models: `{domain}_models.py`
- Utilities: `{domain}_utils.py`

## Implementation Details

### Base Classes

All controllers inherit from `BaseController`:
```python
from shared.core.base_controller import BaseController

class AuthenticationController(BaseController):
    def __init__(self):
        super().__init__()
        self.auth_service = AuthenticationService()
```

All services inherit from `BaseService`:
```python
from shared.core.base_service import BaseService

class AuthenticationService(BaseService):
    def __init__(self):
        super().__init__()
```

### Error Handling

Consistent error handling using custom exceptions:
```python
from shared.core.exceptions import ValidationException, AuthenticationException

# In service
if not user:
    raise AuthenticationException("Invalid credentials")

# In controller
try:
    result = await self.service.method()
except ServiceException as e:
    raise self.handle_service_exception(e)
```

### Authentication & Authorization

Centralized authentication using decorators:
```python
from shared.authentication.decorators import get_current_user, require_permission
from shared.authentication.permissions import Permission

@router.get("/protected")
async def protected_endpoint(current_user: dict = Depends(get_current_user)):
    # Endpoint logic
```

### Response Standardization

All endpoints return standardized responses:
```python
return self.success_response(
    data=result,
    message="Operation successful",
    status_code=200
)
```

## Benefits

1. **Consistency**: All services follow the same patterns
2. **Maintainability**: Clear separation of concerns
3. **Reusability**: Shared utilities reduce code duplication
4. **Testability**: Modular structure makes testing easier
5. **Scalability**: Easy to add new domains and features
6. **Developer Experience**: Familiar structure across services

## Migration Guide

To migrate existing services to this structure:

1. Create the new directory structure
2. Move existing code into appropriate modules
3. Implement base classes and shared utilities
4. Update imports and dependencies
5. Add proper error handling and logging
6. Create tests for the new structure

## Best Practices

1. **Single Responsibility**: Each module should have a single, well-defined purpose
2. **Dependency Injection**: Use FastAPI's dependency injection system
3. **Error Handling**: Always use custom exceptions with proper error codes
4. **Logging**: Log all important operations and errors
5. **Validation**: Validate all inputs using Pydantic schemas
6. **Testing**: Write tests for all business logic
7. **Documentation**: Document all public APIs and complex logic

## Example Usage

See the `auth-service` implementation for a complete example of this structure in action.

## Future Enhancements

- Database integration with repositories
- Event-driven architecture with message queues
- API versioning support
- Rate limiting and throttling
- Comprehensive monitoring and metrics
