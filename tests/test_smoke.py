# Copyright 2026 Voxxy Creative Lab. Apache 2.0.

"""Live smoke tests — gated on VOXXY_GTM_MCP_RUN_SMOKE=1.

These tests call the real Tag Manager API and require:

    VOXXY_GTM_MCP_RUN_SMOKE=1                    # opt-in flag
    VOXXY_GTM_MCP_SMOKE_ACCOUNT_ID=6000000000    # numeric account id
    VOXXY_GTM_MCP_SMOKE_CONTAINER_ID=10000000    # numeric container id

Auth credentials must already be configured per config.example.yaml
(OAuth client_secrets.json + cached token, OR
VOXXY_GTM_MCP_SERVICE_ACCOUNT_JSON env var).

Without VOXXY_GTM_MCP_RUN_SMOKE=1 set, every test is skipped.
"""

import os

import pytest

SMOKE_ENABLED = os.environ.get("VOXXY_GTM_MCP_RUN_SMOKE") == "1"


pytestmark = pytest.mark.skipif(
    not SMOKE_ENABLED,
    reason="Live smoke tests skipped — set VOXXY_GTM_MCP_RUN_SMOKE=1 to run.",
)


@pytest.fixture(scope="module")
def account_id():
    val = os.environ.get("VOXXY_GTM_MCP_SMOKE_ACCOUNT_ID")
    if not val:
        pytest.skip("VOXXY_GTM_MCP_SMOKE_ACCOUNT_ID not set.")
    return val


@pytest.fixture(scope="module")
def container_id():
    val = os.environ.get("VOXXY_GTM_MCP_SMOKE_CONTAINER_ID")
    if not val:
        pytest.skip("VOXXY_GTM_MCP_SMOKE_CONTAINER_ID not set.")
    return val


def test_list_accounts():
    """Smoke test 1 — list_accounts returns ≥1 GTM account."""
    from gtm_mcp.tools.accounts import list_accounts
    result = list_accounts()
    assert "accounts" in result, f"Expected 'accounts' key, got: {result}"
    assert len(result["accounts"]) >= 1, "No GTM accounts visible to this identity."


def test_list_containers_and_workspaces(account_id, container_id):
    """Smoke test 2 — list_containers + list_workspaces resolve a known container."""
    from gtm_mcp.tools.containers import list_containers
    from gtm_mcp.tools.workspaces import list_workspaces

    containers = list_containers(account_id)
    assert "containers" in containers
    assert any(
        c.get("containerId") == container_id for c in containers["containers"]
    ), f"Container {container_id} not found in account {account_id}."

    workspaces = list_workspaces(account_id, container_id)
    assert "workspaces" in workspaces
    assert len(workspaces["workspaces"]) >= 1, "Container has no workspaces."


# Smoke test 3 — round-trip create_trigger + create_tag + list_tags + revert is
# left as a manual scenario for the Phase 1.5.E sub-session. Encoded here as
# a placeholder so the test surface is visible in this file.
def test_create_trigger_tag_roundtrip_TODO(account_id, container_id):
    pytest.skip(
        "Round-trip smoke test deferred to Phase 1.5.E manual run. "
        "Will: create a sandbox workspace, create a trigger + tag in it, "
        "list_tags to verify, then delete the workspace."
    )
