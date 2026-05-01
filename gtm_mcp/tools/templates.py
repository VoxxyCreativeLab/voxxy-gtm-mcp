# Copyright 2026 Voxxy Creative Lab
# Licensed under the Apache License, Version 2.0.

"""Custom-template (sandboxed JS) GTM API v2 tools (P1).

GTM custom templates carry the sandboxed JavaScript implementation behind
custom tag and variable types. They live under a workspace and use the
fingerprint optimistic-concurrency pattern for updates.

GTM templates schema reference:
    https://developers.google.com/tag-platform/tag-manager/api/v2/reference/accounts/containers/workspaces/templates
"""

from typing import Any

from gtm_mcp.tools.utils import (
    get_service,
    shape_error,
    template_path,
    workspace_path,
)


def list_templates(
    account_id: str, container_id: str, workspace_id: str
) -> dict[str, Any]:
    """Lists custom templates in a workspace.

    Wraps ``accounts.containers.workspaces.templates.list``.

    Returns:
        On success: ``{"templates": [...]}``.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .templates()
            .list(parent=workspace_path(account_id, container_id, workspace_id))
        )
        response = request.execute()
        return {"templates": response.get("template", [])}
    except Exception as exc:
        return shape_error("list_templates", exc)


def get_template(
    account_id: str,
    container_id: str,
    workspace_id: str,
    template_id: str,
) -> dict[str, Any]:
    """Returns a single custom template by ID.

    Wraps ``accounts.containers.workspaces.templates.get``. Response
    includes ``fingerprint`` for optimistic-concurrency updates and
    ``templateData`` (the sandboxed-JS .tpl payload).

    Returns:
        On success: full template resource.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .templates()
            .get(
                path=template_path(
                    account_id, container_id, workspace_id, template_id
                )
            )
        )
        return request.execute()
    except Exception as exc:
        return shape_error("get_template", exc)


def create_template(
    account_id: str,
    container_id: str,
    workspace_id: str,
    template: dict,
) -> dict[str, Any]:
    """Creates a custom template in a workspace.

    Wraps ``accounts.containers.workspaces.templates.create``.

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.
        workspace_id: Numeric workspace ID.
        template: Template resource body. Required keys:

            - ``name``: Display name.
            - ``templateData``: The full sandboxed-JS .tpl file contents
              (including ``___INFO___``, ``___TEMPLATE_PARAMETERS___``,
              ``___SANDBOXED_JS_FOR_WEB_TEMPLATE___``, etc. blocks).

            Example::

                {
                    "name": "Voxxy — Conversion Linker (custom)",
                    "templateData": "___INFO___\\n{\\n  ...\\n}\\n___TEMPLATE_PARAMETERS___\\n[]\\n"
                }

    Returns:
        On success: created template resource (includes assigned
            ``templateId`` and ``fingerprint``).
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .templates()
            .create(
                parent=workspace_path(account_id, container_id, workspace_id),
                body=template,
            )
        )
        return request.execute()
    except Exception as exc:
        return shape_error("create_template", exc)


def update_template(
    account_id: str,
    container_id: str,
    workspace_id: str,
    template_id: str,
    template: dict,
    fingerprint: str | None = None,
) -> dict[str, Any]:
    """Updates an existing custom template.

    Wraps ``accounts.containers.workspaces.templates.update``.

    Args:
        account_id: Numeric account ID.
        container_id: Numeric container ID.
        workspace_id: Numeric workspace ID.
        template_id: Numeric template ID.
        template: New template body (full replacement).
        fingerprint: Optional optimistic-concurrency token from the most
            recent ``get_template`` call. If supplied, the API rejects the
            update when the server-side template has been modified since.

    Returns:
        On success: updated template resource.
        On error: ``{"error": {...}}``.
    """
    try:
        service = get_service()
        kwargs: dict[str, Any] = {
            "path": template_path(
                account_id, container_id, workspace_id, template_id
            ),
            "body": template,
        }
        if fingerprint:
            kwargs["fingerprint"] = fingerprint
        request = (
            service.accounts()
            .containers()
            .workspaces()
            .templates()
            .update(**kwargs)
        )
        return request.execute()
    except Exception as exc:
        return shape_error("update_template", exc)
