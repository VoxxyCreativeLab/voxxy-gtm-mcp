@echo off
REM voxxy-gtm-mcp Windows launcher
REM
REM Activates the local .venv and runs the MCP server over stdio.
REM Wire into Claude Code with:
REM   claude mcp add voxxy-gtm "%~dp0start-mcp.cmd"

setlocal

REM Resolve script directory
set SCRIPT_DIR=%~dp0

REM Activate venv if present
if exist "%SCRIPT_DIR%.venv\Scripts\activate.bat" (
    call "%SCRIPT_DIR%.venv\Scripts\activate.bat"
)

REM Run the MCP server entry-point
python -m gtm_mcp.server

endlocal
