from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
import json
from typing import Dict, Any, List
import asyncio
from datetime import datetime

from shared.core.base_controller import BaseController
from shared.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


class DocsController(BaseController):
    """Controller for aggregated documentation endpoints."""
    
    def __init__(self):
        super().__init__()
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


docs_controller = DocsController()


@router.get("/docs", response_class=HTMLResponse)
async def get_unified_docs():
    """Serve unified Swagger UI with all microservices."""
    try:
        # Generate the unified OpenAPI spec
        unified_spec = await get_unified_openapi_spec()
        
        # Create Swagger UI HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Microservices API Documentation</title>
            <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
            <style>
                html {{
                    box-sizing: border-box;
                    overflow: -moz-scrollbars-vertical;
                    overflow-y: scroll;
                }}
                *, *:before, *:after {{
                    box-sizing: inherit;
                }}
                body {{
                    margin:0;
                    background: #fafafa;
                }}
                .service-selector {{
                    background: #1f2937;
                    color: white;
                    padding: 1rem;
                    text-align: center;
                }}
                .service-selector h1 {{
                    margin: 0 0 1rem 0;
                    color: #10b981;
                }}
                .service-buttons {{
                    display: flex;
                    justify-content: center;
                    gap: 1rem;
                    flex-wrap: wrap;
                }}
                .service-btn {{
                    background: #10b981;
                    color: white;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 0.375rem;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                }}
                .service-btn:hover {{
                    background: #059669;
                }}
                .service-btn.active {{
                    background: #065f46;
                }}
            </style>
        </head>
        <body>
            <div class="service-selector">
                <h1>🚀 Microservices API Documentation</h1>
                <div class="service-buttons">
                    <button class="service-btn active" onclick="loadSpec('unified')">All Services</button>
                    <button class="service-btn" onclick="loadSpec('auth')">Auth Service</button>
                    <button class="service-btn" onclick="loadSpec('organization')">Organization Service</button>
                </div>
            </div>
            <div id="swagger-ui"></div>
            
            <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
            <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-standalone-preset.js"></script>
            <script>
                const specs = {{
                    unified: {json.dumps(unified_spec)},
                    auth: null,
                    organization: null
                }};
                
                let ui;
                
                function loadSpec(specType) {{
                    // Update active button
                    document.querySelectorAll('.service-btn').forEach(btn => btn.classList.remove('active'));
                    event.target.classList.add('active');
                    
                    let spec = specs[specType];
                    if (!spec) {{
                        // Load individual service spec
                        if (specType === 'auth') {{
                            fetch('/auth/openapi.json')
                                .then(response => response.json())
                                .then(data => {{
                                    specs.auth = data;
                                    initSwaggerUI(data);
                                }});
                        }} else if (specType === 'organization') {{
                            fetch('/organization/openapi.json')
                                .then(response => response.json())
                                .then(data => {{
                                    specs.organization = data;
                                    initSwaggerUI(data);
                                }});
                        }}
                    }} else {{
                        initSwaggerUI(spec);
                    }}
                }}
                
                function initSwaggerUI(spec) {{
                    ui = SwaggerUIBundle({{
                        spec: spec,
                        dom_id: '#swagger-ui',
                        deepLinking: true,
                        presets: [
                            SwaggerUIBundle.presets.apis,
                            SwaggerUIStandalonePreset
                        ],
                        plugins: [
                            SwaggerUIBundle.plugins.DownloadUrl
                        ],
                        layout: "StandaloneLayout"
                    }});
                }}
                
                // Initialize with unified spec
                window.onload = function() {{
                    initSwaggerUI(specs.unified);
                }};
            </script>
        </body>
        </html>
        """
        
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        logger.error(f"Failed to generate unified docs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=docs_controller.error_response(
                message="Failed to generate unified documentation"
            )
        )


@router.get("/openapi.json")
async def get_unified_openapi_spec():
    """Get unified OpenAPI specification for all microservices."""
    try:
        service_specs = {}
        
        async def fetch_service_spec(service_name: str, service_config: Dict[str, Any]):
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.get(service_config["openapi_url"])
                    if response.status_code == 200:
                        spec = response.json()
                        service_specs[service_name] = {
                            "spec": spec,
                            "config": service_config
                        }
                    else:
                        logger.warning(f"Failed to fetch spec for {service_name}: HTTP {response.status_code}")
            except Exception as e:
                logger.error(f"Error fetching spec for {service_name}: {str(e)}")
        
        # Fetch all service specs concurrently
        tasks = [
            fetch_service_spec(name, config) 
            for name, config in docs_controller.services.items()
        ]
        await asyncio.gather(*tasks)
        
        # Create unified OpenAPI spec
        unified_spec = {
            "openapi": "3.0.2",
            "info": {
                "title": "Microservices API",
                "description": "Unified API documentation for all microservices",
                "version": "1.0.0",
                "contact": {
                    "name": "API Support",
                    "email": "support@example.com"
                }
            },
            "servers": [
                {
                    "url": "http://localhost",
                    "description": "Local development server"
                }
            ],
            "paths": {},
            "components": {
                "schemas": {},
                "securitySchemes": {}
            },
            "tags": []
        }
        
        # Merge specs from all services
        for service_name, service_data in service_specs.items():
            if "spec" not in service_data:
                continue
                
            spec = service_data["spec"]
            config = service_data["config"]
            prefix = config["prefix"]
            
            # Add service tag
            service_tag = {
                "name": service_name,
                "description": f"Endpoints from {config['name']}"
            }
            unified_spec["tags"].append(service_tag)
            
            # Merge paths with prefix
            if "paths" in spec:
                for path, path_item in spec["paths"].items():
                    prefixed_path = f"{prefix}{path}"
                    
                    # Add service tag to all operations
                    for method, operation in path_item.items():
                        if isinstance(operation, dict) and "tags" in operation:
                            operation["tags"] = [service_name] + operation.get("tags", [])
                        elif isinstance(operation, dict):
                            operation["tags"] = [service_name]
                    
                    unified_spec["paths"][prefixed_path] = path_item
            
            # Merge components
            if "components" in spec:
                if "schemas" in spec["components"]:
                    for schema_name, schema_def in spec["components"]["schemas"].items():
                        # Prefix schema names to avoid conflicts
                        prefixed_name = f"{service_name}_{schema_name}"
                        unified_spec["components"]["schemas"][prefixed_name] = schema_def
                
                if "securitySchemes" in spec["components"]:
                    unified_spec["components"]["securitySchemes"].update(
                        spec["components"]["securitySchemes"]
                    )
        
        return unified_spec
        
    except Exception as e:
        logger.error(f"Failed to generate unified OpenAPI spec: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=docs_controller.error_response(
                message="Failed to generate unified OpenAPI specification"
            )
        )


@router.get("/services")
async def get_services_info():
    """Get information about all available services."""
    try:
        services_info = []
        
        for service_name, config in docs_controller.services.items():
            services_info.append({
                "name": service_name,
                "display_name": config["name"],
                "url": config["url"],
                "prefix": config["prefix"],
                "docs_url": f"{config['url']}/docs",
                "openapi_url": config["openapi_url"]
            })
        
        return docs_controller.success_response(
            data={
                "services": services_info,
                "total_services": len(services_info),
                "unified_docs_url": "/docs",
                "timestamp": datetime.utcnow().isoformat()
            },
            message="Services information retrieved successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to get services info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=docs_controller.error_response(
                message="Failed to retrieve services information"
            )
        )
