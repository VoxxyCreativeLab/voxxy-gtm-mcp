# Copyright 2026 Voxxy Creative Lab
# Licensed under the Apache License, Version 2.0.

"""Container-version GTM API v2 tools (P1).

Versioning is the bridge between workspace edits and a published live
container. ``create_version`` snapshots a workspace; ``publish_version``
promotes a snapshot to live.

GTM version reference:
    https://developers.google.com/tag-platform/tag-manager/api/v2/reference/accounts/containers/versions
GTM workspace.create_version reference:
    https://developers.google.com/tag-platform/tag-manager/api/v2/reference/accounts/containers/workspaces/create_version
"""

from typing import Any

from gtm_mcp.tools.utils import (
    get_service,
    shape_error,
    version_path,
    workspace_path,
)


def create_version(
    account_id: str,
    container_id: str,
    workspace_id: str,
    name: str,
    notes: str = "",
) -> dict[str, Any]:
    """Snapshots a workspace into a new container version.

    Wraps ``accounts.containers.workspaces.create_version``. The discovery
    client uses snake_case for ``createVersion``.

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.
        workspace_id: Numeric workspace ID.
        name: Human-readable version name.
        notes: Optional release notes.

    Returns:
        On success: ``CreateContainerVersionResponse`` with keys
            ``containerVersion``, ``compilerError``, ``syncStatus``,
            ``newWorkspacePath``.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        body = {"name": name}
        if notes:
            body["notes"] = notes
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .create_version(
                path=workspace_path(account_id, container_id, workspace_id),
                body=body,
            )
        )
        return request.execute()
    except Exception as exc:
        return shape_error("create_version", exc)


def publish_version(
    account_id: str,
    container_id: str,
    version_id: str,
    fingerprint: str | None = None,
) -> dict[str, Any]:
    """Publishes a container version to live.

    Wraps ``accounts.containers.versions.publish``. Requires the
    ``tagmanager.publish`` OAuth scope.

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.
        version_id: Numeric version ID (as returned by ``create_version``).
        fingerprint: Optional optimistic-concurrency token from a prior
            ``versions.get`` call. If supplied, the API rejects the publish
            when the server-side version has been modified since.

    Returns:
        On success: ``PublishContainerVersionResponse`` with keys
            ``containerVersion`` and ``compilerError``.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        kwargs: dict[str, Any] = {
            "path": version_path(account_id, container_id, version_id),
        }
        if fingerprint:
            kwargs["fingerprint"] = fingerprint
        request = (
            service.accounts()
            .containers()
            .versions()
            .publish(**kwargs)
        )
        return request.execute()
    except Exception as exc:
        return shape_error("publish_version", exc)
