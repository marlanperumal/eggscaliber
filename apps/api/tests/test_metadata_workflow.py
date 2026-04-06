"""Tests for metadata lifecycle workflow and tenant isolation."""

from typing import Any, cast

import pytest
from pydantic import ValidationError

from apps.api.metadata_domain import (
    InMemoryMetadataWorkflowService,
    MetadataLifecycleState,
    MetadataNotFoundError,
    MetadataRevision,
    MetadataWorkflowError,
    PreviewGateReport,
)


def test_draft_preview_publish_happy_path() -> None:
    svc = InMemoryMetadataWorkflowService()
    draft = svc.create_draft_revision(
        "tenant-a",
        "instance-1",
        {"fields": [{"name": "x"}]},
    )
    assert draft.state == MetadataLifecycleState.DRAFT

    preview = svc.submit_for_preview(
        "tenant-a",
        draft.revision_id,
        PreviewGateReport(passed=True),
    )
    assert preview.state == MetadataLifecycleState.PREVIEW

    published = svc.publish("tenant-a", draft.revision_id)
    assert published.state == MetadataLifecycleState.PUBLISHED


def test_discard_preview_returns_to_draft() -> None:
    svc = InMemoryMetadataWorkflowService()
    draft = svc.create_draft_revision("t1", "i1", {})
    svc.submit_for_preview(
        "t1",
        draft.revision_id,
        PreviewGateReport(passed=True),
    )
    again = svc.discard_preview("t1", draft.revision_id)
    assert again.state == MetadataLifecycleState.DRAFT


def test_publish_from_draft_rejected() -> None:
    svc = InMemoryMetadataWorkflowService()
    draft = svc.create_draft_revision("t1", "i1", {})
    with pytest.raises(MetadataWorkflowError, match="PREVIEW"):
        svc.publish("t1", draft.revision_id)


def test_submit_for_preview_fails_when_gate_fails() -> None:
    svc = InMemoryMetadataWorkflowService()
    draft = svc.create_draft_revision("t1", "i1", {})
    with pytest.raises(MetadataWorkflowError, match="preview gate") as exc_info:
        svc.submit_for_preview(
            "t1",
            draft.revision_id,
            PreviewGateReport(passed=False, messages=("bad",)),
        )
    assert exc_info.value.details == ("bad",)


def test_tenant_mismatch_raises_not_found() -> None:
    svc = InMemoryMetadataWorkflowService()
    draft = svc.create_draft_revision("tenant-a", "i1", {})
    with pytest.raises(MetadataNotFoundError):
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


def test_create_draft_deep_copies_nested_body() -> None:
    svc = InMemoryMetadataWorkflowService()
    nested: list[dict[str, str]] = [{"name": "a"}]
    draft = svc.create_draft_revision("t1", "i1", {"fields": nested})
    nested[0]["name"] = "mutated"
    assert draft.body["fields"][0]["name"] == "a"


def test_get_revision_returns_snapshot_matching_create() -> None:
    svc = InMemoryMetadataWorkflowService()
    created = svc.create_draft_revision("t1", "i1", {"x": 1})
    loaded = svc.get_revision("t1", created.revision_id)
    assert loaded == created
    assert loaded is not created


def test_metadata_revision_rejects_empty_revision_id() -> None:
    with pytest.raises(ValidationError):
        MetadataRevision(
            revision_id="",
            tenant_id="t1",
            instance_id="i1",
            state=MetadataLifecycleState.DRAFT,
        )


def test_mutating_returned_revision_body_does_not_change_stored_revision() -> None:
    svc = InMemoryMetadataWorkflowService()
    returned = svc.create_draft_revision(
        "t1",
        "i1",
        {"items": [{"n": 1}]},
    )
    rid = returned.revision_id
    body = cast(dict[str, Any], returned.body)
    body["items"][0]["n"] = 999
    again = svc.get_revision("t1", rid)
    assert cast(dict[str, Any], again.body)["items"][0]["n"] == 1
