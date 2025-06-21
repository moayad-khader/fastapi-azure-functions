#!/usr/bin/env python3
"""
API Versioning Demo Script

This script demonstrates the API versioning functionality of the Authentication Service.
It shows how to interact with both v1 and v2 endpoints and the differences between them.
"""

import requests
import json
from typing import Dict, Any


class AuthAPIDemo:
    """Demo class for testing API versioning."""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        
    def make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Make a request to the API and return the response."""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            return {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "data": response.json() if response.content else None
            }
        except Exception as e:
            return {
                "error": str(e),
                "status_code": None,
                "headers": {},
                "data": None
            }
    
    def demo_version_info(self):
        """Demonstrate version information endpoint."""
        print("=" * 60)
        print("API VERSION INFORMATION")
        print("=" * 60)
        
        response = self.make_request("GET", "/api/version")
        print(f"Status Code: {response['status_code']}")
        print(f"Response: {json.dumps(response['data'], indent=2)}")
        print()
    
    def demo_root_endpoint(self):
        """Demonstrate root endpoint."""
        print("=" * 60)
        print("ROOT ENDPOINT")
        print("=" * 60)
        
        response = self.make_request("GET", "/")
        print(f"Status Code: {response['status_code']}")
        print(f"Response: {json.dumps(response['data'], indent=2)}")
        print()
    
    def demo_health_endpoints(self):
        """Demonstrate health endpoints for both versions."""
        print("=" * 60)
        print("HEALTH ENDPOINTS COMPARISON")
        print("=" * 60)
        
        # Test v1 health endpoint
        print("V1 Health Endpoint:")
        v1_response = self.make_request("GET", "/v1/api/")
        print(f"Status Code: {v1_response['status_code']}")
        print(f"API Version Header: {v1_response['headers'].get('x-api-version', 'Not present')}")
        print(f"Response: {json.dumps(v1_response['data'], indent=2)}")
        print()
        
        # Test v2 health endpoint
        print("V2 Health Endpoint:")
        v2_response = self.make_request("GET", "/v2/api/")
        print(f"Status Code: {v2_response['status_code']}")
        print(f"API Version Header: {v2_response['headers'].get('x-api-version', 'Not present')}")
        print(f"Response: {json.dumps(v2_response['data'], indent=2)}")
        print()
    
    def demo_version_negotiation(self):
        """Demonstrate version negotiation via headers."""
        print("=" * 60)
        print("VERSION NEGOTIATION VIA HEADERS")
        print("=" * 60)
        
        # Test with X-API-Version header
        print("Using X-API-Version header (v2) on v1 endpoint:")
        headers = {"X-API-Version": "v2"}
        response = self.make_request("GET", "/v1/api/", headers=headers)
        print(f"Status Code: {response['status_code']}")
        print(f"API Version Header: {response['headers'].get('x-api-version', 'Not present')}")
        print("Note: URL path takes precedence over header")
        print()
        
        # Test with Accept header
        print("Using Accept header with version:")
        headers = {"Accept": "application/vnd.api+json;version=2"}
        response = self.make_request("GET", "/v1/api/", headers=headers)
        print(f"Status Code: {response['status_code']}")
        print(f"API Version Header: {response['headers'].get('x-api-version', 'Not present')}")
        print("Note: URL path takes precedence over Accept header")
        print()
    
    def demo_login_comparison(self):
        """Demonstrate login endpoint differences between versions."""
        print("=" * 60)
        print("LOGIN ENDPOINT COMPARISON")
        print("=" * 60)
        
        # Sample login data for v1
        v1_login_data = {
            "email": "demo@example.com",
            "password": "demo123"
        }
        
        # Sample login data for v2 (enhanced)
        v2_login_data = {
            "email": "demo@example.com",
            "password": "demo123",
            "remember_me": True,
            "device_info": {
                "device_id": "demo-device-123",
                "type": "web",
                "name": "Demo Browser"
            }
        }
        
        print("V1 Login Request:")
        print(f"Endpoint: POST /v1/api/login")
        print(f"Payload: {json.dumps(v1_login_data, indent=2)}")
        v1_response = self.make_request("POST", "/v1/api/login", v1_login_data)
        print(f"Status Code: {v1_response['status_code']}")
        if v1_response['data']:
            print(f"Response Structure: {list(v1_response['data'].keys())}")
        print()
        
        print("V2 Login Request:")
        print(f"Endpoint: POST /v2/api/login")
        print(f"Payload: {json.dumps(v2_login_data, indent=2)}")
        v2_response = self.make_request("POST", "/v2/api/login", v2_login_data)
        print(f"Status Code: {v2_response['status_code']}")
        if v2_response['data']:
            print(f"Response Structure: {list(v2_response['data'].keys())}")
            if 'data' in v2_response['data']:
                print(f"Enhanced Data Fields: {list(v2_response['data']['data'].keys())}")
        print()
    
    def run_full_demo(self):
        """Run the complete API versioning demonstration."""
        print("🚀 Authentication Service API Versioning Demo")
        print("=" * 60)
        print()
        
        self.demo_version_info()
        self.demo_root_endpoint()
        self.demo_health_endpoints()
        self.demo_version_negotiation()
        self.demo_login_comparison()
        
        print("=" * 60)
        print("✅ Demo completed successfully!")
        print("=" * 60)
        print()
        print("Key Takeaways:")
        print("1. The API supports both v1 and v2 versions")
        print("2. Version can be specified via URL path (recommended)")
        print("3. Version negotiation middleware adds X-API-Version header")
        print("4. v2 provides enhanced features and richer response formats")
        print("5. v1 remains fully backward compatible")
        print()
        print("Next Steps:")
        print("- Visit http://localhost:8001/docs for interactive API documentation")
        print("- Check the API versioning guide in docs/api-versioning-guide.md")
        print("- Test your client applications against both versions")


def main():
    """Main function to run the demo."""
    demo = AuthAPIDemo()
    demo.run_full_demo()


if __name__ == "__main__":
    main()
