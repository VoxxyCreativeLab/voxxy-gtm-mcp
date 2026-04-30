# Copyright 2026 Voxxy Creative Lab
# Licensed under the Apache License, Version 2.0.

"""Variable-level GTM API v2 tools (P0) — user-defined variables and
container-level built-in variables.

GTM variable schema reference:
    https://developers.google.com/tag-platform/tag-manager/api/v2/reference/accounts/containers/workspaces/variables
GTM built-in variable reference:
    https://developers.google.com/tag-platform/tag-manager/api/v2/reference/accounts/containers/workspaces/built_in_variables
"""

from typing import Any

from gtm_mcp.tools.utils import get_service, shape_error, workspace_path


# ---------- User-defined variables ----------


def list_variables(
    account_id: str, container_id: str, workspace_id: str
) -> dict[str, Any]:
    """Lists user-defined variables in a workspace.

    Wraps ``accounts.containers.workspaces.variables.list``.

    Returns:
        On success: ``{"variables": [...]}``.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .variables()
            .list(parent=workspace_path(account_id, container_id, workspace_id))
        )
        response = request.execute()
        return {"variables": response.get("variable", [])}
    except Exception as exc:
        return shape_error("list_variables", exc)


def create_variable(
    account_id: str,
    container_id: str,
    workspace_id: str,
    variable: dict,
) -> dict[str, Any]:
    """Creates a user-defined variable in a workspace.

    Wraps ``accounts.containers.workspaces.variables.create``.

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.
        workspace_id: Numeric workspace ID.
        variable: Variable resource body. Required keys: ``name``, ``type``.
            Common shapes:

            DataLayer variable::

                {
                    "name": "DLV — ecommerce.value",
                    "type": "v",
                    "parameter": [
                        {"type": "INTEGER", "key": "dataLayerVersion",
                         "value": "2"},
                        {"type": "TEMPLATE", "key": "name",
                         "value": "ecommerce.value"}
                    ]
                }

            Constant::

                {
                    "name": "Const — GA4 Measurement ID",
                    "type": "c",
                    "parameter": [
                        {"type": "TEMPLATE", "key": "value",
                         "value": "G-XXXXXXXXXX"}
                    ]
                }

    Returns:
        On success: created variable resource.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .variables()
            .create(
                parent=workspace_path(account_id, container_id, workspace_id),
                body=variable,
            )
        )
        return request.execute()
    except Exception as exc:
        return shape_error("create_variable", exc)


# ---------- Built-in variables ----------


def list_built_in_variables(
    account_id: str, container_id: str, workspace_id: str
) -> dict[str, Any]:
    """Lists enabled built-in variables for a workspace.

    Wraps ``accounts.containers.workspaces.built_in_variables.list``.

    Returns:
        On success: ``{"builtInVariables": [...]}``.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .built_in_variables()
            .list(parent=workspace_path(account_id, container_id, workspace_id))
        )
        response = request.execute()
        return {"builtInVariables": response.get("builtInVariable", [])}
    except Exception as exc:
        return shape_error("list_built_in_variables", exc)


def enable_built_in_variables(
    account_id: str,
    container_id: str,
    workspace_id: str,
    types: list[str],
) -> dict[str, Any]:
    """Enables built-in variables of the specified types.

    Wraps ``accounts.containers.workspaces.built_in_variables.create``.

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.
        workspace_id: Numeric workspace ID.
        types: List of built-in variable type strings. Common values:
            ``"pageUrl"``, ``"pagePath"``, ``"pageHostname"``, ``"referrer"``,
            ``"event"``, ``"clickId"``, ``"clickClasses"``, ``"clickElement"``,
            ``"clickText"``, ``"clickUrl"``, ``"clickTarget"``, ``"formId"``,
            ``"formClasses"``, ``"formElement"``, ``"formText"``, ``"formUrl"``,
            ``"errorMessage"``, ``"errorUrl"``, ``"errorLine"``,
            ``"newHistoryUrl"``, ``"oldHistoryUrl"``, ``"newHistoryFragment"``,
            ``"oldHistoryFragment"``, ``"historySource"``, ``"historyChange"``,
            ``"environmentName"``, ``"containerId"``, ``"containerVersion"``,
            ``"debugMode"``, ``"randomNumber"``, ``"htmlId"``,
            ``"firstPartyServingUrl"``, ``"videoProvider"``, ``"videoStatus"``,
            ``"videoUrl"``, ``"videoTitle"``, ``"videoDuration"``,
            ``"videoCurrentTime"``, ``"videoPercent"``, ``"videoVisible"``,
            ``"scrollDepthThreshold"``, ``"scrollDepthUnits"``,
            ``"scrollDepthDirection"``, ``"elementVisibilityFirstTime"``,
            ``"elementVisibilityRatio"``, ``"elementVisibilityTime"``,
            ``"elementVisibilityRecentTime"``.

    Returns:
        On success: ``{"builtInVariable": [...]}`` with the enabled set.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .built_in_variables()
            .create(
                parent=workspace_path(account_id, container_id, workspace_id),
                type=types,
            )
        )
        return request.execute()
    except Exception as exc:
        return shape_error("enable_built_in_variables", exc)
