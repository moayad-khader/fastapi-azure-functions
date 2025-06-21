"""Permission management utilities."""

from enum import Enum
from typing import List, Set


class Permission(Enum):
    """Define application permissions."""
    
    # User permissions
    USER_READ = "user:read"
    USER_WRITE = "user:write"
    USER_DELETE = "user:delete"
    
    # Organization permissions
    ORG_READ = "organization:read"
    ORG_WRITE = "organization:write"
    ORG_DELETE = "organization:delete"
    ORG_ADMIN = "organization:admin"
    
    # AI Agent permissions
    AGENT_READ = "agent:read"
    AGENT_WRITE = "agent:write"
    AGENT_DELETE = "agent:delete"
    AGENT_EXECUTE = "agent:execute"
    
    # System permissions
    SYSTEM_ADMIN = "system:admin"
    SYSTEM_READ = "system:read"


class PermissionChecker:
    """Check user permissions."""
    
    def __init__(self):
        # Define permission hierarchies
        self.permission_hierarchy = {
            Permission.SYSTEM_ADMIN.value: [
                # System admin has all permissions
                Permission.USER_READ.value,
                Permission.USER_WRITE.value,
                Permission.USER_DELETE.value,
                Permission.ORG_READ.value,
                Permission.ORG_WRITE.value,
                Permission.ORG_DELETE.value,
                Permission.ORG_ADMIN.value,
                Permission.AGENT_READ.value,
                Permission.AGENT_WRITE.value,
                Permission.AGENT_DELETE.value,
                Permission.AGENT_EXECUTE.value,
                Permission.SYSTEM_READ.value,
            ],
            Permission.ORG_ADMIN.value: [
                # Org admin has user and agent permissions within their org
                Permission.USER_READ.value,
                Permission.USER_WRITE.value,
                Permission.ORG_READ.value,
                Permission.ORG_WRITE.value,
                Permission.AGENT_READ.value,
                Permission.AGENT_WRITE.value,
                Permission.AGENT_EXECUTE.value,
            ],
        }
    
    def get_effective_permissions(self, user_permissions: List[str]) -> Set[str]:
        """Get all effective permissions including inherited ones."""
        effective_permissions = set(user_permissions)
        
        for permission in user_permissions:
            if permission in self.permission_hierarchy:
                effective_permissions.update(self.permission_hierarchy[permission])
        
        return effective_permissions
    
    def has_permission(self, user_permissions: List[str], required_permission: str) -> bool:
        """Check if user has a specific permission."""
        effective_permissions = self.get_effective_permissions(user_permissions)
        return required_permission in effective_permissions
    
    def has_permissions(self, user_permissions: List[str], required_permissions: List[str]) -> bool:
        """Check if user has all required permissions."""
        effective_permissions = self.get_effective_permissions(user_permissions)
        return all(perm in effective_permissions for perm in required_permissions)
    
    def has_any_permission(self, user_permissions: List[str], required_permissions: List[str]) -> bool:
        """Check if user has any of the required permissions."""
        effective_permissions = self.get_effective_permissions(user_permissions)
        return any(perm in effective_permissions for perm in required_permissions)
