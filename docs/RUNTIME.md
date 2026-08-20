# GPT-PluginOS Runtime v0.2

GPT-PluginOS v0.2 turns the architecture/reference layer into an installable, read-only capability-control-plane runtime.

## Install

```bash
python -m pip install .
pluginos --version
pluginos validate
```

Python 3.11+ is supported. The runtime has no third-party runtime dependencies.

## Included commands

```bash
pluginos scan [--json]
pluginos validate
pluginos providers [--json]
pluginos capabilities [--json]
pluginos route <capability> [--policy balanced] [--json]
pluginos explain <capability> [--policy balanced]
pluginos overlaps [--json]
pluginos benchmark <capability-or-domain> [--policy balanced] [--json]
pluginos compile [--output FILE]
pluginos lock [--output FILE]
pluginos diff <lock-a> <lock-b>
pluginos graph [--format mermaid|json]
pluginos audit
pluginos export-site <directory>
```

`benchmark` in v0.2 is a **metadata snapshot**, not a live provider quality test. It ranks the normalized quality/privacy/latency/cost/health observations currently in the registry. Live benchmark harnesses remain a later phase.

## Safety boundary

Routing is advisory. Every JSON route response includes:

```json
{"authorization_implied": false}
```

PluginOS v0.2 does not execute provider actions, store credentials, broaden permissions, publish, deploy, or make financial changes. SuperAgents/human policy remains responsible for authorization and execution.

## Registry

The bundled seed registry contains normalized provider, capability, and policy records in `pluginos/data/`. Use `--data-dir` to operate against another compatible directory containing:

- `providers.json`
- `capabilities.json`
- `policies.json`

The strict validator rejects duplicate IDs and providers that reference unknown capabilities.

## Routing

Routes are computed from five normalized signals: quality, privacy, latency, cost, and health. Policies may also impose hard constraints such as local-only execution, maximum cost, degraded-provider exclusion, and read-only operation. Hard constraints are never widened automatically to force a route.

## Lockfile

`pluginos lock` creates a deterministic graph hash over provider/capability/policy state plus source versions. The generated timestamp is observational; `graph_sha256` is the stable comparison key for an unchanged registry.

## Studio export

```bash
pluginos export-site site/data
```

This writes the canonical provider/capability/policy datasets plus `compiled.json`, allowing the browser Studio to consume the same normalized records as the CLI.

## Testing

```bash
python -m unittest discover -s tests -v
pluginos validate
pluginos route media.image.upscale --policy quality-first --json
pluginos audit
```

## Current scope vs roadmap

Implemented now:

- local/bundled registry
- contract validation
- deterministic ranking
- route explanations
- overlap analysis
- metadata benchmark snapshots
- compiled route projection
- lockfile/diff
- graph export
- audit summary
- Studio dataset export
- schemas/tests/CI

Future phases:

- live plugin/MCP/source adapters
- live health observations
- real provider benchmark execution
- SuperAgents route-projection exchange
- Content Universe provenance write adapters
- canary/shadow execution observations
- hosted/team control plane
