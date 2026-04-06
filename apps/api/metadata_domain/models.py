"""Version-stable metadata aggregates and ingestion-side contracts."""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field


class MetadataLifecycleState(StrEnum):
    """Editor and publish pipeline state for a metadata revision."""

    DRAFT = "draft"
    PREVIEW = "preview"
    PUBLISHED = "published"


class IngestionSourceKind(StrEnum):
    """Supported ingestion channels for MVP metadata foundations."""

    CSV = "csv"
    SPSS = "spss"
    POSTGRES = "postgres"


class DatasetDefinition(BaseModel):
    """Stable identity and naming for a dataset across instance periods."""

    model_config = ConfigDict(frozen=True)

    definition_id: str
    tenant_id: str
    name: str = Field(min_length=1)


class DatasetInstance(BaseModel):
    """Time-bounded dataset materialization tied to one definition."""

    model_config = ConfigDict(frozen=True)

    instance_id: str
    tenant_id: str
    definition_id: str


class IngestionSourceDescriptor(BaseModel):
    """What an ingestion adapter must expose before metadata editing."""

    model_config = ConfigDict(frozen=True)

    tenant_id: str
    kind: IngestionSourceKind
    ref: str = Field(min_length=1, description="Opaque connector-specific locator.")


class MetadataRevision(BaseModel):
    """One editable metadata snapshot for a dataset instance."""

    model_config = ConfigDict(frozen=True)

    revision_id: str
    tenant_id: str
    dataset_instance_id: str
    state: MetadataLifecycleState
    body: Mapping[str, Any] = Field(default_factory=dict)


class PreviewGateReport(BaseModel):
    """Result of preview-time validation (compatibility, schema, policy)."""

    model_config = ConfigDict(frozen=True)

    passed: bool
    messages: tuple[str, ...] = ()
