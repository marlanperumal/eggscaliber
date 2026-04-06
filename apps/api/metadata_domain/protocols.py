"""Service and adapter interfaces for metadata ingestion and publishing."""

from __future__ import annotations

from typing import Any, Mapping, Protocol

from apps.api.metadata_domain.models import (
    DatasetDefinition,
    DatasetInstance,
    IngestionSourceDescriptor,
    MetadataRevision,
    PreviewGateReport,
)


class IngestionAdapter(Protocol):
    """Connector-specific raw access; must never mix tenant data."""

    def describe_source(self, tenant_id: str, source_ref: str) -> IngestionSourceDescriptor:
        """Return a tenant-scoped descriptor for the raw source."""

    def sample_column_headers(self, tenant_id: str, source_ref: str) -> tuple[str, ...]:
        """Return lightweight structure hints for draft metadata bootstrap."""


class MetadataDefinitionRepository(Protocol):
    """Read stable dataset definitions for a tenant."""

    def get_definition(self, tenant_id: str, definition_id: str) -> DatasetDefinition:
        """Load a definition or raise if missing or out of tenant scope."""


class MetadataInstanceRepository(Protocol):
    """Read dataset instances for a tenant."""

    def get_instance(self, tenant_id: str, instance_id: str) -> DatasetInstance:
        """Load an instance or raise if missing or out of tenant scope."""


class MetadataWorkflowService(Protocol):
    """draft -> preview -> publish orchestration for metadata revisions."""

    def create_draft_revision(
        self,
        tenant_id: str,
        instance_id: str,
        body: Mapping[str, Any],
    ) -> MetadataRevision:
        """Create a new revision in DRAFT."""

    def get_revision(self, tenant_id: str, revision_id: str) -> MetadataRevision:
        """Load a revision for read/validation; implementations return an isolated snapshot."""

    def submit_for_preview(
        self,
        tenant_id: str,
        revision_id: str,
        gate: PreviewGateReport,
    ) -> MetadataRevision:
        """Move DRAFT -> PREVIEW when preview gates pass."""

    def publish(self, tenant_id: str, revision_id: str) -> MetadataRevision:
        """Move PREVIEW -> PUBLISHED."""

    def discard_preview(self, tenant_id: str, revision_id: str) -> MetadataRevision:
        """Move PREVIEW -> DRAFT without publishing."""
