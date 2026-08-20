# GPT-PluginOS

> A federated capability control plane for discovering, comparing, routing, governing, and explaining the provider ecosystem around AvaTar-ArTs agents, skills, plugins, tools, and creative infrastructure.

GPT-PluginOS answers a deceptively hard question:

> **Given an intent, which capability is needed, which providers can satisfy it, and which route is best under current quality, privacy, cost, risk, health, and project constraints?**

It is not another agent runtime and not another plugin list.

## Field site

A dependency-free static field site now lives in [`site/`](site/):

- [`site/index.html`](site/index.html) — product command center and capability-routing demo
- [`site/advanced.html`](site/advanced.html) — advanced routing, governance, creator, engineering, research, benchmark, and drift scenarios
- [`site/market.html`](site/market.html) — market positioning, sellable offers, SaaS ladder, revenue flywheel, launch channels, and commercialization roadmap

Preview locally:

```bash
python -m http.server 8080 --directory site
```

The field site is intentionally dependency-free and presents architecture/reference behavior. It does not imply that every illustrated future CLI or automation capability is already implemented.

## Why it exists

Modern AI workspaces accumulate overlapping providers:

- ChatGPT plugins/apps/connectors
- MCP servers
- APIs
- local Python tools
- workflow engines
- specialist repositories
- creative generation providers
- research systems
- deployment systems
- internal agents and skills

Without a control plane, orchestration slowly hard-codes vendor names and loses track of why a provider was selected.

PluginOS introduces a stable middle layer:

```text
intent
  -> capability
  -> provider graph
  -> policy + benchmark + state
  -> advisory route
  -> approval/execution
  -> provenance
```

## Ecosystem position

```text
                        GPT-PluginOS
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
     discovery           compiler          governance
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
  SuperSkills            gpt-plugs          SuperAgents
  capabilities           providers          execution
       │                    │                    │
       └────────────────────┼────────────────────┘
                            ▼
                     Content Universe
                 provenance / lineage / assets
                            │
                    specialist systems
```

### Sources of truth

- **SuperSkills**: reusable capability/skill contracts
- **SuperAgents**: routing acceptance, approvals, execution, verification
- **gpt-plugs**: governed external provider/action registry
- **Content Universe**: creative entities, provenance, assets, lineage
- **agent-skills**: broader experimental/specialist skill ecosystem
- **GPT-PluginOS**: normalized cross-source graph, overlap, policy, benchmark, health, lockfile, and route projections

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

PluginOS may then rank:

```text
1. Magnific      premium specialist
2. Cloudinary    infrastructure transform
3. Local ESRGAN  private/offline fallback
```

The ranking can change without rewriting the workflow.

## Current status

The repository is in foundation/design phase. The approved federated architecture and operator/reference documentation are being established before runtime implementation.

The command examples in the documentation describe the intended CLI surface and should not be interpreted as already implemented unless a later release says otherwise.

## Documentation

Start here:

- [Architecture design](docs/superpowers/specs/2026-08-19-gpt-pluginos-design.md)
- [Operator handbook](docs/OPERATOR_HANDBOOK.md)
- [Extensive use cases](docs/USE_CASES.md)
- [Worked examples](docs/EXAMPLES.md)
- [Advanced patterns](docs/ADVANCED_PATTERNS.md)
- [Governance playbook](docs/GOVERNANCE_PLAYBOOK.md)
- [Benchmark playbook](docs/BENCHMARK_PLAYBOOK.md)
- [Ecosystem integrations](docs/ECOSYSTEM_INTEGRATIONS.md)
- [Implementation plan](docs/superpowers/plans/2026-08-19-operator-handbook-v1.md)

## Example contracts

Reference examples live in [`examples/`](examples/):

- `provider-cloudinary.yaml`
- `provider-product-design.yaml`
- `provider-google-calendar.yaml`
- `route-media-upscale.yaml`
- `route-product-audit.yaml`
- `workflow-creator-campaign.yaml`
- `workflow-code-release.yaml`

These examples are designed to become future compiler/test fixtures.

## Example: creator campaign

```text
market discovery
  -> Product Hunt / web
SEO intelligence
  -> Semrush
product/design direction
  -> Product Design
image generation
  -> provider selected per benchmark/policy
upscale
  -> Magnific / Cloudinary / local fallback
asset infrastructure
  -> Cloudinary
creative lineage
  -> Content Universe
brand/social adaptation
  -> Canva
schedule
  -> Google Calendar
publication
  -> explicit approval via SuperAgents
```

No single plugin owns the campaign.

## Example: engineering release

```text
repository inspection -> GitHub
change implementation -> controlled code-change route
tests -> local/runtime verification
security -> Codex Security
release -> GitHub
production deploy -> Vercel + deployment approval
milestone -> Google Calendar
```

Again, capability stages matter more than vendor categories.

## Planned CLI

```bash
pluginos scan
pluginos validate
pluginos compile
pluginos providers
pluginos capabilities
pluginos explain <capability>
pluginos route <capability>
pluginos overlaps
pluginos benchmark <suite>
pluginos lock
pluginos diff <lock-a> <lock-b>
pluginos graph --format mermaid
pluginos audit
```

JSON output is planned for agent consumption.

## Routing signals

PluginOS is designed to rank providers using signals such as:

- capability fit
- provider role
- installed/connected state
- health
- risk compatibility
- benchmark quality
- latency
- cost class
- provenance quality
- local-first preference
- privacy zone
- project overrides
- downstream output compatibility

No single weighted score is required. Multi-objective/Pareto routing is a first-class pattern.

## Governance

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

SuperAgents remains responsible for approval and execution policy.

## Lockfiles

A planned `pluginos.lock.json` captures the exact ecosystem projection used for a benchmark, audit, or production-sensitive decision:

- source repository revisions
- catalog hashes
- schema versions
- provider/capability counts
- graph hash
- benchmark snapshots

This lets future operators answer:

> “What provider ecosystem produced this route?”

## First-party providers

External SaaS providers are not privileged over local tools.

A repository such as `icho-reel-eng`, a tool inside `pythons`, or a workflow inside `n8n_workflows` can participate through a provider manifest and compete by capability.

That allows PluginOS to answer questions like:

> “Should this image operation use Cloudinary, Magnific, or one of my own local tools?”

## Provider maturity

A useful integration maturity model is:

```text
discovered
 -> declared
 -> normalized
 -> validated
 -> benchmarked
 -> routed
 -> executable
 -> provenance-complete
```

Being listed does not mean a provider is production-ready.

## Non-goals

GPT-PluginOS is not intended to:

- replace SuperAgents
- replace SuperSkills
- replace gpt-plugs
- store creative assets
- store credentials
- autonomously install/uninstall plugins
- silently broaden permissions
- execute destructive/financial/publication actions by itself
- become an unbounded universal agent runtime

## Roadmap

### Phase 0: foundation

Architecture, schemas, docs, tests, CI, changelog discipline.

### Phase 1: federated registry

Adapters for gpt-plugs, SuperSkills, SuperAgents, agent-skills, GitHub/repository providers, plugin inventory, and deterministic lockfiles.

### Phase 2: routing intelligence

Capability graph, overlap analysis, ranking, route explanations, SuperAgents projections.

### Phase 3: evaluation and health

Benchmark harnesses, health/lifecycle observations, canary/shadow providers, historical plugin migration mapping.

### Phase 4: creator/asset integration

Content Universe provenance, Cloudinary handoff, CreativeOS projections, ichoTaKu/reel/creator-provider manifests.

### Phase 5: operator surfaces

Generated ecosystem reports, graph views, dashboard, drift explorer, benchmark comparisons.

## Design philosophy

The system should make a sprawling AI tool ecosystem feel less like a drawer of adapters and more like a typed, queryable nervous system.

Every route should ultimately be able to answer:

1. What capability did we think was required?
2. Which providers were eligible?
3. Why was this one selected?
4. What policy changed the ranking?
5. What source/benchmark state supported the decision?
6. What approval was required?
7. Where did the resulting artifact or audit record go?

If PluginOS cannot explain those seven things, the control plane is not finished.
