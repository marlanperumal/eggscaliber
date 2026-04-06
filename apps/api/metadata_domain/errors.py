"""Domain errors for metadata lifecycle and lookup failures."""


class MetadataDomainError(Exception):
    """Base class for metadata domain failures."""


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
