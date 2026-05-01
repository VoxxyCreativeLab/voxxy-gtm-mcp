# Copyright 2026 Voxxy Creative Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

"""Shared utilities — Tag Manager API v2 service builder, User-Agent injection,
resource-name helpers, and response shaping.
"""

from importlib import metadata
from typing import Any

from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError

from gtm_mcp.auth import get_credentials


def _get_package_version_with_fallback() -> str:
    """Returns voxxy-gtm-mcp's package version, or 'unknown' if unresolved."""
    try:
        return metadata.version("voxxy-gtm-mcp")
    except Exception:
        return "unknown"


# User-Agent string injected on every Tag Manager API request. No upstream
# fork — this is a greenfield build; the User-Agent identifies voxxy-gtm-mcp
# directly without a `(fork-of: ...)` suffix (cf. sibling voxxy-ga4-mcp).
USER_AGENT = f"voxxy-gtm-mcp/{_get_package_version_with_fallback()}"

# GTM API surface
_API_SERVICE = "tagmanager"
_API_VERSION = "v2"


def _build_service() -> Resource:
    """Returns a Tag Manager API v2 service client with Voxxy User-Agent."""
    credentials = get_credentials()
    # cache_discovery=False avoids a noisy warning on Python 3.10+ where the
    # default file_cache backend isn't writable in some sandboxed contexts.
    service = build(
        _API_SERVICE,
        _API_VERSION,
        credentials=credentials,
        cache_discovery=False,
    )
    # Inject User-Agent on the underlying http transport. `_http.headers` is
    # the documented hook in google-api-python-client for static header
    # additions.
    if hasattr(service, "_http") and hasattr(service._http, "headers"):
        service._http.headers["user-agent"] = USER_AGENT
    return service


# Module-level lazy cache. The MCP server is long-lived in stdio mode, so we
# build the service once per process. Tests should not import this module
# directly — they should patch `_build_service`.
_SERVICE: Resource | None = None


def get_service() -> Resource:
    """Lazy-singleton accessor for the GTM API v2 service."""
    global _SERVICE
    if _SERVICE is None:
        _SERVICE = _build_service()
    return _SERVICE


# ---------- Resource-name helpers ----------
#
# GTM API v2 resource paths follow the pattern:
#   accounts/{accountId}
#   accounts/{accountId}/containers/{containerId}
#   accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}
#   accounts/{accountId}/containers/{containerId}/workspaces/{workspaceId}/tags/{tagId}
#
# Helpers below normalize ID inputs (numeric or path-string) into the
# expected `parent` / `path` parameters consumed by the discovery client.


def account_path(account_id: str | int) -> str:
    return f"accounts/{account_id}"


def container_path(account_id: str | int, container_id: str | int) -> str:
    return f"accounts/{account_id}/containers/{container_id}"


def workspace_path(
    account_id: str | int, container_id: str | int, workspace_id: str | int
) -> str:
    return (
        f"accounts/{account_id}/containers/{container_id}"
        f"/workspaces/{workspace_id}"
    )


def tag_path(
    account_id: str | int,
    container_id: str | int,
    workspace_id: str | int,
    tag_id: str | int,
) -> str:
    return (
        workspace_path(account_id, container_id, workspace_id)
        + f"/tags/{tag_id}"
    )


def version_path(
    account_id: str | int,
    container_id: str | int,
    version_id: str | int,
) -> str:
    return (
        container_path(account_id, container_id) + f"/versions/{version_id}"
    )


def template_path(
    account_id: str | int,
    container_id: str | int,
    workspace_id: str | int,
    template_id: str | int,
) -> str:
    return (
        workspace_path(account_id, container_id, workspace_id)
        + f"/templates/{template_id}"
    )


def client_path(
    account_id: str | int,
    container_id: str | int,
    workspace_id: str | int,
    client_id: str | int,
) -> str:
    return (
        workspace_path(account_id, container_id, workspace_id)
        + f"/clients/{client_id}"
    )


# ---------- Response shaping ----------


def shape_error(action: str, exc: Exception) -> dict[str, Any]:
    """Common error shape returned to the MCP client."""
    if isinstance(exc, HttpError):
        try:
            content = exc.content.decode("utf-8") if exc.content else ""
        except Exception:
            content = ""
        return {
            "error": {
                "action": action,
                "type": "HttpError",
                "status": getattr(exc.resp, "status", None),
                "reason": getattr(exc.resp, "reason", None),
                "content": content,
            }
        }
    return {
        "error": {
            "action": action,
            "type": type(exc).__name__,
            "message": str(exc),
        }
    }
