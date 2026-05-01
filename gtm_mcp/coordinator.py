# Copyright 2026 Voxxy Creative Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

"""Singleton MCP server with Google Tag Manager API v2 tool registry.

Mirrors the sibling voxxy-ga4-mcp coordinator pattern — same google-adk +
mcp-python-sdk wrapping, same FunctionTool → adk_to_mcp_tool_type conversion.
The 22 v0.1-surface tools are imported from gtm_mcp.tools.* sub-modules
(14 P0 + 6 P1 + 2 P2).
"""

import json

from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type
from mcp import types as mcp_types
from mcp.server.lowlevel import Server

from gtm_mcp.tools.accounts import list_accounts
from gtm_mcp.tools.clients import create_client, list_clients
from gtm_mcp.tools.containers import list_containers
from gtm_mcp.tools.tags import create_tag, get_tag, list_tags, update_tag
from gtm_mcp.tools.templates import (
    create_template,
    get_template,
    list_templates,
    update_template,
)
from gtm_mcp.tools.triggers import create_trigger, list_triggers
from gtm_mcp.tools.variables import (
    create_variable,
    enable_built_in_variables,
    list_built_in_variables,
    list_variables,
)
from gtm_mcp.tools.versions import create_version, publish_version
from gtm_mcp.tools.workspaces import get_workspace_status, list_workspaces

tools = [
    # P0 — accounts / containers / workspaces (4)
    FunctionTool(list_accounts),
    FunctionTool(list_containers),
    FunctionTool(list_workspaces),
    FunctionTool(get_workspace_status),
    # P0 — tags (4)
    FunctionTool(list_tags),
    FunctionTool(get_tag),
    FunctionTool(create_tag),
    FunctionTool(update_tag),
    # P0 — triggers (2)
    FunctionTool(list_triggers),
    FunctionTool(create_trigger),
    # P0 — variables (4)
    FunctionTool(list_variables),
    FunctionTool(create_variable),
    FunctionTool(list_built_in_variables),
    FunctionTool(enable_built_in_variables),
    # P1 — versions (2)
    FunctionTool(create_version),
    FunctionTool(publish_version),
    # P1 — templates (4)
    FunctionTool(list_templates),
    FunctionTool(get_template),
    FunctionTool(create_template),
    FunctionTool(update_template),
    # P2 — clients (2)
    FunctionTool(list_clients),
    FunctionTool(create_client),
]

tool_map = {t.name: t for t in tools}

app = Server(name="Voxxy GTM MCP Server")

mcp_tools = [adk_to_mcp_tool_type(tool) for tool in tools]
# Workaround for google-adk/issues/948 (mirrors voxxy-ga4-mcp) — empty
# inputSchema for no-arg tools, and union-with-None type stripping.
for tool in mcp_tools:
    if tool.inputSchema == {}:
        tool.inputSchema = {"type": "object", "properties": {}}
    for prop in tool.inputSchema.get("properties", {}).values():
        if "anyOf" in prop and prop.get("type") == "null":
            del prop["type"]


@app.list_tools()
async def list_tools_handler() -> list[mcp_types.Tool]:
    return mcp_tools


@app.call_tool()
async def call_mcp_tool(name: str, arguments: dict) -> list[mcp_types.Content]:
    if name in tool_map:
        tool = tool_map[name]
        try:
            adk_tool_response = await tool.run_async(
                args=arguments,
                tool_context=None,
            )
            response_text = json.dumps(adk_tool_response, indent=2, default=str)
            return [mcp_types.TextContent(type="text", text=response_text)]
        except Exception as e:
            print(f"MCP Server: Error executing tool '{name}': {e}")
            error_text = json.dumps(
                {"error": f"Failed to execute tool '{name}': {str(e)}"}
            )
            return [mcp_types.TextContent(type="text", text=error_text)]

    error_text = json.dumps(
        {"error": f"Tool '{name}' not implemented by this server."}
    )
    return [mcp_types.TextContent(type="text", text=error_text)]
