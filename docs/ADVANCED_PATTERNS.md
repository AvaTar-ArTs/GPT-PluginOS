# GPT-PluginOS Advanced Patterns

This document covers patterns that become useful once the basic capability/provider registry is trustworthy.

## 1. Provider ensembles

A provider ensemble is a deliberate set of providers for the same capability, each with a distinct role.

```text
media.image.upscale
  ├── Magnific      premium specialist
  ├── Cloudinary    infrastructure transform
  └── local-esrgan  private/offline fallback
```

Use an ensemble when quality, latency, privacy, cost, or resilience differ meaningfully.

Do not create an ensemble simply because several providers exist.

### Recommended role dimensions

- premium specialist
- fast interactive
- deterministic infrastructure
- local/private
- low-cost batch
- experimental/canary
- legacy compatibility

---

## 2. Specialist-first routing

Prefer a provider when the requested capability is one of its core strengths.

Example:

```text
design.product.audit
  Product Design > Figma > generic visual analysis
```

This avoids category-level routing such as “all design tasks go to Canva.”

Specialist-first is a preference, not an absolute rule. A disconnected specialist loses to a connected fallback.

---

## 3. Local-first routing

For sensitive or high-volume workloads, local tooling can be ranked above SaaS providers.

```yaml
policy:
  local_first: true
  external_processing: denied
  minimum_quality_score: 0.70
```

A local-first policy should still expose the quality tradeoff rather than pretending the local option is objectively superior.

---

## 4. Privacy zones

Classify workflows by where data may travel.

Suggested zones:

- `public`: public data may use any approved provider
- `workspace`: connected workspace data may use approved authenticated providers
- `sensitive`: only explicitly allowlisted providers
- `local_only`: no external processing

Providers declare compatible zones. Routes filter before ranking.

---

## 5. Cost ceilings

Route policies can reject otherwise high-quality providers when they exceed a project cost class.

```yaml
constraints:
  max_cost_class: low
```

Avoid hard-coding dollar values into capability contracts. Price observations change faster than capability semantics.

Use timestamped cost observations and project-level ceilings.

---

## 6. Latency-aware routing

Interactive tasks and batch production have different priorities.

Example:

```text
interactive preview  -> low-latency provider
final master render  -> high-quality provider
```

A workflow can intentionally route the same capability differently at preview and final stages.

---

## 7. Provenance-first routing

When reproducibility matters, rank providers with strong stable IDs, versions, and transform metadata above providers that only return opaque outputs.

Useful for:

- creative canon
- training data preparation
- regulated workflows
- benchmark fixtures
- reproducible publishing

A provenance score should evaluate:

- stable asset/result ID
- source/model/version visibility
- input/output linkage
- transformation parameters
- timestamps
- retrievability

---

## 8. Confidence-aware fallback

Fallbacks should reduce confidence when they cannot provide equivalent evidence.

Example:

```text
Semrush unavailable
  -> public web research fallback
  -> keyword ideas still possible
  -> exact search-volume claims not possible
  -> route confidence reduced
```

Never use fallback as permission to hallucinate missing structured data.

---

## 9. Shadow providers

A shadow provider receives evaluation traffic but does not become the production route.

Use for:

- new plugin evaluation
- new local model comparison
- migration testing
- benchmark refresh

```yaml
provider: new-upscaler
mode: shadow
eligible_for_production: false
```

Promote only after benchmark and governance review.

---

## 10. Canary routing

Canary routing sends a small fraction of noncritical work to a candidate provider.

Use when benchmark fixtures are insufficient and real-world variation matters.

Record:

- route reason
- candidate provider version/state
- baseline provider
- output comparison
- human preference
- failures

Canaries should never bypass write/destructive approval rules.

---

## 11. Capability aliases

Source vocabularies will drift.

```yaml
canonical: media.asset.visual_search
aliases:
  - similar_image_search
  - visual_lookup
  - image_similarity
```

Rules:

1. aliases resolve to exactly one canonical ID
2. canonical IDs never silently change
3. deprecations create migration metadata
4. collisions fail validation

---

## 12. Provider aliases and identity stitching

One vendor may appear as:

- marketplace plugin name
- connector slug
- GitHub repository
- MCP package
- legacy plugin name

PluginOS should stitch these into one canonical provider only when evidence supports identity.

Do not merge merely because names look similar.

---

## 13. Provider successor graph

Lifecycle history should be explicit.

```text
legacy plugin
   -> replaced_by
modern app
   -> exposes
current plugin package
```

Successor edges can be:

- vendor_successor
- capability_successor
- protocol_migration
- rebrand
- native_replacement

This supports historical research without contaminating current routing.

---

## 14. Deterministic ecosystem snapshots

Every benchmark or production-critical route should be reproducible from a lockfile.

Lock:

- source revisions
- normalized graph hash
- policy version
- benchmark snapshot IDs
- schema versions

Do not store secrets in lockfiles.

---

## 15. Route explanation as a first-class artifact

Routing should produce an explanation artifact, not only a provider ID.

Minimum fields:

```yaml
capability: media.image.upscale
selected: magnific
excluded:
  local-esrgan: quality_below_project_threshold
  provider-x: unavailable
ranking_signals:
  quality: 0.95
  latency: 0.70
  cost: 0.62
  provenance: 0.80
policy_effects:
  specialist_first: +0.10
confidence: 0.91
```

Explanations make bad routes debuggable.

---

## 16. Multi-objective/Pareto routing

Do not force every decision into one weighted score.

Sometimes the useful output is a Pareto frontier:

```text
Magnific     best quality
Cloudinary   best latency/provenance balance
Local        best privacy/cost
```

The project policy then chooses among non-dominated candidates.

---

## 17. Workflow-level optimization

The cheapest provider at each stage may not produce the cheapest workflow.

Example:

- cheap generator creates poor assets
- expensive manual cleanup follows
- overall workflow cost rises

PluginOS can later score end-to-end routes using:

- stage success rates
- retry rates
- manual intervention
- downstream compatibility
- provenance completeness

---

## 18. Data-gravity routing

Prefer providers near the canonical data when moving data is expensive or risky.

Examples:

- Cloudinary-held image -> Cloudinary transform
- GitHub code -> GitHub-native repository operations
- Drive document -> Drive-native update

Data gravity is a routing signal, not an ownership transfer.

---

## 19. Output-compatibility routing

Provider choice should account for downstream needs.

A presentation workflow may require editable PPTX, not a beautiful rendered image. A media workflow may require alpha transparency, layered assets, or stable CDN URLs.

Capability contracts should eventually include output constraints.

---

## 20. Policy inheritance

Suggested hierarchy:

```text
global policy
  -> domain policy
     -> project policy
        -> workflow override
           -> action-time approval
```

More specific policy may tighten permissions freely. Loosening sensitive constraints should require an explicit policy decision.

---

## 21. First-party preference

Your own repositories can receive preference for capabilities where they are mature enough.

```yaml
preferences:
  first_party_bonus: 0.08
```

Do not let first-party preference override clear quality/security failures.

---

## 22. Capability-gap proposals

PluginOS can recommend installing or building a provider only after proving a gap.

A gap can be:

- zero provider
- only unavailable providers
- no provider satisfying privacy policy
- no provider satisfying output constraint
- single-provider resilience risk

This is better than generic plugin recommendations.

---

## 23. Benchmark-gated promotion

A new provider should move through:

```text
discovered
 -> available
 -> installed
 -> connected
 -> shadow
 -> benchmarked
 -> candidate
 -> preferred
```

Not every provider needs every state, but the progression should be explicit for important capabilities.

---

## 24. Staleness budgets

Different observations age differently.

Examples:

- provider install state: minutes/hours
- health: minutes
- price: days
- benchmark quality: weeks/months
- capability definition: months
- historical migration evidence: durable

PluginOS should eventually support per-observation staleness budgets.

---

## 25. Route regression detection

A route regression occurs when the winner changes unexpectedly.

CI can flag:

```text
media.image.upscale
  old: magnific
  new: provider-x
  cause: benchmark weight changed
```

The point is not to freeze routing forever. It is to make changes reviewable.

---

## 26. Human preference as evidence

For creative capabilities, human preference data matters.

Store preference observations with:

- fixture
- provider outputs
- reviewer
- timestamp
- selected result
- confidence/reason

Do not convert one subjective preference into permanent global truth.

---

## 27. Provider health circuit breaker

Future routing can automatically de-prioritize repeatedly failing providers.

Example policy:

```text
3 consecutive retryable failures -> degraded
10%+ failure rate over window -> warning
validated outage -> unavailable
recovery observations -> canary before full restore
```

This should affect routing, not permissions.

---

## 28. Historical reproducibility

A route from six months ago should remain explainable even if the provider disappears.

Preserve:

- provider canonical ID
- source revision
- route projection
- benchmark snapshot
- lifecycle state at decision time

Historical explainability is one of the strongest reasons to separate observations from current provider truth.
