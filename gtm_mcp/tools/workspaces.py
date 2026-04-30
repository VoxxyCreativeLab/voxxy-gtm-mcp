# Copyright 2026 Voxxy Creative Lab
# Licensed under the Apache License, Version 2.0.

"""Workspace-level GTM API v2 tools (P0)."""

from typing import Any

from gtm_mcp.tools.utils import (
    container_path,
    get_service,
    shape_error,
    workspace_path,
)


def list_workspaces(account_id: str, container_id: str) -> dict[str, Any]:
    """Lists workspaces in a container.

    Wraps ``accounts.containers.workspaces.list``.

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.

    Returns:
        On success: ``{"workspaces": [...]}`` (workspaceId, name, description, path).
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .list(parent=container_path(account_id, container_id))
        )
        response = request.execute()
        return {"workspaces": response.get("workspace", [])}
    except Exception as exc:
        return shape_error("list_workspaces", exc)


def get_workspace_status(
    account_id: str, container_id: str, workspace_id: str
) -> dict[str, Any]:
    """Returns the change status of a workspace vs. its base version.

    Wraps ``accounts.containers.workspaces.getStatus``. Useful for the
    `diff_workspace_vs_published` Voxxy extension (deferred to v0.2).

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.
        workspace_id: Numeric workspace ID.

    Returns:
        On success: workspace-status payload (mergeConflict, workspaceChange).
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .getStatus(path=workspace_path(account_id, container_id, workspace_id))
        )
        return request.execute()
    except Exception as exc:
        return shape_error("get_workspace_status", exc)
