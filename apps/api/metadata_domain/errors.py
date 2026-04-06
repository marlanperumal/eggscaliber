"""Domain errors for metadata lifecycle and tenant isolation."""


class MetadataDomainError(Exception):
    """Base class for metadata domain failures."""


class TenantIsolationError(MetadataDomainError):
    """Raised when a caller references a resource outside its tenant scope."""


class MetadataWorkflowError(MetadataDomainError):
    """
    Raised when a lifecycle transition is invalid or prerequisites fail.

    ``details`` carries structured context (for example preview gate messages)
    without encoding it only in ``str(exc)``.
    """

    def __init__(self, message: str, *, details: tuple[str, ...] = ()) -> None:
        super().__init__(message)
        self.details = details


class MetadataNotFoundError(MetadataDomainError):
    """Raised when a revision or related aggregate is unknown."""
