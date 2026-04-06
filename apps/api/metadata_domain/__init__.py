"""Metadata model boundaries, ingestion contracts, and workflow interfaces (STU-117)."""

from apps.api.metadata_domain.errors import (
    MetadataDomainError,
    MetadataNotFoundError,
    MetadataWorkflowError,
)
from apps.api.metadata_domain.models import (
    DatasetDefinition,
    DatasetInstance,
    IngestionSourceDescriptor,
    IngestionSourceKind,
    MetadataLifecycleState,
    MetadataRevision,
    PreviewGateReport,
)
from apps.api.metadata_domain.protocols import (
    IngestionAdapter,
    MetadataDefinitionRepository,
    MetadataInstanceRepository,
    MetadataWorkflowService,
)
from apps.api.metadata_domain.workflow import InMemoryMetadataWorkflowService

__all__ = [
    "DatasetDefinition",
    "DatasetInstance",
    "IngestionAdapter",
    "IngestionSourceDescriptor",
    "IngestionSourceKind",
    "InMemoryMetadataWorkflowService",
    "MetadataDefinitionRepository",
    "MetadataDomainError",
    "MetadataInstanceRepository",
    "MetadataLifecycleState",
    "MetadataNotFoundError",
    "MetadataRevision",
    "MetadataWorkflowError",
    "MetadataWorkflowService",
    "PreviewGateReport",
]
