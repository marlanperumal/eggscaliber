"""Domain errors for metadata lifecycle and tenant isolation."""


class MetadataDomainError(Exception):
    """Base class for metadata domain failures."""


class TenantIsolationError(MetadataDomainError):
    """Raised when a caller references a resource outside its tenant scope."""


class MetadataWorkflowError(MetadataDomainError):
    """Raised when a lifecycle transition is invalid or prerequisites fail."""


class MetadataNotFoundError(MetadataDomainError):
    """Raised when a revision or related aggregate is unknown."""
