# Copyright 2026 Voxxy Creative Lab. Apache 2.0.

"""Cheap import-only tests — verify the package wires up without auth.

These tests do NOT call the GTM API. They confirm:
    - All modules import cleanly
    - The coordinator builds its tools list (mocked service builder)
    - The MCP server entry-point is callable
"""

from unittest import mock


def test_package_imports():
    import gtm_mcp
    assert gtm_mcp.__version__ == "0.2.0"


def test_tool_modules_import():
    from gtm_mcp.tools import (
        accounts,
        clients,
        containers,
        tags,
        templates,
        triggers,
        utils,
        variables,
        versions,
        workspaces,
    )
    # P0 — accounts / containers / workspaces
    assert callable(accounts.list_accounts)
    assert callable(containers.list_containers)
    assert callable(workspaces.list_workspaces)
    assert callable(workspaces.get_workspace_status)
    # P0 — tags
    assert callable(tags.list_tags)
    assert callable(tags.get_tag)
    assert callable(tags.create_tag)
    assert callable(tags.update_tag)
    # P0 — triggers
    assert callable(triggers.list_triggers)
    assert callable(triggers.create_trigger)
    # P0 — variables
    assert callable(variables.list_variables)
    assert callable(variables.create_variable)
    assert callable(variables.list_built_in_variables)
    assert callable(variables.enable_built_in_variables)
    # P1 — versions
    assert callable(versions.create_version)
    assert callable(versions.publish_version)
    # P1 — templates
    assert callable(templates.list_templates)
    assert callable(templates.get_template)
    assert callable(templates.create_template)
    assert callable(templates.update_template)
    # P2 — clients
    assert callable(clients.list_clients)
    assert callable(clients.create_client)
    # Shared
    assert callable(utils.get_service)


def test_coordinator_registers_22_tools():
    # Patch the service builder so coordinator import doesn't try to auth.
    with mock.patch("gtm_mcp.tools.utils._build_service", return_value=mock.MagicMock()):
        # Force a clean import
        import importlib
        import gtm_mcp.coordinator
        importlib.reload(gtm_mcp.coordinator)
        assert len(gtm_mcp.coordinator.tools) == 22


def test_user_agent_format():
    from gtm_mcp.tools.utils import USER_AGENT
    assert USER_AGENT.startswith("voxxy-gtm-mcp/")
