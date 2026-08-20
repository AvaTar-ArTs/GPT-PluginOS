# GPT-PluginOS Operator Handbook

GPT-PluginOS is the federated capability control plane for the AvaTar-ArTs ecosystem. It answers four questions before any agent or workflow should act:

1. **What capability is actually required?**
2. **Which providers can satisfy it right now?**
3. **Which provider should be preferred under the current constraints?**
4. **What governance, provenance, and fallback rules apply?**

It does not replace the systems that actually own skills, execution, provider records, or creative artifacts.

- **SuperSkills** owns reusable capability contracts.
- **SuperAgents** owns orchestration, approvals, execution, verification, and runtime state.
- **gpt-plugs** owns governed plugin/provider/action records.
- **Content Universe** owns creative provenance, assets, and lineage.
- **GPT-PluginOS** compiles those sources into a discoverable, comparable, routable, and governable projection.

---

## 1. Mental model

Think of PluginOS as a compiler for an ecosystem of tools.

```text
intent
  -> capability requirements
  -> source observations
  -> normalized provider graph
  -> ranking and policy evaluation
  -> advisory route projection
  -> SuperAgents approval/execution
  -> result verification
  -> Content Universe provenance/lineage when applicable
```

The most important rule is:

> **Provider selection is not authorization.**

PluginOS may conclude that GitHub is the best provider for `code.repository.modify`, Stripe for `commerce.payment.manage`, or Cloudinary for `media.asset.transform`. That conclusion does not grant permission to change a repository, charge/refund a customer, or delete an asset.

---

## 2. Core entities

### Capability

A stable description of **what can be done**, independent of vendor.

Examples:

- `media.image.generate`
- `media.image.upscale`
- `media.asset.visual_search`
- `media.video.edit`
- `design.product.audit`
- `research.seo.keyword`
- `research.academic.search`
- `code.repository.modify`
- `deploy.web.publish`
- `schedule.event.create`

Capabilities should be small enough to route, benchmark, and govern independently.

### Provider

A plugin, API, local tool, repository, runtime, or service capable of satisfying one or more capabilities.

Examples:

- Cloudinary
- Product Design
- Google Calendar
- Semrush
- GitHub
- a local Python tool in `AvaTar-ArTs/pythons`
- a workflow exposed by `AvaTar-ArTs/n8n_workflows`

### Action

A provider-specific operation that may carry risk or approval requirements.

A provider can support both safe and dangerous actions. For example, an asset service might support `search`, `transform`, and `delete`. Routing must not flatten those into one generic permission level.

### Source observation

A timestamped fact imported from an authoritative source, such as a provider manifest, plugin directory entry, repository file, benchmark result, or health observation.

### Route projection

An advisory ranking of candidate providers for a capability under a defined policy context.

### Lockfile

A deterministic snapshot of the ecosystem projection used for a build, audit, comparison, or benchmark.

---

## 3. Provider lifecycle states

PluginOS treats availability as stateful rather than binary.

| State | Meaning | Routing implication |
|---|---|---|
| `discovered` | Known from a source but not necessarily available | Catalog only |
| `available` | Can be installed or invoked in principle | Candidate with penalty |
| `installed` | Installed in the current environment | Candidate |
| `connected` | Installed and authenticated/usable when observable | Strong candidate |
| `degraded` | Partially functional, unhealthy, rate-limited, or missing features | Fallback only unless explicitly allowed |
| `deprecated` | Supported but scheduled for retirement | Avoid for new workflows |
| `unavailable` | Cannot currently be used | Exclude |
| `legacy` | Historical integration generation | Research/migration only |
| `replaced` | Superseded by another provider or integration form | Route to successor |

A provider can also have different states per capability. A service may be healthy for image transforms while a video endpoint is degraded.

---

## 4. Daily operating cycle

The planned CLI is intentionally command-shaped around a simple operating loop.

> These commands describe the target interface from the architecture spec. They should not be read as proof that every command is implemented yet.

```bash
pluginos scan
pluginos validate
pluginos compile
pluginos audit
```

### Scan

Collect source observations from configured adapters.

Use when:

- plugins were installed or removed
- a source repository changed
- provider health may have changed
- a benchmark suite was refreshed
- a new specialist repository should be indexed

### Validate

Check schemas, canonical IDs, aliases, source references, and graph invariants.

Validation should fail on:

- unknown capability references
- duplicate canonical provider IDs
- ambiguous aliases
- missing provenance
- malformed risk declarations
- broken source revisions

### Compile

Build the normalized provider/capability graph and route projections.

Compilation can be degraded if a noncritical source is unavailable, but the output must explicitly record missing sources.

### Audit

Produce operator-facing findings:

- newly discovered providers
- disconnected installed providers
- overlapping capabilities
- stale benchmarks
- risky providers without policy classification
- legacy providers with known successors
- source drift since the last lockfile

---

## 5. Inspecting a capability

The most useful PluginOS question is not “what plugins do I have?” It is:

> “How can this capability be satisfied?”

Target CLI shape:

```bash
pluginos explain media.image.upscale
pluginos route media.image.upscale
```

A good explanation should include:

- capability definition
- authoritative source
- candidate providers
- installation/connection state
- capability-fit evidence
- benchmark freshness
- risk class
- cost/latency class
- ranking reason
- fallback chain
- policy blockers

Example conceptual result:

```text
Capability: media.image.upscale

1. Magnific
   role: premium specialist
   state: connected
   quality: high
   latency: medium
   risk: external_write
   reason: strongest specialist score for detail recovery

2. Cloudinary
   role: media infrastructure
   state: connected
   quality: medium-high
   latency: low
   risk: external_write
   reason: deterministic transformation path and strong provenance

3. Local ESRGAN adapter
   role: local fallback
   state: installed
   quality: medium
   latency: hardware-dependent
   risk: local_write
   reason: privacy-preserving offline fallback
```

No universal winner is implied. A privacy-sensitive project may invert the ranking.

---

## 6. Routing contexts

A route should always be evaluated inside a context.

Recommended context fields:

```yaml
project: ichotaku
capability: media.image.upscale
constraints:
  privacy: standard
  max_cost_class: medium
  max_latency_class: medium
  require_provenance: true
  external_write_allowed: true
preferences:
  specialist_first: true
  local_first: false
  preferred_providers:
    - magnific
```

Useful routing policies include:

- **specialist-first**: prefer the provider whose primary purpose matches the capability
- **local-first**: prefer local/private providers where quality is acceptable
- **cost-capped**: exclude providers above a project budget class
- **latency-capped**: optimize for interactive workflows
- **provenance-first**: prefer providers that return strong identifiers and metadata
- **reliability-first**: favor health and historical success over peak quality
- **human-approved-only**: exclude providers/actions lacking an explicit approval path

---

## 7. Multi-stage workflows

PluginOS should decompose workflows into capability stages rather than route the whole job to one monolithic provider.

Example creator campaign:

```text
research.market.trend
  -> Product Hunt / Semrush

design.product.ideate
  -> Product Design

media.image.generate
  -> selected generation provider

media.image.upscale
  -> Magnific

media.asset.register
  -> Cloudinary + Content Universe reference

media.transform.social
  -> Cloudinary / Canva

schedule.event.create
  -> Google Calendar

publication.prepare
  -> Canva / content tooling

publication.execute
  -> SuperAgents approval gate
```

Each stage can have a different provider, policy, benchmark, and risk class.

---

## 8. Approval boundaries

Recommended minimum governance matrix:

| Risk class | Default behavior |
|---|---|
| `read_only` | May be automatically selected and queried under policy |
| `external_write` | Require write-capable route and explicit execution policy |
| `destructive_write` | Require explicit human approval near action time |
| `financial` | Require explicit human approval and strong audit record |
| `identity_or_access` | Require explicit approval and least privilege |
| `publication` | Require final-content confirmation unless policy says otherwise |
| `code_change` | Route through repository workflow, tests, review policy |
| `deployment` | Require environment-aware deployment policy |

PluginOS records and explains these classes. SuperAgents enforces execution approval.

---

## 9. Onboarding a new provider

Use this checklist when adding any external plugin, MCP server, local tool, or specialist repository.

1. Assign a stable provider ID.
2. Record authoritative source and revision.
3. Identify exact capabilities, not marketing categories.
4. Split read, write, destructive, financial, publication, and deployment actions.
5. Record install/connection state separately.
6. Declare outputs and provenance support.
7. Identify aliases and possible canonical collisions.
8. Add initial role, such as `primary_media_infrastructure` or `seo_specialist`.
9. Add at least one degraded/fallback path for critical capabilities.
10. Add benchmark coverage if the provider overlaps another provider.
11. Compile a new graph and lockfile.
12. Review the diff before promoting new routing preferences.

---

## 10. Reviewing provider overlap

Overlap is not automatically waste.

Three providers for the same capability may be desirable when they occupy different positions:

```text
premium specialist
  + fast commodity provider
  + private local fallback
```

Overlap becomes harmful when providers have:

- indistinguishable roles
- no benchmark differentiation
- no project-specific need
- duplicate credentials or billing without a fallback purpose
- unclear routing precedence

Operator question:

> “What unique job does each provider own?”

If there is no answer, the provider is a candidate for de-prioritization or removal.

---

## 11. Degraded operation

PluginOS should fail loudly in metadata and gracefully in routing.

Example:

```text
Semrush adapter unavailable
  -> mark source observation stale
  -> retain last-known catalog with timestamp
  -> reduce route confidence
  -> recommend web/public fallback if allowed
  -> emit degraded compilation diagnostic
```

Never silently present stale data as current.

A degraded compile should report:

- missing source
- last successful observation
- affected capabilities
- candidate fallback providers
- confidence reduction

---

## 12. Debugging a bad route

When PluginOS selects the wrong provider, do not immediately hard-code a special case.

Debug in this order:

1. **Capability definition**: Was the intent normalized correctly?
2. **Provider metadata**: Does each candidate really support the capability?
3. **State**: Is install/connection/health current?
4. **Policy**: Did privacy, cost, risk, or latency constraints alter the route?
5. **Benchmark freshness**: Is the score stale or based on the wrong fixture family?
6. **Role priority**: Is a provider incorrectly marked primary?
7. **Alias resolution**: Did multiple records collapse incorrectly?
8. **Project override**: Is a local preference intentionally changing rank?

Only after those checks should routing weights change.

---

## 13. Lockfile discipline

`pluginos.lock.json` should make ecosystem decisions reproducible.

Use a lockfile before:

- a benchmark run
- a major content-production batch
- a release workflow
- a security audit
- comparing provider quality over time
- generating a published ecosystem report

The lock should capture:

- source repository commits
- source catalog hashes
- schema versions
- provider count
- capability count
- graph hash
- benchmark snapshot IDs
- generated timestamp

A lockfile answers:

> “What ecosystem did this decision come from?”

---

## 14. Drift review

A drift report should distinguish meaningful change from noise.

High-value drift:

- provider added/removed
- installed state changed
- capability added/removed
- risk classification changed
- source revision changed
- benchmark winner changed
- provider became degraded/deprecated/replaced
- alias changed canonical target

Low-value drift:

- description wording changed
- non-routing metadata changed
- timestamp-only refresh

Do not promote a new lockfile automatically when high-value drift is present.

---

## 15. Historical plugin migration

Legacy plugin datasets such as old `ai-plugin.json` directories belong in PluginOS as historical evidence, not current provider truth.

Useful migration edges:

```text
legacy ChatGPT plugin
  -> GPT Action
  -> app/connector
  -> modern plugin package
  -> MCP or provider successor
```

This enables research such as:

- which old integrations survived
- which vendors migrated platforms
- which capabilities disappeared
- which plugin categories became native features
- what architectural patterns proved durable

---

## 16. Operator review cadence

### Per change

- validate affected manifests
- inspect route diffs
- check risk changes
- update changelog when behavior changes

### Weekly or before major production

- refresh provider state
- inspect degraded providers
- review stale benchmarks
- review overlap matrix
- regenerate lockfile

### Monthly or ecosystem milestone

- audit aliases/canonical IDs
- refresh specialist repository manifests
- review legacy/replaced mappings
- reassess provider roles
- archive obsolete benchmark snapshots

---

## 17. What PluginOS should never do silently

PluginOS must not silently:

- install or uninstall providers
- broaden permissions
- execute destructive actions
- make purchases or refunds
- publish content
- deploy production code
- rewrite authoritative IDs
- discard provenance
- replace source catalogs with generated projections
- treat a stale benchmark as permanent truth

Its job is to make the decision surface explicit enough that SuperAgents and humans can act safely and intelligently.
