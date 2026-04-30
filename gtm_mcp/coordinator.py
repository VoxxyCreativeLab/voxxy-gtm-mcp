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
The 14 v0.1 P0 tools are imported from gtm_mcp.tools.* sub-modules.
"""

import json

from google.adk.tools.function_tool import FunctionTool
from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type
from mcp import types as mcp_types
from mcp.server.lowlevel import Server

from gtm_mcp.tools.accounts import list_accounts
from gtm_mcp.tools.containers import list_containers
from gtm_mcp.tools.workspaces import list_workspaces, get_workspace_status
from gtm_mcp.tools.tags import list_tags, get_tag, create_tag, update_tag
from gtm_mcp.tools.triggers import list_triggers, create_trigger
from gtm_mcp.tools.variables import (
    list_variables,
    create_variable,
    list_built_in_variables,
    enable_built_in_variables,
)

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
