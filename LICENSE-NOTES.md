---
title: License & dependency audit
date: 2026-04-30
tags:
  - license
  - audit
  - voxxy
  - phase-1.5
---

# License & dependency audit

## Project license

> [!success] Apache License 2.0
> See [[LICENSE]] for the full text. Copyright 2026 Voxxy Creative Lab.

This is a **greenfield** project — Voxxy is the original author. There is no upstream fork-license-inheritance constraint (contrast with `voxxy-meta-ads-mcp`, which inherits BSL 1.1 from Pipeboard).

## Why Apache 2.0

Selected to match the rest of the Voxxy wrapper-plugin family:

| Sibling | License | Source |
|---|---|---|
| `voxxy-google-ads-mcp` | Apache 2.0 | upstream (`google-marketing-solutions/google_ads_mcp`) |
| `voxxy-bigquery-mcp` | Apache 2.0 | upstream (`googleapis/mcp-toolbox`) |
| `voxxy-ga4-mcp` | Apache 2.0 | upstream (`googleanalytics/google-analytics-mcp`) |
| `voxxy-meta-ads-mcp` | BSL 1.1 | upstream (`pipeboard-co/meta-ads-mcp`) — internal-use only |
| **`voxxy-gtm-mcp`** | **Apache 2.0** | **greenfield (Voxxy)** |

Apache 2.0 permits internal use, modification, redistribution, and (importantly) client-distribution without field-of-use restrictions. No managed-service gray area.

## Dependency licenses

All runtime dependencies have permissive licenses compatible with Apache 2.0 redistribution. Audited 2026-04-30 against PyPI metadata.

| Package | Pinned | License |
|---|---|---|
| `google-api-python-client` | `>=2.194.0,<3` | Apache 2.0 |
| `google-auth` | `>=2.40.0,<3` | Apache 2.0 |
| `google-auth-oauthlib` | `>=1.2.0,<2` | Apache 2.0 |
| `google-auth-httplib2` | `>=0.2.0,<1` | Apache 2.0 |
| `mcp` (modelcontextprotocol/python-sdk) | `>=1.24.0` | MIT |
| `google-adk` | `>=1.24.1` | Apache 2.0 |
| `httpx` | `>=0.28.1` | BSD-3-Clause |
| `pyyaml` | `>=6.0.2` | MIT |

Dev-only (`pip install -e .[dev]`):

| Package | License |
|---|---|
| `pytest` | MIT |
| `pytest-asyncio` | Apache 2.0 |
| `black` | MIT |

## Pin policy

`google-api-python-client>=2.194.0,<3` — locked to the v2.x major series. Wave 6 T3 named v2.194.0 as the baseline (PyPI 2026-04-08; weekly cadence; GTM v2 surface stable). The lower bound is moved up only when a needed feature/fix lands; the upper bound `<3` guards against a hypothetical v3 SDK rewrite changing the discovery-client surface.

`mcp>=1.24.0` mirrors the lower bound used by sibling `voxxy-ga4-mcp`. No upper bound; watch for major-version breaks via the modelcontextprotocol/python-sdk changelog.

`google-adk>=1.24.1` mirrors `voxxy-ga4-mcp`. The ADK is the wrapper Google publishes for `FunctionTool` registration and ADK→MCP type conversion.

## Reference repositories consulted (NOT vendored or forked)

Per Wave 6 T3 research, the following repos were reviewed during scaffolding but **not** forked or vendored. Their content does not appear in this codebase; they served only as reference material that informed independent reimplementation. License compatibility is therefore not load-bearing — but listed here for transparency.

| Repo | License | Role |
|---|---|---|
| `pouyanafisi/gtm-mcp` | MIT | Endpoint coverage reference (its `OPERATIONS.md` lists 99 GTM v2 ops + 4 workflow helpers). |
| `shakibmolla/gtm-mcp` | CC0-1.0 | Python OAuth + pytest pattern reference. |
| `owntag/gtm-cli` | MIT | Naming/parameter convention reference (commercial sGTM vendor). |
| `google-marketing-solutions/google_ads_mcp` | Apache 2.0 | Directory-layout reference (mirrored). |
| `vaidik/gtm-tools` | (TypeScript) | `diff` command reference for the v0.2 `diff_workspace_vs_published` extension. |

> [!note] Greenfield, not derived
> No code, comments, or docstrings were copied from any of these repos. The naming of common GTM operations (`list_tags`, `create_tag`, etc.) is dictated by the Google Tag Manager API v2 surface and is not derived from any of these projects.

## Open issues

None. Greenfield project; no upstream-license open questions to resolve.
