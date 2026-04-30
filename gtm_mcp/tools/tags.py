# Copyright 2026 Voxxy Creative Lab
# Licensed under the Apache License, Version 2.0.

"""Tag-level GTM API v2 tools (P0).

GTM tag schema reference:
    https://developers.google.com/tag-platform/tag-manager/api/v2/reference/accounts/containers/workspaces/tags
"""

from typing import Any

from gtm_mcp.tools.utils import (
    get_service,
    shape_error,
    tag_path,
    workspace_path,
)


def list_tags(
    account_id: str, container_id: str, workspace_id: str
) -> dict[str, Any]:
    """Lists tags in a workspace.

    Wraps ``accounts.containers.workspaces.tags.list``.

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.
        workspace_id: Numeric workspace ID.

    Returns:
        On success: ``{"tags": [...]}``.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .tags()
            .list(parent=workspace_path(account_id, container_id, workspace_id))
        )
        response = request.execute()
        return {"tags": response.get("tag", [])}
    except Exception as exc:
        return shape_error("list_tags", exc)


def get_tag(
    account_id: str,
    container_id: str,
    workspace_id: str,
    tag_id: str,
) -> dict[str, Any]:
    """Returns a single tag by ID.

    Wraps ``accounts.containers.workspaces.tags.get``.

    Returns:
        On success: full tag resource.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .tags()
            .get(path=tag_path(account_id, container_id, workspace_id, tag_id))
        )
        return request.execute()
    except Exception as exc:
        return shape_error("get_tag", exc)


def create_tag(
    account_id: str,
    container_id: str,
    workspace_id: str,
    tag: dict,
) -> dict[str, Any]:
    """Creates a tag in a workspace.

    Wraps ``accounts.containers.workspaces.tags.create``.

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.
        workspace_id: Numeric workspace ID.
        tag: Tag resource body. Required keys vary by tag type but always
            include ``name`` and ``type``. Common shapes:

            GA4 event tag::

                {
                    "name": "GA4 — purchase",
                    "type": "gaawe",
                    "parameter": [
                        {"type": "TEMPLATE", "key": "measurementId",
                         "value": "{{GA4 Measurement ID}}"},
                        {"type": "TEMPLATE", "key": "eventName",
                         "value": "purchase"}
                    ],
                    "firingTriggerId": ["{{Trigger ID}}"]
                }

            Google Ads conversion::

                {
                    "name": "Google Ads — conversion",
                    "type": "awct",
                    "parameter": [
                        {"type": "TEMPLATE", "key": "conversionId",
                         "value": "AW-XXXXXXXXX"},
                        {"type": "TEMPLATE", "key": "conversionLabel",
                         "value": "abcDEF"}
                    ],
                    "firingTriggerId": ["{{Trigger ID}}"]
                }

    Returns:
        On success: created tag resource (includes assigned ``tagId``).
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .tags()
            .create(
                parent=workspace_path(account_id, container_id, workspace_id),
                body=tag,
            )
        )
        return request.execute()
    except Exception as exc:
        return shape_error("create_tag", exc)


def update_tag(
    account_id: str,
    container_id: str,
    workspace_id: str,
    tag_id: str,
    tag: dict,
    fingerprint: str | None = None,
) -> dict[str, Any]:
    """Updates an existing tag.

    Wraps ``accounts.containers.workspaces.tags.update``.

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.
        workspace_id: Numeric workspace ID.
        tag_id: Numeric tag ID.
        tag: New tag body (full replacement).
        fingerprint: Optional optimistic-concurrency token from the most
            recent ``get_tag`` call. If supplied, the API rejects the update
            when the server-side tag has been modified since.

    Returns:
        On success: updated tag resource.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        kwargs = {
            "path": tag_path(account_id, container_id, workspace_id, tag_id),
            "body": tag,
        }
        if fingerprint:
            kwargs["fingerprint"] = fingerprint
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .tags()
            .update(**kwargs)
        )
        return request.execute()
    except Exception as exc:
        return shape_error("update_tag", exc)
