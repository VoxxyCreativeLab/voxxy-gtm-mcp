# Copyright 2026 Voxxy Creative Lab
# Licensed under the Apache License, Version 2.0.

"""Account-level GTM API v2 tools (P0)."""

from typing import Any

from gtm_mcp.tools.utils import get_service, shape_error


def list_accounts() -> dict[str, Any]:
    """Lists every Tag Manager account the credentialed identity can access.

    Wraps `accounts.list` (https://www.googleapis.com/tagmanager/v2/accounts).

    Returns:
        On success: ``{"accounts": [...]}`` where each item carries ``accountId``,
        ``name``, ``path``, and ``shareData``.
        On error: ``{"error": {...}}`` from ``shape_error``.
    """
    try:
        service = get_service()
        request = service.accounts().list()
        response = request.execute()
        return {"accounts": response.get("account", [])}
    except Exception as exc:
        return shape_error("list_accounts", exc)
