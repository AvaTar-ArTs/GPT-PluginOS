# GPT-PluginOS Ecosystem Integration Guide

GPT-PluginOS is intentionally federated. This guide defines what each surrounding repository owns, what PluginOS consumes, what it may emit, and what it must never duplicate.

## 1. Source-of-truth map

| Repository/system | Canonical ownership | PluginOS role |
|---|---|---|
| `superSkills` | reusable capability/skill contracts | consume and index |
| `superAgents` | orchestration, approvals, execution, verification | emit advisory routing projections |
| `agent-skills` | experimental/long-form/specialist skills | index, evaluate, recommend promotion |
| `gpt-plugs` | governed external provider/action registry | consume as primary provider source |
| `content-universe` | creative entities, assets, provenance, lineage | emit compatible provider/provenance references |
| `CreativeOS` direction | creative authoring/workflow/runtime semantics | supply provider intelligence |
| `icho-reel-eng` | specialist reel/video production | index as first-party provider |
| `pythons` | first-party automation/tool implementations | index selected tools as providers |
| `n8n_workflows` | workflow automations | index selected workflows as providers |
| `creator-camp` | creator education/publishing/business workflows | consume PluginOS intelligence where useful |
| `my-creators` | creator production tooling | index compatible capabilities |

---

## 2. SuperSkills integration

SuperSkills defines **what a reusable capability means**.

PluginOS should import:

- stable skill ID
- capability tags/IDs
- lifecycle state
- risk metadata
- source revision
- provenance metadata

PluginOS should emit:

- providers capable of satisfying linked capabilities
- health/evaluation observations
- overlap/gap findings

PluginOS must not:

- fork canonical skill definitions
- rewrite SuperSkills IDs
- silently promote experimental skills

### Promotion flow

```text
agent-skills
  experimental skill
      ↓
evaluation / stabilization
      ↓
superSkills
  canonical reusable contract
      ↓
PluginOS recompile
      ↓
provider graph + SuperAgents route projection
```

---

## 3. SuperAgents integration

SuperAgents owns:

- agent identities/manifests
- execution envelopes
- approval policy
- provider adapters/execution
- verification
- audit events

PluginOS supplies advisory data:

```yaml
capability: media.image.upscale
ranked_providers:
  - magnific
  - cloudinary
route_confidence: 0.91
policy_notes:
  - external_write
  - provenance_required
```

SuperAgents decides whether and how the provider is actually invoked.

### Important boundary

A PluginOS route is **advisory until accepted by SuperAgents policy and an execution adapter**.

---

## 4. gpt-plugs integration

gpt-plugs already defines the governed provider control layer for external plugins.

PluginOS should reuse:

- provider/plugin IDs
- action records
- provenance records
- permissions/risk metadata
- dependencies
- lifecycle/evaluation metadata

PluginOS may enrich its projection with:

- capability normalization
- cross-provider overlap
- routing scores
- benchmark observations
- install/connection observations
- aliases/successor relationships

Do not create a competing provider master record in PluginOS.

---

## 5. Content Universe integration

Content Universe is the durable creative graph.

PluginOS should not store image/video/audio assets.

When a routed workflow produces creative outputs, the later execution layer can emit a Content Universe-compatible envelope such as:

```yaml
provider:
  id: magnific
  capability: media.image.upscale
route:
  projection_id: route-2026-08-19-001
  lockfile_hash: sha256:...
input:
  content_universe_entity: image:character-ref-001
output:
  cloudinary_asset_id: abc123
provenance:
  observed_at: 2026-08-19T23:00:00-04:00
  source_provider: magnific
```

This preserves why/how an asset was created without making PluginOS the asset database.

---

## 6. Cloudinary + Content Universe handoff

Recommended division:

```text
Cloudinary
  physical media asset
  delivery URLs
  transforms
  technical metadata
  visual search
        ↓ reference
Content Universe
  semantic identity
  canon
  project/series/character
  prompt lineage
  creative relationships
  provenance graph
```

Example:

```text
Cloudinary asset_id = 9f...
Content Universe entity = image:ichotaku-cover-037
relationship = stored_as
```

Neither system needs to duplicate the other's entire record.

---

## 7. First-party repository provider manifest

Specialist repositories may opt in with `pluginos-provider.yaml`.

Recommended shape:

```yaml
id: icho-reel-eng
kind: repository_provider
source:
  repository: AvaTar-ArTs/icho-reel-eng
  ref: <commit>
capabilities:
  - creator.reel.compile
  - media.video.compose
interfaces:
  - cli
runtime:
  mode: local
risk:
  - local_write
outputs:
  - video
  - manifest
provenance:
  supported: true
```

PluginOS should validate but not mutate this manifest by default.

---

## 8. `pythons` integration

Do not register the entire repository as one giant provider if it contains many unrelated tools.

Prefer either:

```text
provider: pythons/image-renamer
provider: pythons/asset-indexer
provider: pythons/video-tool
```

or a parent provider with explicit child tools.

Each promoted tool should declare:

- stable ID
- entrypoint
- required runtime
- input/output artifact classes
- capabilities
- write behavior
- deterministic/non-deterministic behavior
- provenance support

This makes local Python tools first-class alternatives to SaaS plugins without pretending they are all equivalent.

---

## 9. `n8n_workflows` integration

A workflow is a provider when it exposes a stable capability contract.

Example:

```yaml
id: n8n/publish-asset-bundle
kind: workflow_provider
capabilities:
  - publication.asset_bundle.distribute
risk:
  - publication
inputs:
  - asset_manifest
outputs:
  - publication_receipt
```

PluginOS routes to the workflow. SuperAgents/execution policy controls whether the workflow runs.

---

## 10. `icho-reel-eng` integration

Treat the reel engine as a specialist provider, not a generic video editor.

Potential capabilities:

- `creator.reel.compile`
- `media.asset.sequence`
- `media.video.compose`
- `creator.timeline.generate`

Upstream:

- Content Universe asset query
- Cloudinary asset retrieval/transforms
- campaign/character manifests

Downstream:

- HyperFrames/Remotion-like renderers where appropriate
- Cloudinary delivery
- publication workflow

---

## 11. Creator ecosystem integration

Repositories such as `creator-camp` and `my-creators` may consume PluginOS for:

- provider recommendations by capability
- creator workflow templates
- content production routing
- publishing provider selection
- market/research provider selection
- cost/privacy policies

They should not need to know the entire external plugin inventory.

They ask PluginOS for a capability route.

---

## 12. Repository source pinning

Every imported repository source should record a revision.

```yaml
source:
  repository: AvaTar-ArTs/superSkills
  commit: abcdef123456
```

PluginOS compilation should be explainable against exact refs.

Avoid importing mutable `main` as if it were a reproducible source state in lockfiles.

---

## 13. Catalog hashes

When a source contains multiple manifests, store a deterministic catalog hash in the lockfile.

Recommended process:

1. canonical sort
2. normalize line endings/serialization
3. hash relevant files
4. record source commit + aggregate hash

This distinguishes repository movement from catalog-semantic changes.

---

## 14. Ecosystem drift

Drift categories:

- source commit changed
- catalog hash changed
- schema version changed
- provider count changed
- capability count changed
- action risk changed
- route winner changed
- provider lifecycle changed

High-risk drift should block automatic lockfile promotion.

---

## 15. Cross-repo changelog discipline

If a change modifies an interface consumed by another repository:

- update source repo changelog
- update schema version if contract changed
- update PluginOS adapter/fixture
- regenerate lockfile
- record compatibility note in PluginOS changelog

This is especially important for SuperSkills, SuperAgents, gpt-plugs, and Content Universe interfaces.

---

## 16. Adapter rules

An adapter has one job: convert source truth into normalized observations.

Adapter output should contain:

- source ID
- source revision
- source locator
- raw/stable identity
- normalized provider/capability projection
- confidence
- normalization version
- diagnostics

Adapters should not:

- execute provider actions
- modify source repositories
- hide schema errors
- guess ambiguous canonical identities

---

## 17. OpenAI/ChatGPT plugin inventory

Live plugin inventory is an observation source, not the canonical provider definition source.

Useful observations:

- known
- available
- installed
- connected when observable
- disabled/unavailable
- plugin ID/name

Join this against gpt-plugs/provider metadata by stable ID or explicit alias evidence.

---

## 18. Legacy plugin datasets

Repositories such as `targed/Awesome-Plugins` belong under a historical adapter.

Store:

- legacy manifest URL
- historical health
- old plugin name/vendor
- capability inference with confidence
- successor edges when verified

Never let a live-but-legacy endpoint automatically outrank current plugins.

---

## 19. Integration maturity levels

Suggested scale:

### Level 0: discovered
Repository/provider known only by metadata.

### Level 1: declared
Provider manifest exists.

### Level 2: normalized
Capabilities map into PluginOS ontology.

### Level 3: validated
Schema/graph invariants pass.

### Level 4: benchmarked
Overlapping capabilities have evaluation data.

### Level 5: routed
Provider participates in advisory routing.

### Level 6: executable
SuperAgents has a compatible adapter and approval policy.

### Level 7: provenance-complete
Execution outputs preserve end-to-end provenance/lineage.

This prevents “listed in the registry” from being confused with “safe and ready to execute.”

---

## 20. Target end-state

The ecosystem should eventually behave like this:

```text
user / workflow / agent
        ↓
required capability
        ↓
GPT-PluginOS
  current provider graph
  project policy
  benchmark evidence
  risk/governance
        ↓
advisory route
        ↓
SuperAgents
  approval
  adapter
  execution
  verification
        ↓
provider / local tool / workflow
        ↓
result
        ↓
Content Universe / repository / operational system
        ↓
provenance + audit
```

Each repository stays excellent at one job. PluginOS is the connective intelligence between them.
