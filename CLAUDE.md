---
title: voxxy-gtm-mcp — Wrapper Identity
date: 2026-05-01
tags:
  - mcp
  - gtm
  - tag-manager
  - voxxy
  - wrapper
  - phase-1.5
---

# voxxy-gtm-mcp — CLAUDE Identity

> [!important] Purpose
> Voxxy MCP server for Google Tag Manager API v2. **Greenfield Python build** — no upstream fork. Built per Phase 2.2b sub-2 of [[../ad-platform-campaign-manager/V2-PLAN|ad-platform-campaign-manager v2.0.0]] (Wave 6 T3 research recommended greenfield over fork; no candidate combined Python + permissive license + production-quality architecture). Mirrors `google-marketing-solutions/google_ads_mcp` directory layout for structural consistency across the Voxxy wrapper-plugin family.

## License

> [!success] Apache License 2.0
> Greenfield project — Voxxy is the original author. Apache 2.0 selected to match the rest of the wrapper family (`voxxy-ga4-mcp`, `voxxy-bigquery-mcp`, the `google_ads_mcp` upstream that `voxxy-google-ads-mcp` wraps). Internal use, client-distribution, modification, and redistribution all permitted. **No upstream license-inheritance constraint** (unlike `voxxy-meta-ads-mcp` BSL audit). See [[LICENSE-NOTES]] for the full audit + dependency licenses.

## Position in the wrapper family

5th and final v2.0.0 wrapper plugin. Sibling pattern reference (Python same-tree, fork-of): [[../voxxy-ga4-mcp/CLAUDE|voxxy-ga4-mcp]]. Sibling pattern reference (Go subdir, fork-of): `voxxy-bigquery-mcp/CLAUDE.md`. Sibling pattern reference (Python same-tree, BSL upstream): `voxxy-meta-ads-mcp/CLAUDE.md`.

This is the first **greenfield** wrapper. ADR-031 (BACKLOG `v2.0.0-110`) language-aware wrapper-pattern authoring will use voxxy-gtm-mcp as its 4th data point.

## Voxxy modifications (vs. upstream)

| Modification | File(s) | Why |
|---|---|---|
| Greenfield build | `gtm_mcp/**` | No upstream fork; coded from scratch on `google-api-python-client` per Wave 6 T3 decision. |
| Mirrors `google_ads_mcp` layout | `gtm_mcp/coordinator.py`, `gtm_mcp/server.py`, `gtm_mcp/tools/*` | Structural family consistency. |
| Apache 2.0 license | `LICENSE` | Family standard. |
| User-Agent | `gtm_mcp/tools/utils.py` | `voxxy-gtm-mcp/<version>` (no `(fork-of: ...)` suffix — greenfield). |
| Auth: OAuth desktop default + SA opt-in | `gtm_mcp/auth.py` | Jerry-as-implementer single-user case is OAuth; SA path retained for shared-agency setups. |

## Tool surface

**v0.2: 22 tools shipped — v0.1 surface complete.** Total: 14 P0 + 6 P1 + 2 P2. Voxxy extensions (`scaffold_conversion_tag`, `diff_workspace_vs_published`, `validate_tag_assistant`) deferred to v0.3+.

| Tool | Module | Status | Purpose |
|---|---|---|---|
| `list_accounts` | `accounts.py` | v0.1 P0 | List GTM accounts the credentialed identity can access |
| `list_containers` | `containers.py` | v0.1 P0 | List containers under an account |
| `list_workspaces` | `workspaces.py` | v0.1 P0 | List workspaces in a container |
| `get_workspace_status` | `workspaces.py` | v0.1 P0 | Workspace change status vs. base version |
| `list_tags` | `tags.py` | v0.1 P0 | List tags in a workspace |
| `get_tag` | `tags.py` | v0.1 P0 | Get a tag (returns fingerprint for optimistic concurrency) |
| `create_tag` | `tags.py` | v0.1 P0 | Create a tag |
| `update_tag` | `tags.py` | v0.1 P0 | Update a tag (fingerprint-aware) |
| `list_triggers` | `triggers.py` | v0.1 P0 | List triggers in a workspace |
| `create_trigger` | `triggers.py` | v0.1 P0 | Create a trigger |
| `list_variables` | `variables.py` | v0.1 P0 | List user-defined variables |
| `create_variable` | `variables.py` | v0.1 P0 | Create a user-defined variable |
| `list_built_in_variables` | `variables.py` | v0.1 P0 | List enabled built-in variables |
| `enable_built_in_variables` | `variables.py` | v0.1 P0 | Enable built-in variables (e.g. `clickClasses`, `pageUrl`) |
| `create_version` | `versions.py` | v0.1 P1 | Snapshot a workspace into a new container version |
| `publish_version` | `versions.py` | v0.1 P1 | Publish a container version to live (fingerprint-aware) |
| `list_templates` | `templates.py` | v0.1 P1 | List sandboxed-JS custom templates |
| `get_template` | `templates.py` | v0.1 P1 | Get a custom template (returns fingerprint + templateData) |
| `create_template` | `templates.py` | v0.1 P1 | Create a custom template (sandboxed JS) |
| `update_template` | `templates.py` | v0.1 P1 | Update a custom template (fingerprint-aware) |
| `list_clients` | `clients.py` | v0.1 P2 | List sGTM clients (server-side containers) |
| `create_client` | `clients.py` | v0.1 P2 | Create an sGTM client |

## Auth

Two paths, OAuth Desktop is default:

1. **OAuth 2.0 Desktop (default)** — interactive browser flow on first run; refresh token cached at `~/.config/voxxy-gtm-mcp/token.json`. Requires a Desktop OAuth client `client_secrets.json` at the project root (or `VOXXY_GTM_MCP_OAUTH_CLIENT_SECRETS` env var).
2. **Service Account (opt-in)** — set `VOXXY_GTM_MCP_SERVICE_ACCOUNT_JSON` to a SA-JSON path. Optional `VOXXY_GTM_MCP_DELEGATED_USER` for domain-wide delegation. Required for non-interactive / shared-agency setups.

Scopes (combined v0.1 surface):
- `tagmanager.edit.containers`
- `tagmanager.publish`
- `tagmanager.readonly`
- `tagmanager.manage.accounts`

See [[config.example.yaml]] for setup paths.

## Pin policy

`google-api-python-client>=2.194.0,<3` — pinned to the v2.x major. Wave 6 T3 named v2.194.0 as the locked-in baseline (PyPI 2026-04-08, weekly cadence, GTM v2 via `build("tagmanager", "v2")`). Bump the lower bound only when an upstream feature is needed; the upper-bound `<3` guards against a major-version SDK rewrite breaking the discovery client surface.

## Smoke test status

⏸️ **Deferred to Phase 1.5.E sub-session** (BACKLOG `v2.0.0-110-smoke`, to be filed after this scaffold lands). Blocked on:

1. A Voxxy GCP project with the Tag Manager API enabled
2. Either (a) a Desktop OAuth client (Voxxy "voxxy-gtm-mcp-desktop") OR (b) a service account with GTM account access
3. A test GTM container the credentialed identity has read+write on

Smoke-test scope (3 tests):

1. `list_accounts` returns ≥1 GTM account
2. `list_containers` + `list_workspaces` resolve a known container's workspaces
3. `create_trigger` + `create_tag` + `list_tags` round-trips on a sandbox workspace, then the workspace is reverted

## Companion plugin

[[../ad-platform-campaign-manager/CLAUDE|ad-platform-campaign-manager]] — Phase 2.2b sub-4 will rewrite `/gads-conversion-tracking` to call this MCP for tag-side conversion-tracking config (alongside `voxxy-google-ads-mcp` for conversion-action setup, and the Data Manager API directly for offline imports). Phase 2.2b sub-5 (integration dogfood) is the validation gate.

## Related files in this folder

- [[README]] — Setup + usage
- [[LICENSE]] — Apache 2.0
- [[LICENSE-NOTES]] — License audit + dependency licenses + pin policy
- `gtm_mcp/auth.py` — OAuth + Service Account flows
- `gtm_mcp/coordinator.py` — Tool registry
- `gtm_mcp/server.py` — Stdio MCP entry-point
- `gtm_mcp/tools/utils.py` — Service builder, User-Agent, resource-name helpers
- `gtm_mcp/tools/{accounts,containers,workspaces,tags,triggers,variables,versions,templates,clients}.py` — 22 v0.1 surface tools (14 P0 + 6 P1 + 2 P2)
- `config.example.yaml` — OAuth + SA setup paths
- `start-mcp.cmd` — Windows launcher
- `tests/test_smoke.py` — pytest scaffold (smoke tests run only when `VOXXY_GTM_MCP_RUN_SMOKE=1`)

## Cross-references in the broader ecosystem

- [[../ad-platform-campaign-manager/v2-plan/03-mcp-plan|ad-platform-campaign-manager/v2-plan/03-mcp-plan.md]] § Phase 1.5 — spec source
- [[../ad-platform-campaign-manager/v2-plan/09-research-log|ad-platform-campaign-manager/v2-plan/09-research-log.md]] § Wave 6 Track T3 — greenfield-build decision
- [[../ad-platform-campaign-manager/DESIGN|ad-platform-campaign-manager/DESIGN.md]] § ADR-012 (wrappers) and forthcoming ADR-031 (language-aware wrapper pattern, BACKLOG `v2.0.0-110`)
- [[../ad-platform-campaign-manager/_config/ecosystem|ad-platform-campaign-manager/_config/ecosystem.md]] — wrapper plugin family table
- Sibling wrapper precedents:
  - [[../voxxy-ga4-mcp/CLAUDE|voxxy-ga4-mcp]] (Python same-tree, fork-of pattern — closest analogue for the directory layout, but voxxy-gtm-mcp is greenfield)
  - `voxxy-meta-ads-mcp/CLAUDE.md` (Python same-tree, BSL fork)
  - `voxxy-bigquery-mcp/CLAUDE.md` (Go subdir, Apache fork)

## Reference candidates (NOT fork targets)

Per Wave 6 T3 research, these are reference resources the implementation consulted, but none was forked as the primary codebase:

- `pouyanafisi/gtm-mcp` (MIT, TypeScript, 99 ops + 4 workflow helpers) — endpoint-coverage reference; `OPERATIONS.md` lists every GTM API v2 op. The workflow-helper pattern is what `scaffold_conversion_tag` (v0.2) will mirror.
- `shakibmolla/gtm-mcp` (CC0, Python) — auth-pattern reference (CC0 = no attribution required).
- `owntag/gtm-cli` (MIT, v1.5.8 commercial sGTM vendor's CLI) — naming/parameter convention reference.
- `google-marketing-solutions/google_ads_mcp` (Apache 2.0, voxxy-google-ads-mcp upstream) — directory layout reference (mirrored precisely).
- `vaidik/gtm-tools` (TypeScript) — `diff` command implementation reference for `diff_workspace_vs_published` (v0.2 extension).
