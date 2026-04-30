# Copyright 2026 Voxxy Creative Lab
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0

"""Auth module — OAuth 2.0 desktop flow (default) + service account (opt-in).

Two code paths exist for v0.1:

1. **OAuth 2.0 Desktop App (default)** — interactive browser flow on first run;
   refresh-token + token cached at `~/.config/voxxy-gtm-mcp/token.json`.
   Targets the Jerry-as-implementer single-user case (most local work).

2. **Service Account (opt-in via VOXXY_GTM_MCP_SERVICE_ACCOUNT_JSON env var)** —
   non-interactive; requires GTM API access granted to the SA email at
   the GTM account level. Domain-wide delegation supported via the
   VOXXY_GTM_MCP_DELEGATED_USER env var.

Auth selection algorithm:
    1. If VOXXY_GTM_MCP_SERVICE_ACCOUNT_JSON is set, use SA path.
    2. Otherwise, use OAuth desktop flow with cached token.

Scopes (v0.1 surface — covers all 14 P0 + 6 P1 + 2 P2 tools):
    https://www.googleapis.com/auth/tagmanager.edit.containers
    https://www.googleapis.com/auth/tagmanager.publish
    https://www.googleapis.com/auth/tagmanager.readonly
    https://www.googleapis.com/auth/tagmanager.manage.accounts
"""

import os
from pathlib import Path

from google.auth.credentials import Credentials
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials as UserCredentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes — must cover all v0.1 tool operations. Tighter scopes per-tool would
# require multiple credential paths; v0.1 ships with one combined scope set.
SCOPES = [
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.publish",
    "https://www.googleapis.com/auth/tagmanager.readonly",
    "https://www.googleapis.com/auth/tagmanager.manage.accounts",
]

# Env var contract
ENV_SERVICE_ACCOUNT_JSON = "VOXXY_GTM_MCP_SERVICE_ACCOUNT_JSON"
ENV_DELEGATED_USER = "VOXXY_GTM_MCP_DELEGATED_USER"
ENV_OAUTH_CLIENT_SECRETS = "VOXXY_GTM_MCP_OAUTH_CLIENT_SECRETS"
ENV_TOKEN_PATH = "VOXXY_GTM_MCP_TOKEN_PATH"

# Defaults
DEFAULT_OAUTH_CLIENT_SECRETS = "client_secrets.json"
DEFAULT_TOKEN_PATH = Path.home() / ".config" / "voxxy-gtm-mcp" / "token.json"


def _load_oauth_credentials() -> Credentials:
    """OAuth 2.0 Desktop App flow. Cached token at DEFAULT_TOKEN_PATH."""
    client_secrets = os.environ.get(
        ENV_OAUTH_CLIENT_SECRETS, DEFAULT_OAUTH_CLIENT_SECRETS
    )
    token_path = Path(os.environ.get(ENV_TOKEN_PATH, str(DEFAULT_TOKEN_PATH)))
    creds: UserCredentials | None = None

    if token_path.exists():
        creds = UserCredentials.from_authorized_user_file(str(token_path), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        if not Path(client_secrets).exists():
            raise FileNotFoundError(
                f"OAuth client secrets file not found at '{client_secrets}'. "
                f"Set {ENV_OAUTH_CLIENT_SECRETS} or place a Desktop OAuth "
                f"client_secrets.json at the project root. See "
                f"config.example.yaml § 'OAuth desktop flow setup'."
            )
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets, SCOPES)
        # run_local_server opens a browser and binds to a random local port.
        creds = flow.run_local_server(port=0, open_browser=True)

    token_path.parent.mkdir(parents=True, exist_ok=True)
    token_path.write_text(creds.to_json())
    return creds


def _load_service_account_credentials() -> Credentials:
    """Service Account flow. Optional domain-wide delegation."""
    sa_path = os.environ[ENV_SERVICE_ACCOUNT_JSON]
    if not Path(sa_path).exists():
        raise FileNotFoundError(
            f"Service account JSON not found at '{sa_path}' "
            f"(from {ENV_SERVICE_ACCOUNT_JSON})."
        )
    creds = service_account.Credentials.from_service_account_file(
        sa_path, scopes=SCOPES
    )
    delegated = os.environ.get(ENV_DELEGATED_USER)
    if delegated:
        creds = creds.with_subject(delegated)
    return creds


def get_credentials() -> Credentials:
    """Returns credentials per the auth selection algorithm.

    Priority:
        1. Service account (env-driven, opt-in)
        2. OAuth 2.0 desktop (default)
    """
    if os.environ.get(ENV_SERVICE_ACCOUNT_JSON):
        return _load_service_account_credentials()
    return _load_oauth_credentials()
