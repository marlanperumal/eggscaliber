"""Reference workflow engine implementing draft -> preview -> publish."""

from __future__ import annotations

import copy
import logging
import uuid
from typing import Any, Mapping

from apps.api.metadata_domain.errors import (
    MetadataNotFoundError,
    MetadataWorkflowError,
)
from apps.api.metadata_domain.models import (
    MetadataLifecycleState,
    MetadataRevision,
    PreviewGateReport,
)

logger = logging.getLogger(__name__)


class InMemoryMetadataWorkflowService:
    """
    In-memory implementation of MetadataWorkflowService for tests and local dev.

    Persistence adapters replace this in production without changing call sites
    that depend on MetadataWorkflowService.
    """

    def __init__(self) -> None:
        self._revisions: dict[str, MetadataRevision] = {}

    def create_draft_revision(
        self,
        tenant_id: str,
        dataset_instance_id: str,
        body: Mapping[str, Any],
    ) -> MetadataRevision:
        revision_id = str(uuid.uuid4())
        rev = MetadataRevision(
            revision_id=revision_id,
            tenant_id=tenant_id,
            dataset_instance_id=dataset_instance_id,
            state=MetadataLifecycleState.DRAFT,
            body=copy.deepcopy(dict(body)),
        )
        self._revisions[revision_id] = rev
        logger.info(
            "metadata_revision_created",
            extra={
                "revision_id": revision_id,
                "tenant_id": tenant_id,
                "dataset_instance_id": dataset_instance_id,
                "state": rev.state,
            },
        )
        return rev

    def submit_for_preview(
        self,
        tenant_id: str,
        revision_id: str,
        gate: PreviewGateReport,
    ) -> MetadataRevision:
        rev = self._get_revision(tenant_id, revision_id)
        if rev.state != MetadataLifecycleState.DRAFT:
            raise MetadataWorkflowError(
                f"submit_for_preview requires DRAFT, got {rev.state}"
            )
        if not gate.passed:
            raise MetadataWorkflowError(
                "preview gate failed; cannot enter PREVIEW",
                details=tuple(gate.messages),
            )

        updated = rev.model_copy(
            update={"state": MetadataLifecycleState.PREVIEW},
        )
        self._revisions[revision_id] = updated
        logger.info(
            "metadata_revision_preview",
            extra={
                "revision_id": revision_id,
                "tenant_id": tenant_id,
                "state": updated.state,
            },
        )
        return updated

    def publish(self, tenant_id: str, revision_id: str) -> MetadataRevision:
        rev = self._get_revision(tenant_id, revision_id)
        if rev.state != MetadataLifecycleState.PREVIEW:
            raise MetadataWorkflowError(f"publish requires PREVIEW, got {rev.state}")

        updated = rev.model_copy(
            update={"state": MetadataLifecycleState.PUBLISHED},
        )
        self._revisions[revision_id] = updated
        logger.info(
            "metadata_revision_published",
            extra={
                "revision_id": revision_id,
                "tenant_id": tenant_id,
                "state": updated.state,
            },
        )
        return updated

    def discard_preview(self, tenant_id: str, revision_id: str) -> MetadataRevision:
        rev = self._get_revision(tenant_id, revision_id)
        if rev.state != MetadataLifecycleState.PREVIEW:
            raise MetadataWorkflowError(
                f"discard_preview requires PREVIEW, got {rev.state}"
            )

        updated = rev.model_copy(
            update={"state": MetadataLifecycleState.DRAFT},
        )
        self._revisions[revision_id] = updated
        logger.info(
            "metadata_revision_preview_discarded",
            extra={
                "revision_id": revision_id,
                "tenant_id": tenant_id,
                "state": updated.state,
            },
        )
        return updated

    def _get_revision(self, tenant_id: str, revision_id: str) -> MetadataRevision:
        rev = self._revisions.get(revision_id)
        if rev is None or rev.tenant_id != tenant_id:
            raise MetadataNotFoundError(f"unknown revision {revision_id!r}")
        return rev
