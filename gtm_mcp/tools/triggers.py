# Copyright 2026 Voxxy Creative Lab
# Licensed under the Apache License, Version 2.0.

"""Trigger-level GTM API v2 tools (P0).

GTM trigger schema reference:
    https://developers.google.com/tag-platform/tag-manager/api/v2/reference/accounts/containers/workspaces/triggers
"""

from typing import Any

from gtm_mcp.tools.utils import get_service, shape_error, workspace_path


def list_triggers(
    account_id: str, container_id: str, workspace_id: str
) -> dict[str, Any]:
    """Lists triggers in a workspace.

    Wraps ``accounts.containers.workspaces.triggers.list``.

    Returns:
        On success: ``{"triggers": [...]}``.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .triggers()
            .list(parent=workspace_path(account_id, container_id, workspace_id))
        )
        response = request.execute()
        return {"triggers": response.get("trigger", [])}
    except Exception as exc:
        return shape_error("list_triggers", exc)


def create_trigger(
    account_id: str,
    container_id: str,
    workspace_id: str,
    trigger: dict,
) -> dict[str, Any]:
    """Creates a trigger in a workspace.

    Wraps ``accounts.containers.workspaces.triggers.create``.

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.
        workspace_id: Numeric workspace ID.
        trigger: Trigger resource body. Required keys: ``name``, ``type``.
            Common shapes:

            Pageview::

                {"name": "All Pages", "type": "pageview"}

            Custom event (e.g. dataLayer ``purchase`` event)::

                {
                    "name": "DLE — purchase",
                    "type": "customEvent",
                    "customEventFilter": [{
                        "type": "equals",
                        "parameter": [
                            {"type": "TEMPLATE", "key": "arg0",
                             "value": "{{_event}}"},
                            {"type": "TEMPLATE", "key": "arg1",
                             "value": "purchase"}
                        ]
                    }]
                }

            Click — All elements::

                {"name": "All Clicks", "type": "click"}

    Returns:
        On success: created trigger resource (includes assigned ``triggerId``).
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .triggers()
            .create(
                parent=workspace_path(account_id, container_id, workspace_id),
                body=trigger,
            )
        )
        return request.execute()
    except Exception as exc:
        return shape_error("create_trigger", exc)
