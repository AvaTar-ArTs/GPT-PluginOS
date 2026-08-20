# GPT-PluginOS Federated Architecture Design

Date: 2026-08-19
Status: Design approved in conversation; implementation pending plan review
Owner: AvaTar-ArTs

## 1. Purpose

GPT-PluginOS is the federated capability control plane for the AvaTar-ArTs AI ecosystem.

It does not replace SuperAgents, SuperSkills, agent-skills, gpt-plugs, Content Universe, CreativeOS, or specialist production systems. It indexes and compiles their capabilities into a coherent provider graph, then exposes normalized routing, governance, benchmarking, health, and interoperability views.

The operating idea is simple:

> External plugins and internal tools are providers. Skills define capabilities. Agents orchestrate. Content Universe records provenance and lineage. GPT-PluginOS makes the whole system discoverable, comparable, routable, and governable.

## 2. Existing ecosystem boundaries

### SuperSkills

Canonical source for reusable skill/capability contracts, lifecycle metadata, risk classification, tags, and provenance.

GPT-PluginOS consumes SuperSkills definitions. It does not rewrite them.

### SuperAgents

Canonical source for agent manifests, routing behavior, execution envelopes, approval boundaries, adapters, verification, and audit semantics.

GPT-PluginOS emits provider/capability projections that SuperAgents can route against. It does not become the executor.

### agent-skills

Broader source ecosystem for experimental, long-form, specialist, and domain skills.

GPT-PluginOS indexes compatible skill metadata and may recommend promotion into SuperSkills, but does not make agent-skills non-authoritative for its own content.

### gpt-plugs

Canonical governed registry for external plugin/provider definitions, action risk, permissions, dependencies, provenance, lifecycle, and provider-level evaluation metadata.

GPT-PluginOS treats gpt-plugs as a first-class provider source. Existing plugin/action/provenance schemas should be reused or versioned upward rather than reimplemented incompatibly.

### Content Universe

Canonical creative provenance, recovery, catalog, graph, asset lineage, and project/entity substrate.

GPT-PluginOS records execution/provider observations and output references into Content Universe-compatible provenance envelopes where applicable, but does not store creative assets itself.

### CreativeOS

Provider-neutral creative authoring, workflow, routing, evaluation, and approval runtime above Content Universe.

GPT-PluginOS supplies provider intelligence and capability resolution to CreativeOS, especially for media, design, research, publishing, and transformation providers.

### Specialist systems

Repositories such as icho-reel-eng, creator-camp, my-creators, pythons, n8n_workflows, ToolUniverse, notebooklm integrations, and production-specific compilers remain specialist capability providers or consumers.

GPT-PluginOS indexes them through adapters and manifests instead of absorbing them.

## 3. Chosen architecture

### Approach A: Monolithic PluginOS

One repository contains plugin schemas, agent routing, skill definitions, provider execution, asset provenance, benchmarking, UI, and persistence.

Rejected because it duplicates mature subsystem boundaries, increases coupling, creates competing sources of truth, and would eventually turn into an ecosystem-sized merge conflict.

### Approach B: Thin catalog/dashboard

PluginOS only lists installed plugins and produces documentation.

Rejected because it cannot resolve provider overlap, generate routing projections, enforce governance, benchmark providers, or create machine-readable interoperability.

### Approach C: Federated capability control plane

Chosen.

GPT-PluginOS owns normalized indexing, graph compilation, provider comparison, routing projections, health/evaluation summaries, ecosystem lockfiles, and governance views. Authoritative definitions remain in their source repositories.

This makes PluginOS a compiler/control plane rather than another content warehouse or execution engine.

## 4. Core architecture

```text
                       GPT-PluginOS
                           |
        +------------------+------------------+
        |                  |                  |
     discovery          compiler          governance
        |                  |                  |
   source adapters    capability graph    risk/health
        |             provider graph      permissions
        |             route projections   lifecycle
        |                  |                  |
  +-----+------+-----------+----------+-------+------+
  |            |                      |              |
SuperSkills  gpt-plugs              SuperAgents  Content Universe
capability   provider/action        execution    provenance/lineage
contracts    registry               runtime      substrate
  |            |                      |              |
  +------------+----------+-----------+--------------+
                         |
                 specialist systems
      media / code / research / design / publishing
```

## 5. Major subsystems

### 5.1 Source adapters

Purpose: discover and normalize metadata from ecosystem sources.

Initial adapters:

- ChatGPT/OpenAI plugin inventory
- gpt-plugs catalogs/manifests
- SuperSkills catalog
- SuperAgents manifests
- agent-skills catalog/index
- GitHub repository metadata
- Content Universe provider/entity references
- optional MCP registry sources
- optional legacy ai-plugin.json datasets such as Awesome-Plugins for historical analysis

Each adapter emits immutable source observations plus a normalized projection.

No adapter may mutate the authoritative source by default.

### 5.2 Capability ontology

Capabilities use dotted stable identifiers, for example:

- `media.image.generate`
- `media.image.upscale`
- `media.asset.visual_search`
- `media.video.edit`
- `design.product.audit`
- `design.prototype.generate`
- `research.academic.search`
- `research.seo.keyword`
- `code.repository.modify`
- `deploy.web.publish`
- `schedule.event.create`
- `commerce.payment.manage`

Capabilities represent what can be done, not which product does it.

SuperSkills remains authoritative when a matching reusable capability contract exists.

### 5.3 Provider registry projection

Each provider receives a normalized record:

```yaml
id: cloudinary
kind: plugin
source: gpt-plugs
status: installed
roles:
  - primary_media_infrastructure
capabilities:
  - media.asset.upload
  - media.asset.search
  - media.asset.visual_search
  - media.asset.relate
  - media.transform.image
  - media.transform.video
  - media.delivery.cdn
risk:
  writes_external_state: true
  destructive_actions: true
health:
  availability: unknown
benchmarks: []
```

Provider records must distinguish:

- installed versus merely known
- connected versus unconnected when observable
- read versus write actions
- destructive actions
- local versus remote provider
- first-party versus third-party
- authoritative source versus inferred metadata
- current plugin generation versus legacy integration

### 5.4 Capability graph

The compiler creates graph edges among:

- capability -> providers
- skill -> capabilities
- agent -> required capabilities
- workflow -> capabilities
- provider -> actions
- provider -> dependencies
- provider -> outputs
- provider -> permission/risk classes
- provider -> ecosystem repositories
- output -> provenance sink

The graph must be serializable to JSON and optionally Mermaid/DOT.

### 5.5 Provider ranking and routing projections

PluginOS does not execute provider calls in v1.

It computes ranked candidates using configurable weighted signals:

- explicit role priority
- capability fit
- installed/connected state
- permission/risk compatibility
- benchmark scores
- health/availability
- cost class
- latency class
- output quality
- provenance quality
- local-first preference
- user/project override

Example projection:

```yaml
capability: media.image.upscale
providers:
  - id: magnific
    rank: 1
    reason: preferred specialist; high quality
  - id: cloudinary
    rank: 2
    reason: infrastructure transformation path
```

SuperAgents may consume these projections as advisory routing inputs.

### 5.6 Governance and permission model

The system records governance metadata but does not silently broaden permissions.

Risk classes:

- `read_only`
- `external_write`
- `destructive_write`
- `financial`
- `identity_or_access`
- `publication`
- `code_change`
- `deployment`

Each provider/action can declare approval expectations and provenance requirements.

Selection never implies authorization.

### 5.7 Benchmarks and evaluations

Overlapping providers are evaluated per capability, never through a single global winner.

Initial benchmark families:

#### Image/media

- generation quality
- prompt adherence
- character consistency
- typography accuracy
- editing fidelity
- upscaling/detail recovery
- latency
- cost
- metadata/provenance quality

#### Presentation

- structural quality
- visual hierarchy
- editable output
- source grounding
- export fidelity
- iteration ergonomics

#### Research

- source quality
- citation completeness
- freshness
- factual accuracy
- recall
- structured output usefulness

#### Development

- correctness
- diff quality
- test behavior
- security findings
- reproducibility

Benchmark results are versioned observations, not permanent truth.

### 5.8 Health and lifecycle

Lifecycle states:

- discovered
- available
- installed
- connected
- degraded
- deprecated
- unavailable
- legacy
- replaced

Historical plugin datasets may additionally track migration relationships:

`legacy_plugin -> GPT/action/app/plugin/MCP successor`

### 5.9 Ecosystem lockfile

PluginOS generates a deterministic lockfile describing the exact ecosystem projection used for a build or benchmark.

Suggested file: `pluginos.lock.json`

Fields:

- generated timestamp
- source repository refs/commits
- catalog hashes
- schema versions
- provider count
- capability count
- graph hash
- benchmark snapshot IDs

This extends the lockfile/hash discipline already introduced across SuperAgents/SuperSkills.

### 5.10 Provenance envelope

Every compiled observation should preserve:

- source
- source locator
- observed timestamp
- source revision when known
- confidence
- normalization version
- transformation history

Execution results are outside PluginOS v1, but when later integrated they should emit Content Universe-compatible provenance references.

## 6. Repository structure

```text
GPT-PluginOS/
  README.md
  CHANGELOG.md
  LICENSE
  pyproject.toml
  pluginos.toml

  docs/
    architecture.md
    ecosystem-map.md
    capability-ontology.md
    provider-model.md
    governance.md
    benchmarking.md
    integrations/
    superpowers/specs/

  schemas/
    capability.schema.json
    provider.schema.json
    action-ref.schema.json
    source-observation.schema.json
    route-projection.schema.json
    benchmark.schema.json
    lockfile.schema.json

  catalog/
    capabilities/
    roles/
    aliases/

  adapters/
    gpt_plugs/
    superskills/
    superagents/
    agent_skills/
    github/
    openai_plugins/
    content_universe/
    legacy_plugins/

  pluginos/
    models/
    ingest/
    normalize/
    graph/
    rank/
    evaluate/
    provenance/
    lockfile/
    cli/

  tests/
    fixtures/
    contract/
    unit/
    integration/

  scripts/
    validate_catalog.py
    compile_registry.py
    build_lockfile.py
    audit_ecosystem.py

  .github/workflows/
    validate.yml
    changelog.yml
    ecosystem-drift.yml
```

## 7. CLI surface

Initial commands:

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

Commands should support JSON output for agent consumption.

## 8. Integration contracts

### With gpt-plugs

PluginOS imports provider/action/provenance definitions and reuses stable IDs.

No duplicated plugin master records.

### With SuperSkills

PluginOS links capability IDs to canonical skill IDs and source commit hashes.

### With SuperAgents

PluginOS exports advisory route projections and provider health/evaluation metadata. SuperAgents remains responsible for approvals and execution.

### With Content Universe

PluginOS can export provider/provenance observations as references. Creative outputs remain Content Universe entities/assets, not PluginOS records.

### With specialist repositories

Repositories may opt in through a lightweight `pluginos-provider.yaml` manifest declaring:

- stable provider ID
- repository
- capabilities
- interfaces
- runtime requirements
- risk classes
- outputs
- provenance support

## 9. Data integrity rules

1. Every normalized record preserves source provenance.
2. Authoritative source IDs are never silently rewritten.
3. Inferred data is explicitly marked inferred.
4. Duplicate provider aliases resolve to one canonical ID plus aliases.
5. Provider health and evaluation are timestamped observations.
6. Capability IDs are stable and versioned through schema/catalog changes.
7. Lockfiles include source revisions and hashes.
8. Destructive/write capability metadata never implies permission to execute.
9. PluginOS does not store credentials or OAuth tokens.
10. Generated projections are disposable; source catalogs remain authoritative.

## 10. Error handling

Adapters fail independently.

A failed source should create a structured diagnostic containing:

- source ID
- failure type
- retryability
- last successful observation
- affected projection domains

Compilation may proceed in degraded mode only when the output explicitly lists missing sources.

Schema violations fail validation and CI.

Conflicting canonical IDs fail compilation until resolved by alias or precedence policy.

## 11. Testing strategy

### Contract tests

Validate every schema and source adapter fixture.

### Golden projection tests

Known source fixtures must compile to stable normalized outputs.

### Graph invariant tests

Examples:

- every provider capability references an existing capability ID
- every ranked provider exists
- every alias resolves exactly once
- every observation has provenance
- graph output is deterministic for a fixed lockfile

### Ranking tests

Use fixed synthetic providers to prove changes in risk, health, benchmarks, and priority affect rank predictably.

### Integration tests

Test read-only ingestion from pinned fixtures representing gpt-plugs, SuperSkills, SuperAgents, and selected repository manifests.

### Drift tests

CI compares newly compiled graph hashes and catalog diffs against the committed lockfile and reports ecosystem changes.

## 12. Security model

- read-only ingestion by default
- no credential persistence
- no autonomous external writes in v1
- explicit source allowlists for remote ingestion
- validation of untrusted manifest content
- bounded file/path handling
- provenance retained for all imported metadata
- write/destructive actions classified but not executed
- later execution integration must pass through SuperAgents approval policy

## 13. Initial provider roles from current plugin audit

These are starting roles, not permanent rankings.

- Product Design: product discovery, UX research/audit, visual exploration, prototype validation
- Figma: canonical editable product design and design-system handoff
- Canva: marketing/brand/social production
- Cloudinary: primary media asset infrastructure, transformation, delivery, visual search, relationships
- Magnific: premium image enhancement/upscale/relight
- Morphix: multimodal generation provider
- Picsart: graphics/media generation and editing
- Deep Art AI: experimental image/video generation provider
- HeyGen: avatar/talking-video/localization provider
- Descript: transcript-based editorial video provider
- HyperFrames: programmable HTML/video composition provider
- Sider Scholar: academic research provider
- Semrush: SEO/competitive data provider
- Product Hunt: product/market discovery signal
- GitHub: source-code/repository provider
- Codex Security: security analysis provider
- OpenAI Developers: OpenAI app/agent/API development provider
- Supabase: backend/database/auth provider
- Vercel: deployment/hosting provider
- Gmail: email provider
- Google Drive: document/file provider
- Google Calendar: temporal orchestration provider
- Slack: team communication provider
- Notion: knowledge/project documentation provider
- Airtable: structured operational data provider
- Stripe: commerce/payment provider

## 14. Phased delivery

### Phase 0: foundation

- repository standards
- architecture docs
- schemas
- test harness
- changelog discipline
- CI

### Phase 1: federated registry

- gpt-plugs adapter
- SuperSkills adapter
- SuperAgents adapter
- agent-skills adapter
- GitHub repository adapter
- normalized provider and capability catalog
- lockfile compiler

### Phase 2: routing intelligence

- capability graph
- overlap matrix
- ranking engine
- route explanation
- SuperAgents projection export

### Phase 3: evaluation and health

- benchmark schema/harness
- capability-specific provider benchmarks
- lifecycle/health observations
- historical plugin migration mapping

### Phase 4: creative and asset integration

- Content Universe provenance export
- CreativeOS provider projection
- Cloudinary/content-universe asset handoff contracts
- icho-reel-eng and creator tooling manifests

### Phase 5: operator surfaces

- static generated ecosystem report
- optional local web dashboard
- graph visualization
- diff views
- audit reports

The UI is deliberately deferred until the data contracts and compiler are trustworthy.

## 15. Non-goals for v1

- becoming a universal autonomous agent runtime
- replacing SuperAgents execution
- replacing SuperSkills definitions
- replacing gpt-plugs provider records
- storing creative assets
- storing credentials
- silently installing/uninstalling plugins
- autonomous purchases, publications, deployments, or destructive writes
- building a full SaaS backend before local deterministic compilation works

## 16. Success criteria

GPT-PluginOS v1 is successful when:

1. One command can ingest pinned ecosystem sources and compile a deterministic provider/capability graph.
2. The graph can answer which providers satisfy a requested capability and why one ranks above another.
3. Overlapping providers can be detected automatically.
4. Every normalized record retains provenance.
5. A lockfile can reproduce the exact ecosystem projection.
6. CI detects schema errors, broken references, and ecosystem drift.
7. SuperAgents can consume a generated routing projection without adopting PluginOS internals.
8. Content Universe can receive provenance references without PluginOS becoming an asset database.
9. Adding a new provider requires a manifest/adapter, not edits across the whole runtime.
10. Existing repositories remain authoritative for their own domains.

## 17. Immediate implementation plan boundary

The first implementation plan should cover only Phase 0 and Phase 1 plus a narrow end-to-end vertical slice:

`gpt-plugs + SuperSkills -> normalize -> capability graph -> route explanation -> lockfile`

Do not attempt the benchmark dashboard, live plugin execution, Content Universe writes, or every ecosystem adapter in the first implementation cycle.

That vertical slice is sufficient to prove the architecture while keeping the initial build testable and reversible.
