#!/usr/bin/env python
# Copyright 2026 Voxxy Creative Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

"""Entry point for the Voxxy GTM MCP server."""

import asyncio
import traceback

import mcp.server
import mcp.server.stdio
from mcp.server.lowlevel import NotificationOptions
from mcp.server.models import InitializationOptions

import gtm_mcp.coordinator as coordinator


async def run_server_async():
    """Runs the MCP server over standard I/O."""
    print("Starting MCP Stdio Server:", coordinator.app.name)
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await coordinator.app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=coordinator.app.name,
                server_version="0.1.0",
                capabilities=coordinator.app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def run_server():
    """Synchronous wrapper to run the async MCP server."""
    asyncio.run(run_server_async())


if __name__ == "__main__":
    try:
        asyncio.run(run_server_async())
    except KeyboardInterrupt:
        print("\nMCP Server (stdio) stopped by user.")
    except Exception:
        print("MCP Server (stdio) encountered an error:")
        traceback.print_exc()
    finally:
        print("MCP Server (stdio) process exiting.")
