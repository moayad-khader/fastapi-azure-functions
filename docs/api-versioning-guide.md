# API Versioning Guide

This guide explains the API versioning strategy implemented in the Authentication Service and how to use it effectively.

## Overview

The Authentication Service supports multiple API versions to ensure backward compatibility while allowing for new features and improvements. Currently supported versions:

- **v1**: Legacy API with basic authentication features
- **v2**: Enhanced API with additional security features, detailed responses, and improved user management

## Version Negotiation

The API supports multiple ways to specify the desired version:

### 1. URL Path (Recommended)
```
GET /v1/api/auth/me    # Uses v1
GET /v2/api/auth/me    # Uses v2
```

### 2. Accept Header
```
Accept: application/vnd.api+json;version=1
Accept: application/vnd.api+json;version=2
```

### 3. Custom Header
```
X-API-Version: v1
X-API-Version: v2
```

### 4. Default Behavior
If no version is specified, the API defaults to **v1** for backward compatibility.

## API Differences

### Authentication Endpoints

#### Login
**v1 Endpoint**: `POST /v1/api/login`
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**v2 Endpoint**: `POST /v2/api/login`
```json
{
  "email": "user@example.com",
  "password": "password123",
  "remember_me": true,
  "device_info": {
    "device_id": "device-123",
    "type": "mobile",
    "name": "iPhone 12"
  },
  "two_factor_code": "123456"
}
```

#### Registration
**v1 Endpoint**: `POST /v1/api/register`
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "password123"
}
```

**v2 Endpoint**: `POST /v2/api/register`
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "terms_accepted": true,
  "marketing_consent": false
}
```

### Response Formats

#### v1 Response Format
```json
{
  "success": true,
  "message": "Login successful",
  "status_code": 200,
  "api_version": "v1",
  "data": {
    "access_token": "...",
    "refresh_token": "...",
    "user_id": "123"
  }
}
```

#### v2 Response Format
```json
{
  "success": true,
  "message": "Login successful",
  "status_code": 200,
  "api_version": "v2",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "tokens": {
      "access_token": "...",
      "refresh_token": "...",
      "token_type": "bearer",
      "expires_in": 3600,
      "refresh_expires_in": 86400,
      "issued_at": "2024-01-15T10:30:00Z",
      "device_id": "device-123"
    },
    "user": {
      "id": "123",
      "email": "user@example.com",
      "username": "johndoe",
      "first_name": "John",
      "last_name": "Doe",
      "full_name": "John Doe",
      "is_verified": true,
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "last_login": "2024-01-15T10:30:00Z",
      "login_count": 42,
      "roles": ["user"],
      "permissions": ["read:profile"]
    },
    "session_info": {
      "session_id": "session-456",
      "device_info": {...},
      "remember_me": true
    },
    "security_info": {
      "two_factor_enabled": false,
      "last_password_change": "2024-01-01T00:00:00Z",
      "failed_login_attempts": 0
    }
  },
  "metadata": {
    "login_method": "password",
    "device_tracked": true,
    "two_factor_used": false
  }
}
```

## v2 Exclusive Features

### Enhanced Security Endpoints

#### Get Security Information
```
GET /v2/api/security
```
Returns detailed security information including active sessions, recent security events, and security settings.

#### Enhanced Logout
```
POST /v2/api/logout?logout_all_devices=true
```
Supports logging out from all devices or just the current device.

#### Enhanced Password Operations
```
POST /v2/api/change-password
{
  "current_password": "old_password",
  "new_password": "new_password",
  "logout_all_devices": true
}
```

### Enhanced User Profile
v2 provides much more detailed user profile information including:
- Full name composition
- Profile completeness percentage
- Security level assessment
- Login statistics
- Role and permission details

## Migration Guide

### From v1 to v2

1. **Update Request URLs**: Change `/v1/api/` to `/v2/api/`
2. **Handle Enhanced Responses**: Update your client code to handle the richer response format
3. **Optional Fields**: Take advantage of new optional fields in requests
4. **Error Handling**: v2 provides more detailed error information

### Backward Compatibility

- v1 endpoints remain fully functional
- No breaking changes to existing v1 functionality
- v1 will be supported indefinitely for existing integrations

## Best Practices

1. **Always specify version explicitly** in production applications
2. **Use URL path versioning** for better caching and debugging
3. **Handle version-specific features gracefully** in your client code
4. **Monitor deprecation headers** for future version changes
5. **Test against both versions** during development

## Version Information Endpoint

Get information about all supported versions:
```
GET /api/version
```

Response:
```json
{
  "supported_versions": ["v1", "v2"],
  "default_version": "v1",
  "latest_version": "v2",
  "deprecated_versions": []
}
```

## Headers

All responses include version information in headers:
- `X-API-Version`: The version that processed the request
- `Deprecation`: Present if the version is deprecated
- `Sunset`: Date when deprecated version will be removed (if applicable)

## Examples

### cURL Examples

#### v1 Login
```bash
curl -X POST "http://localhost:8001/v1/api/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

#### v2 Login with Enhanced Features
```bash
curl -X POST "http://localhost:8001/v2/api/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "remember_me": true,
    "device_info": {
      "device_id": "my-device-123",
      "type": "web",
      "name": "Chrome Browser"
    }
  }'
```

#### Using Header-based Versioning
```bash
curl -X POST "http://localhost:8001/api/login" \
  -H "Content-Type: application/json" \
  -H "X-API-Version: v2" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

## Support and Migration

For questions about API versioning or migration assistance:
1. Check the API documentation at `/docs`
2. Review this guide for common patterns
3. Test thoroughly in development environment
4. Contact the development team for complex migration scenarios
