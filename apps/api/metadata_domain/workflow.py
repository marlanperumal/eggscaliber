"""Reference workflow engine implementing draft -> preview -> publish."""

from __future__ import annotations

import copy
import logging
import threading
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


def _isolated_revision(rev: MetadataRevision) -> MetadataRevision:
    """Return a deep copy so callers cannot mutate service-internal state."""
    return rev.model_copy(deep=True)


class InMemoryMetadataWorkflowService:
    """
    In-memory implementation of MetadataWorkflowService for tests and local dev.

    Persistence adapters replace this in production without changing call sites
    that depend on MetadataWorkflowService.

    A ``threading.Lock`` serializes access to ``_revisions`` so read-modify-write
    transitions are atomic under concurrent callers (e.g. multi-threaded local
    servers). Production adapters typically rely on storage-level consistency
    instead.
    """

    def __init__(self) -> None:
        self._revisions: dict[str, MetadataRevision] = {}
        self._lock = threading.Lock()

    def create_draft_revision(
        self,
        tenant_id: str,
        instance_id: str,
        body: Mapping[str, Any],
    ) -> MetadataRevision:
        with self._lock:
            revision_id = str(uuid.uuid4())
            rev = MetadataRevision(
                revision_id=revision_id,
                tenant_id=tenant_id,
                instance_id=instance_id,
                state=MetadataLifecycleState.DRAFT,
                body=copy.deepcopy(dict(body)),
            )
            self._revisions[revision_id] = rev
            logger.info(
                "metadata_revision_created",
                extra={
                    "revision_id": revision_id,
                    "tenant_id": tenant_id,
                    "instance_id": instance_id,
                    "state": rev.state,
                },
            )
            return _isolated_revision(rev)

    def get_revision(self, tenant_id: str, revision_id: str) -> MetadataRevision:
        """Return a tenant-scoped revision snapshot (deep-copied)."""
        with self._lock:
            rev = self._get_revision_locked(tenant_id, revision_id)
        return _isolated_revision(rev)

    def submit_for_preview(
        self,
        tenant_id: str,
        revision_id: str,
        gate: PreviewGateReport,
    ) -> MetadataRevision:
        with self._lock:
            rev = self._get_revision_locked(tenant_id, revision_id)
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
                deep=True,
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
            return _isolated_revision(updated)

    def publish(self, tenant_id: str, revision_id: str) -> MetadataRevision:
        with self._lock:
            rev = self._get_revision_locked(tenant_id, revision_id)
            if rev.state != MetadataLifecycleState.PREVIEW:
                raise MetadataWorkflowError(f"publish requires PREVIEW, got {rev.state}")

            updated = rev.model_copy(
                update={"state": MetadataLifecycleState.PUBLISHED},
                deep=True,
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
            return _isolated_revision(updated)

    def discard_preview(self, tenant_id: str, revision_id: str) -> MetadataRevision:
        with self._lock:
            rev = self._get_revision_locked(tenant_id, revision_id)
            if rev.state != MetadataLifecycleState.PREVIEW:
                raise MetadataWorkflowError(
                    f"discard_preview requires PREVIEW, got {rev.state}"
                )

            updated = rev.model_copy(
                update={"state": MetadataLifecycleState.DRAFT},
                deep=True,
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
            return _isolated_revision(updated)

    def _get_revision_locked(
        self, tenant_id: str, revision_id: str
    ) -> MetadataRevision:
        """Load revision; caller must hold ``self._lock``."""
        rev = self._revisions.get(revision_id)
        if rev is None or rev.tenant_id != tenant_id:
            raise MetadataNotFoundError(f"unknown revision {revision_id!r}")
        return rev
