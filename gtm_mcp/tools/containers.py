# Copyright 2026 Voxxy Creative Lab
# Licensed under the Apache License, Version 2.0.

"""Container-level GTM API v2 tools (P0)."""

from typing import Any

from gtm_mcp.tools.utils import account_path, get_service, shape_error


def list_containers(account_id: str) -> dict[str, Any]:
    """Lists every container under a Tag Manager account.

    Wraps ``accounts.containers.list``.

    Args:
        account_id: Numeric account ID (e.g. ``"6000000000"``). String
            allowed for very large IDs that exceed JSON-int safety.

    Returns:
        On success: ``{"containers": [...]}`` where each item carries
        ``containerId``, ``name``, ``publicId``, ``usageContext``, ``path``.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = service.accounts().containers().list(parent=account_path(account_id))
        response = request.execute()
        return {"containers": response.get("container", [])}
    except Exception as exc:
        return shape_error("list_containers", exc)
