#!/bin/bash

# API Versioning Demo Script
# This script demonstrates the API versioning functionality of the Authentication Service

BASE_URL="http://localhost:8001"

echo "🚀 Authentication Service API Versioning Demo"
echo "============================================================"
echo

# Function to make a pretty JSON output
pretty_json() {
    python3 -m json.tool 2>/dev/null || cat
}

# Function to print section header
print_header() {
    echo "============================================================"
    echo "$1"
    echo "============================================================"
}

# Test API Version Information
print_header "API VERSION INFORMATION"
echo "GET $BASE_URL/api/version"
echo
curl -s "$BASE_URL/api/version" | pretty_json
echo
echo

# Test Root Endpoint
print_header "ROOT ENDPOINT"
echo "GET $BASE_URL/"
echo
curl -s "$BASE_URL/" | pretty_json
echo
echo

# Test Health Endpoints Comparison
print_header "HEALTH ENDPOINTS COMPARISON"
echo "V1 Health Endpoint:"
echo "GET $BASE_URL/v1/api/"
echo
echo "Response:"
curl -s "$BASE_URL/v1/api/" | pretty_json
echo
echo "Headers:"
curl -s -I "$BASE_URL/v1/api/" | grep -i "x-api-version"
echo
echo

echo "V2 Health Endpoint:"
echo "GET $BASE_URL/v2/api/"
echo
echo "Response:"
curl -s "$BASE_URL/v2/api/" | pretty_json
echo
echo "Headers:"
curl -s -I "$BASE_URL/v2/api/" | grep -i "x-api-version"
echo
echo

# Test Version Negotiation
print_header "VERSION NEGOTIATION VIA HEADERS"
echo "Using X-API-Version header (v2) on v1 endpoint:"
echo "GET $BASE_URL/v1/api/ -H 'X-API-Version: v2'"
echo
echo "Headers in response:"
curl -s -I -H "X-API-Version: v2" "$BASE_URL/v1/api/" | grep -i "x-api-version"
echo "Note: URL path takes precedence over header"
echo
echo

echo "Using Accept header with version:"
echo "GET $BASE_URL/v1/api/ -H 'Accept: application/vnd.api+json;version=2'"
echo
echo "Headers in response:"
curl -s -I -H "Accept: application/vnd.api+json;version=2" "$BASE_URL/v1/api/" | grep -i "x-api-version"
echo "Note: URL path takes precedence over Accept header"
echo
echo

# Test Login Endpoints (will show error responses since we don't have real auth)
print_header "LOGIN ENDPOINT COMPARISON"
echo "V1 Login Request:"
echo "POST $BASE_URL/v1/api/login"
echo "Payload: {\"email\": \"demo@example.com\", \"password\": \"demo123\"}"
echo
echo "Response:"
curl -s -X POST "$BASE_URL/v1/api/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "password": "demo123"}' | pretty_json
echo
echo

echo "V2 Login Request (Enhanced):"
echo "POST $BASE_URL/v2/api/login"
echo "Payload: Enhanced with device_info and remember_me"
echo
echo "Response:"
curl -s -X POST "$BASE_URL/v2/api/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com", 
    "password": "demo123",
    "remember_me": true,
    "device_info": {
      "device_id": "demo-device-123",
      "type": "web",
      "name": "Demo Browser"
    }
  }' | pretty_json
echo
echo

# Test API Documentation
print_header "API DOCUMENTATION"
echo "Interactive API documentation is available at:"
echo "📖 $BASE_URL/docs"
echo
echo "You can also access ReDoc documentation at:"
echo "📖 $BASE_URL/redoc"
echo
echo

# Summary
print_header "✅ DEMO COMPLETED SUCCESSFULLY!"
echo
echo "Key Takeaways:"
echo "1. ✅ The API supports both v1 and v2 versions"
echo "2. ✅ Version can be specified via URL path (recommended)"
echo "3. ✅ Version negotiation middleware adds X-API-Version header"
echo "4. ✅ v2 provides enhanced features and richer response formats"
echo "5. ✅ v1 remains fully backward compatible"
echo
echo "Next Steps:"
echo "• Visit $BASE_URL/docs for interactive API documentation"
echo "• Check the API versioning guide in docs/api-versioning-guide.md"
echo "• Test your client applications against both versions"
echo "• Use docker-compose to run the full microservices stack"
echo
echo "============================================================"
