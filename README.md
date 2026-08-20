# GPT-PluginOS

> A federated capability control plane for discovering, comparing, routing, governing, and explaining the provider ecosystem around AvaTar-ArTs agents, skills, plugins, MCP servers, local tools, APIs, and creative infrastructure.

GPT-PluginOS answers one deceptively hard question:

> **Given an intent, which capability is needed, which providers can satisfy it, and which route is best under current quality, privacy, cost, risk, health, and project constraints?**

It is not another agent runtime and not another plugin list.

## Status: v0.2 foundation runtime

The repository now contains an installable, read-only control-plane runtime plus the documentation and Studio surfaces that preceded it.

Implemented today:

- normalized provider/capability/policy registry
- strict graph validation and duplicate/unknown-capability checks
- deterministic policy-aware provider ranking
- fail-closed hard constraints with no silent widening
- route explanation with `authorization_implied: false`
- overlap analysis and coverage audit
- metadata benchmark snapshots
- compiled route projection
- deterministic ecosystem lockfile and lockfile diff
- Mermaid/JSON graph export
- Studio dataset export
- JSON Schema contracts
- regression tests and GitHub Actions CI

Execution of provider actions remains outside PluginOS. SuperAgents/human policy remains responsible for authorization and execution.

## Install

```bash
python -m pip install .
pluginos --version
pluginos validate
```

Python 3.11+ is supported. The v0.2 runtime has no third-party runtime dependencies.

## Quick start

```bash
pluginos scan
pluginos providers
pluginos capabilities
pluginos route media.image.upscale --policy quality-first --json
pluginos explain media.image.upscale --policy balanced
pluginos overlaps
pluginos benchmark media --policy quality-first --json
pluginos audit
pluginos graph --format mermaid
pluginos lock --output pluginos.lock.json
pluginos compile --output pluginos.compiled.json
pluginos export-site site/data
```

See [docs/RUNTIME.md](docs/RUNTIME.md) for the full CLI and scope.

## Core principle

**Plugins are providers. Capabilities are the contract.**

Instead of hard-coding:

```text
use Magnific
```

a workflow requests:

```text
media.image.upscale
```

PluginOS can then rank eligible providers under a policy:

```text
quality-first -> Magnific
cost-aware    -> lower-cost eligible route
private-local -> Local Upscaler
```

The workflow stays stable even when providers change.

## Architecture

```text
intent
  -> capability
  -> provider graph
  -> policy + state + benchmark metadata
  -> advisory route
  -> approval/execution outside PluginOS
  -> provenance
```

The surrounding repositories keep their source-of-truth boundaries:

- **SuperSkills**: reusable capability/skill contracts
- **SuperAgents**: approvals, execution, verification, runtime orchestration
- **gpt-plugs**: governed external provider/action registry
- **Content Universe**: creative entities, assets, provenance, lineage
- **agent-skills**: broader experimental/specialist skill ecosystem
- **GPT-PluginOS**: normalized cross-source graph, policy, comparison, lockfile, and route projections

## Governance invariant

Provider selection is never authorization.

Risk classes include:

- `read_only`
- `external_write`
- `destructive_write`
- `financial`
- `identity_or_access`
- `publication`
- `code_change`
- `deployment`

Every JSON route response explicitly reports:

```json
{"authorization_implied": false}
```

## Registry and policies

The canonical seed registry lives in `pluginos/data/` and currently contains:

- 12 normalized providers
- 36 declared capabilities
- 5 policy presets

The Studio browser data in `site/data/` is synchronized to the same v0.2 records.

Use `--data-dir` with another directory containing `providers.json`, `capabilities.json`, and `policies.json` to test alternate registries without modifying the bundled defaults.

## Reproducibility

`pluginos lock` records source versions, registry counts, and a deterministic `graph_sha256` over normalized provider/capability/policy state.

```bash
pluginos lock --output before.json
# change registry
pluginos lock --output after.json
pluginos diff before.json after.json
```

The committed `pluginos.lock.json` is the v0.2 seed snapshot.

## Studio and field site

A dependency-free product surface lives in [`site/`](site/):

- [`site/index.html`](site/index.html) — command center
- [`site/studio.html`](site/studio.html) — routing, registry, governance, provenance, checkpoints
- [`site/advanced.html`](site/advanced.html) — advanced use cases and patterns
- [`site/market.html`](site/market.html) — positioning and commercialization
- [`site/revenue-studio.html`](site/revenue-studio.html) — revenue scenario/offer modeling

Preview locally:

```bash
python -m http.server 8080 --directory site
```

Refresh the Studio's runtime datasets with:

```bash
pluginos export-site site/data
```

## Testing and release check

```bash
python -m unittest discover -s tests -v
make release-check
```

CI repeats install, tests, validation, compile, lockfile, route, and audit smoke checks.

## Documentation

- [Runtime v0.2](docs/RUNTIME.md)
- [Architecture design](docs/superpowers/specs/2026-08-19-gpt-pluginos-design.md)
- [Operator handbook](docs/OPERATOR_HANDBOOK.md)
- [Extensive use cases](docs/USE_CASES.md)
- [Worked examples](docs/EXAMPLES.md)
- [Advanced patterns](docs/ADVANCED_PATTERNS.md)
- [Governance playbook](docs/GOVERNANCE_PLAYBOOK.md)
- [Benchmark playbook](docs/BENCHMARK_PLAYBOOK.md)
- [Ecosystem integrations](docs/ECOSYSTEM_INTEGRATIONS.md)
- [Runtime checkpoint](docs/checkpoints/2026-08-20-runtime-v0.2.md)

## Current roadmap boundary

v0.2 is the completed **foundation runtime**, not the end of the broader PluginOS roadmap.

Next phases remain intentionally separate:

1. live plugin/MCP/repository source adapters
2. live health and lifecycle observations
3. real provider benchmark execution
4. SuperAgents route-projection exchange
5. Content Universe provenance write adapters
6. canary/shadow observations and drift monitoring
7. hosted/team control plane

This boundary is deliberate: PluginOS should become the control plane around execution, not quietly duplicate the execution runtime it was designed to govern.
