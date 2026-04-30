# voxxy-gtm-mcp

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server for the [Google Tag Manager API v2](https://developers.google.com/tag-platform/tag-manager/api/v2). Exposes accounts, containers, workspaces, tags, triggers, and variables to MCP-enabled clients (Claude Code, Claude Desktop, etc.).

**Status: v0.1.0 alpha** — 14 P0 tools shipped (accounts / containers / workspaces / tags / triggers / variables). v0.1 full target is 22 tools (P1 versioning + templates and P2 sGTM clients still TODO). Voxxy extensions (`scaffold_conversion_tag`, `diff_workspace_vs_published`, `validate_tag_assistant`) deferred to v0.2.

## Why this exists

Built per Phase 2.2b sub-2 of the Voxxy [`ad-platform-campaign-manager`](https://github.com/VoxxyCreativeLab/ad-platform-campaign-manager) plugin v2.0.0. The plugin's `/gads-conversion-tracking` skill needs a programmatic interface to GTM container state for tag-side conversion-tracking automation. Wave 6 T3 research evaluated 8 candidate GTM MCP servers and recommended a greenfield Python build over forking any of them — no candidate combined the family Python preference, a permissive license, and production-quality architecture.

This MCP is one of five Voxxy wrapper plugins:

| Wrapper | Purpose | Layout |
|---|---|---|
| `voxxy-google-ads-mcp` | Google Ads API | (fork) |
| `voxxy-meta-ads-mcp` | Meta Marketing API | Python same-tree, BSL upstream |
| `voxxy-bigquery-mcp` | BigQuery via mcp-toolbox | Go subdir, Apache upstream |
| `voxxy-ga4-mcp` | GA4 Data API + Admin API | Python same-tree, Apache upstream |
| **`voxxy-gtm-mcp`** | **GTM API v2** | **Python greenfield, Apache** |

## Install

```bash
git clone https://github.com/VoxxyCreativeLab/voxxy-gtm-mcp.git
cd voxxy-gtm-mcp
python -m venv .venv
. .venv/bin/activate    # or .venv\Scripts\activate on Windows
pip install -e .[dev]
```

Requires Python 3.10+.

## Auth setup

The MCP supports two auth paths. **OAuth 2.0 Desktop is the default**.

### OAuth 2.0 Desktop (default)

1. In a Voxxy Google Cloud project, [enable the Tag Manager API](https://console.cloud.google.com/apis/library/tagmanager.googleapis.com).
2. Create an OAuth Desktop client at [APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials).
3. Download the client JSON to the project root as `client_secrets.json` (or set `VOXXY_GTM_MCP_OAUTH_CLIENT_SECRETS` to its absolute path).
4. First run will open a browser to consent. The refresh token is cached at `~/.config/voxxy-gtm-mcp/token.json`.

### Service Account (opt-in)

For non-interactive / shared-agency setups:

1. Create a service account in your GCP project; download the JSON key.
2. Grant the SA email access at the GTM account level (Admin → User Management → email-add).
3. Export `VOXXY_GTM_MCP_SERVICE_ACCOUNT_JSON=/abs/path/to/sa.json`. Optionally `VOXXY_GTM_MCP_DELEGATED_USER` for domain-wide delegation.

When the SA env var is set, the SA path is used; otherwise OAuth Desktop runs.

See [`config.example.yaml`](./config.example.yaml) for full setup detail.

## Run as MCP server

```bash
voxxy-gtm-mcp
```

The script is registered by `pyproject.toml` and starts a stdio MCP server.

### Wire into Claude Code

```bash
claude mcp add voxxy-gtm voxxy-gtm-mcp
```

Or if not on PATH:

```bash
claude mcp add voxxy-gtm /abs/path/to/.venv/bin/voxxy-gtm-mcp
```

Windows users — see [`start-mcp.cmd`](./start-mcp.cmd) for an example launcher.

## Tools (v0.1.0)

| Tool | Args | Returns |
|---|---|---|
| `list_accounts` | — | `{accounts: [...]}` |
| `list_containers` | `account_id` | `{containers: [...]}` |
| `list_workspaces` | `account_id`, `container_id` | `{workspaces: [...]}` |
| `get_workspace_status` | `account_id`, `container_id`, `workspace_id` | workspace status (mergeConflict, workspaceChange) |
| `list_tags` | `account_id`, `container_id`, `workspace_id` | `{tags: [...]}` |
| `get_tag` | `... ,` `tag_id` | tag resource |
| `create_tag` | `... ,` `tag` (dict body) | created tag |
| `update_tag` | `... ,` `tag_id`, `tag`, `fingerprint?` | updated tag |
| `list_triggers` | `... ,` `workspace_id` | `{triggers: [...]}` |
| `create_trigger` | `... ,` `trigger` (dict body) | created trigger |
| `list_variables` | `... ,` `workspace_id` | `{variables: [...]}` |
| `create_variable` | `... ,` `variable` (dict body) | created variable |
| `list_built_in_variables` | `... ,` `workspace_id` | `{builtInVariables: [...]}` |
| `enable_built_in_variables` | `... ,` `types` (list) | enabled-set |

See [`gtm_mcp/tools/`](./gtm_mcp/tools/) for body shape examples (GA4 event tag, Google Ads conversion, custom-event trigger, dataLayer variable, etc.).

## Roadmap

- **v0.1 (in progress)**: 22 tools target. P0 (this commit, 14 tools). P1 = `create_version` / `publish_version` / 4 templates tools. P2 = sGTM `list_clients` / `create_client`.
- **v0.2 (Voxxy extensions)**: `scaffold_conversion_tag(platform, trigger_type)` (opinionated GA4/Google-Ads/Meta-CAPI defaults), `diff_workspace_vs_published(...)`, `validate_tag_assistant(container_id)`.

## License

Apache 2.0 — see [LICENSE](./LICENSE) and [LICENSE-NOTES.md](./LICENSE-NOTES.md).

## Maintainers

[Voxxy Creative Lab](https://github.com/VoxxyCreativeLab) — `hello@voxxycreativelab.com`
