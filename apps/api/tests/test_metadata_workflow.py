"""Tests for metadata lifecycle workflow and tenant isolation."""

import pytest

from apps.api.metadata_domain import (
    InMemoryMetadataWorkflowService,
    MetadataNotFoundError,
    MetadataWorkflowError,
    PreviewGateReport,
    TenantIsolationError,
)


def test_draft_preview_publish_happy_path() -> None:
    svc = InMemoryMetadataWorkflowService()
    draft = svc.create_draft_revision(
        "tenant-a",
        "instance-1",
        {"fields": [{"name": "x"}]},
    )
    assert draft.state == "draft"

    preview = svc.submit_for_preview(
        "tenant-a",
        draft.revision_id,
        PreviewGateReport(passed=True),
    )
    assert preview.state == "preview"

    published = svc.publish("tenant-a", draft.revision_id)
    assert published.state == "published"


def test_discard_preview_returns_to_draft() -> None:
    svc = InMemoryMetadataWorkflowService()
    draft = svc.create_draft_revision("t1", "i1", {})
    svc.submit_for_preview(
        "t1",
        draft.revision_id,
        PreviewGateReport(passed=True),
    )
    again = svc.discard_preview("t1", draft.revision_id)
    assert again.state == "draft"


def test_publish_from_draft_rejected() -> None:
    svc = InMemoryMetadataWorkflowService()
    draft = svc.create_draft_revision("t1", "i1", {})
    with pytest.raises(MetadataWorkflowError, match="PREVIEW"):
        svc.publish("t1", draft.revision_id)


def test_submit_for_preview_fails_when_gate_fails() -> None:
    svc = InMemoryMetadataWorkflowService()
    draft = svc.create_draft_revision("t1", "i1", {})
    with pytest.raises(MetadataWorkflowError, match="preview gate"):
        svc.submit_for_preview(
            "t1",
            draft.revision_id,
            PreviewGateReport(passed=False, messages=("bad",)),
        )


def test_tenant_mismatch_raises() -> None:
    svc = InMemoryMetadataWorkflowService()
    draft = svc.create_draft_revision("tenant-a", "i1", {})
    with pytest.raises(TenantIsolationError):
        svc.submit_for_preview(
            "tenant-b",
            draft.revision_id,
            PreviewGateReport(passed=True),
        )


def test_unknown_revision_raises() -> None:
    svc = InMemoryMetadataWorkflowService()
    with pytest.raises(MetadataNotFoundError):
        svc.publish("t1", "00000000-0000-0000-0000-000000000000")


def test_no_transitions_after_published() -> None:
    svc = InMemoryMetadataWorkflowService()
    draft = svc.create_draft_revision("t1", "i1", {})
    rid = draft.revision_id
    svc.submit_for_preview("t1", rid, PreviewGateReport(passed=True))
    svc.publish("t1", rid)
    with pytest.raises(MetadataWorkflowError, match="requires DRAFT"):
        svc.submit_for_preview("t1", rid, PreviewGateReport(passed=True))
    with pytest.raises(MetadataWorkflowError, match="requires PREVIEW"):
        svc.discard_preview("t1", rid)
