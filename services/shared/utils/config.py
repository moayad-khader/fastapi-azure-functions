"""Configuration management."""

import os
from typing import Any, Optional


class Config:
    """Configuration management class."""
    
    def __init__(self):
        """Initialize configuration."""
        self._config = {}
        self._load_from_environment()
    
    def _load_from_environment(self):
        """Load configuration from environment variables."""
        # Database configuration
        self._config.update({
            "DATABASE_URL": os.getenv("DATABASE_URL"),
            "DATABASE_HOST": os.getenv("DATABASE_HOST", "localhost"),
            "DATABASE_PORT": int(os.getenv("DATABASE_PORT", "5432")),
            "DATABASE_NAME": os.getenv("DATABASE_NAME", "app_db"),
            "DATABASE_USER": os.getenv("DATABASE_USER", "postgres"),
            "DATABASE_PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
            
            # JWT configuration
            "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production"),
            "ACCESS_TOKEN_EXPIRE_MINUTES": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
            "REFRESH_TOKEN_EXPIRE_DAYS": int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")),
            
            # Application configuration
            "APP_NAME": os.getenv("APP_NAME", "Microservices App"),
            "APP_VERSION": os.getenv("APP_VERSION", "1.0.0"),
            "DEBUG": os.getenv("DEBUG", "false").lower() == "true",
            "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
            
            # Azure configuration
            "AZURE_STORAGE_CONNECTION_STRING": os.getenv("AZURE_STORAGE_CONNECTION_STRING"),
            "AZURE_SERVICE_BUS_CONNECTION_STRING": os.getenv("AZURE_SERVICE_BUS_CONNECTION_STRING"),
            
            # External services
            "REDIS_URL": os.getenv("REDIS_URL"),
            "SMTP_HOST": os.getenv("SMTP_HOST"),
            "SMTP_PORT": int(os.getenv("SMTP_PORT", "587")),
            "SMTP_USER": os.getenv("SMTP_USER"),
            "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD"),
        })
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value."""
        self._config[key] = value
    
    def get_database_url(self) -> str:
        """Get database URL."""
        db_url = self.get("DATABASE_URL")
        if db_url:
            return db_url
        
        # Construct URL from individual components
        host = self.get("DATABASE_HOST")
        port = self.get("DATABASE_PORT")
        name = self.get("DATABASE_NAME")
        user = self.get("DATABASE_USER")
        password = self.get("DATABASE_PASSWORD")
        
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"
    
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.get("DEBUG", False)


# Global configuration instance
config = Config()
