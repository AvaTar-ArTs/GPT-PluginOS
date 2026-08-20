# GPT-PluginOS Worked Examples

These examples are intentionally concrete. They illustrate the target contracts from the architecture spec so future compiler/runtime work has realistic fixtures to grow into.

> **Important:** the YAML files in `examples/` are reference contracts, not proof that the full PluginOS runtime already consumes every field.

---

## 1. Provider manifest: Cloudinary

See `examples/provider-cloudinary.yaml`.

This example demonstrates an **infrastructure provider** rather than a single-purpose generation provider. It owns several related capabilities:

- asset upload and storage
- search and visual search
- metadata and relations
- image/video transformation
- CDN delivery

The important modeling choice is action-level risk. Search is read-only, upload/update is external-write, and deletion is destructive-write. PluginOS should never collapse these into one provider-level permission bit.

---

## 2. Provider manifest: Product Design

See `examples/provider-product-design.yaml`.

This is a **specialist product-discovery provider**. Its role is intentionally upstream of Figma/GitHub implementation:

```text
problem / idea
  -> UX research
  -> flow audit
  -> visual exploration
  -> prototype target
  -> design QA
  -> handoff
```

A workflow should not route “create a marketing banner” here simply because it is a design plugin. Capability fit matters more than category labels.

---

## 3. Provider manifest: Google Calendar

See `examples/provider-google-calendar.yaml`.

This models Calendar as the temporal orchestration provider. It should be used for capabilities such as availability and event creation, not as a general task-management database.

---

## 4. Route example: image upscaling

See `examples/route-media-upscale.yaml`.

The route shows how three providers can coexist:

1. Magnific as premium specialist
2. Cloudinary as deterministic infrastructure fallback
3. a local provider as privacy/offline fallback

The route changes when policy changes. A `local_first: true` project may rank the local provider first even if quality is lower.

---

## 5. Route example: product audit

See `examples/route-product-audit.yaml`.

Product Design wins because its primary role and evidence workflow fit `design.product.audit`. Figma may still participate downstream, but it should not outrank a more specific provider just because Figma is a major design system.

---

## 6. Workflow example: creator campaign

See `examples/workflow-creator-campaign.yaml`.

This example demonstrates the core PluginOS philosophy: **a workflow is a chain of capabilities, not a chain of vendor names.**

The stages are:

```text
market discovery
  -> SEO research
  -> product/design ideation
  -> image generation
  -> upscale
  -> asset registration
  -> branded composition
  -> schedule
  -> publication preparation
```

Every stage declares:

- capability
- routing policy
- preferred role/provider if any
- risk class
- approval expectation
- provenance handoff

Publication is prepared but not executed automatically.

---

## 7. Workflow example: code release

See `examples/workflow-code-release.yaml`.

This workflow models a release as separate capabilities:

```text
repository read
  -> implementation/change
  -> tests
  -> security scan
  -> release preparation
  -> deployment
  -> calendar milestone
```

Code change and deployment have distinct risk classes and should not be merged into a single “engineering allowed” permission.

---

## 8. Example routing explanation

A future `pluginos explain` response might look like:

```yaml
capability: media.image.upscale
selected: magnific
confidence: 0.91
reasons:
  - provider is connected
  - provider role is premium_image_processing
  - benchmark image-upscale-v3 score is highest on detail recovery
  - project allows external writes
  - estimated cost class is within policy
fallbacks:
  - cloudinary
  - local-esrgan
warnings:
  - benchmark snapshot is 19 days old
```

An agent should be able to consume the JSON form, while a human can read an explanation like:

> Magnific ranks first because this project prioritizes output quality over latency and allows medium-cost external processing. Cloudinary is a lower-cost deterministic fallback. The local provider is available if privacy policy changes.

---

## 9. Example degraded route

```yaml
capability: research.seo.keyword
status: degraded
selected: web-research
missing_preferred_provider:
  id: semrush
  state: degraded
  last_successful_observation: 2026-08-18T15:20:00Z
confidence: 0.58
warnings:
  - structured keyword metrics may be unavailable
  - fallback output must not invent search volume
```

The key behavior is epistemic honesty. A fallback that cannot produce equivalent metrics must say so.

---

## 10. Example policy override

Default:

```yaml
policy:
  specialist_first: true
  local_first: false
```

Privacy-sensitive project:

```yaml
policy:
  specialist_first: false
  local_first: true
  external_processing: denied
```

The capability stays the same. The route changes.

---

## 11. Example capability alias

Different sources may call the same thing by different names:

```yaml
canonical: media.asset.visual_search
aliases:
  - image_similarity_search
  - visual_asset_lookup
  - similar_image_search
```

Aliases help normalize source vocabularies, but exactly one canonical ID must win. Ambiguous aliases should fail compilation.

---

## 12. Example provider successor mapping

```yaml
provider: legacy-webpilot-plugin
lifecycle: replaced
successor:
  provider: modern-web-research-provider
  relationship: capability_successor
  evidence:
    - source: vendor-docs
      observed_at: 2026-08-19T00:00:00Z
```

This pattern is useful for old ChatGPT plugin datasets and migration research.

---

## 13. Example specialist repository manifest

A first-party repository can participate without pretending to be a marketplace plugin:

```yaml
id: icho-reel-eng
kind: repository_provider
source:
  repository: AvaTar-ArTs/icho-reel-eng
capabilities:
  - media.video.compose
  - media.asset.sequence
  - creator.reel.compile
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

This is one of the most important PluginOS ideas: **your own tools compete in the same capability graph as external providers.**

---

## 14. Example project policy profile

```yaml
id: ichotaku-production
preferences:
  provenance_first: true
  specialist_first: true
  local_first: false
constraints:
  max_cost_class: medium
  destructive_write: deny
  publication: approval_required
  deployment: approval_required
provider_preferences:
  media.asset.infrastructure:
    - cloudinary
  media.image.upscale:
    - magnific
  design.product:
    - product-design
```

Project policy can influence routes without changing global provider records.

---

## 15. Example lockfile purpose

A future lockfile might capture:

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-08-19T23:00:00-04:00",
  "sources": {
    "gpt-plugs": "<commit>",
    "superSkills": "<commit>",
    "superAgents": "<commit>"
  },
  "providers": 37,
  "capabilities": 112,
  "graph_hash": "sha256:...",
  "benchmark_snapshots": ["image-upscale-v3", "research-seo-v2"]
}
```

The value is not the counts. The value is reproducibility: the system can later explain which catalog and benchmark state produced a route.
