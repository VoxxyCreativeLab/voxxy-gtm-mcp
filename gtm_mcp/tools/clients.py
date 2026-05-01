# Copyright 2026 Voxxy Creative Lab
# Licensed under the Apache License, Version 2.0.

"""sGTM client GTM API v2 tools (P2).

Server-side container clients route inbound HTTP requests to a tag-firing
pipeline. They only apply to server-side container types (``serverHosted``).

GTM clients schema reference:
    https://developers.google.com/tag-platform/tag-manager/api/v2/reference/accounts/containers/workspaces/clients
"""

from typing import Any

from gtm_mcp.tools.utils import get_service, shape_error, workspace_path


def list_clients(
    account_id: str, container_id: str, workspace_id: str
) -> dict[str, Any]:
    """Lists clients in a workspace (server-side containers only).

    Wraps ``accounts.containers.workspaces.clients.list``.

    Returns:
        On success: ``{"clients": [...]}``.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .clients()
            .list(parent=workspace_path(account_id, container_id, workspace_id))
        )
        response = request.execute()
        return {"clients": response.get("client", [])}
    except Exception as exc:
        return shape_error("list_clients", exc)


def create_client(
    account_id: str,
    container_id: str,
    workspace_id: str,
    client: dict,
) -> dict[str, Any]:
    """Creates a client in a workspace (server-side containers only).

    Wraps ``accounts.containers.workspaces.clients.create``.

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.
        workspace_id: Numeric workspace ID.
        client: Client resource body. Required keys: ``name``, ``type``.
            Common shapes:

            GA4 Client (intercepts GA4 hits)::

                {
                    "name": "GA4",
                    "type": "gaaw_client",
                    "parameter": [
                        {"type": "BOOLEAN", "key": "enableServerless",
                         "value": "true"},
                        {"type": "TEMPLATE", "key": "defaultPath",
                         "value": "/g/collect"}
                    ]
                }

            Measurement Protocol GA4 Client::

                {"name": "MP GA4", "type": "mp_ga4_client"}

    Returns:
        On success: created client resource (includes assigned ``clientId``).
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .clients()
            .create(
                parent=workspace_path(account_id, container_id, workspace_id),
                body=client,
            )
        )
        return request.execute()
    except Exception as exc:
        return shape_error("create_client", exc)
