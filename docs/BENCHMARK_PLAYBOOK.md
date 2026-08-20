# GPT-PluginOS Benchmark & Evaluation Playbook

Benchmarks answer a narrow question:

> For this capability, under these constraints, which provider performs best enough to influence routing?

They do not declare a permanent universal winner.

## 1. Benchmark identity

Every benchmark run should have a stable record:

```yaml
id: image-upscale-v3-2026-08-19
capability: media.image.upscale
suite_version: 3
lockfile: pluginos.lock.json
providers:
  - magnific
  - cloudinary
  - local-esrgan
fixture_set: upscale-canon-v2
started_at: 2026-08-19T23:00:00-04:00
```

Record provider state, source revision, model/version when observable, policy, and environment.

---

## 2. Benchmark principles

1. Benchmark capabilities, not marketing categories.
2. Preserve raw inputs and outputs.
3. Use the same fixture family across providers unless provider constraints make that impossible.
4. Separate objective metrics from subjective review.
5. Version fixtures and scoring rubrics.
6. Timestamp results.
7. Re-run when provider behavior materially changes.
8. Record failures, not just successful outputs.
9. Never compare unequal output requirements without declaring the difference.
10. Treat benchmark scores as observations, not eternal provider metadata.

---

## 3. Score dimensions

Recommended common dimensions:

- capability fit
- output quality
- adherence/correctness
- latency
- cost class
- reliability
- provenance quality
- output compatibility
- operator ergonomics

Weights belong to project/routing policy, not the benchmark fixture itself.

---

## 4. Image upscale suite

### Fixtures

Include:

- anime/manga line art
- painterly illustration
- typography-heavy graphic
- low-resolution photo
- detailed character portrait
- noisy/compressed image
- transparent PNG if supported

### Metrics

| Dimension | Example measure |
|---|---|
| detail recovery | blinded reviewer score |
| character fidelity | identity/canon reviewer score |
| line integrity | edge artifact review |
| text integrity | OCR/manual comparison |
| hallucination | invented-detail penalty |
| latency | seconds to usable output |
| provenance | IDs/version/transform metadata |
| cost | normalized cost class |

### Example scorecard

```yaml
provider: magnific
scores:
  detail_recovery: 0.96
  character_fidelity: 0.90
  text_integrity: 0.72
  latency: 0.58
  provenance: 0.75
```

Do not collapse this to `0.82` until a routing policy supplies weights.

---

## 5. Image generation suite

Dimensions:

- prompt adherence
- character consistency
- composition
- style fidelity
- text rendering
- reference-image adherence
- editing controllability
- seed/reproducibility support
- latency
- cost
- provenance

Use multi-turn edit fixtures as well as one-shot generation.

A provider that wins one-shot beauty but cannot preserve character identity across edits may rank lower for a comic workflow.

---

## 6. Video suite

Separate capability families:

- avatar/talking video
- text-to-video
- image-to-video
- transcript-based editing
- programmable composition
- localization/lipsync

Do not benchmark HeyGen and HyperFrames as if they are identical simply because both output video.

Metrics can include:

- motion quality
- lip sync
- temporal consistency
- editability
- caption accuracy
- render latency
- export quality
- programmatic control

---

## 7. Presentation suite

Candidate dimensions:

- information architecture
- source grounding
- visual hierarchy
- text density
- editable output
- diagram quality
- brand adherence
- export fidelity
- revision ergonomics
- latency

Example task classes:

- executive pitch
- technical architecture deck
- educational explainer
- campaign proposal
- data-heavy report

A winner can differ by task class.

---

## 8. Research suite

### Source-quality dimensions

- authority
- relevance
- freshness
- citation completeness
- factual accuracy
- retrieval recall
- structured output quality

### SEO benchmark

Semrush should be evaluated on structured metrics it actually provides. A generic web-search fallback must not be rewarded for inventing equivalent numeric data.

### Academic benchmark

Sider Scholar can be evaluated on paper discovery, source traceability, retrieval usefulness, and collection-level synthesis support.

---

## 9. Development suite

Capabilities:

- code.repository.modify
- code.review
- security.scan
- code.test.generate

Metrics:

- correctness
- minimal diff quality
- test coverage
- regression rate
- security finding quality
- reproducibility
- explanation quality
- repository convention adherence

A “more code generated” metric is not useful.

---

## 10. Asset infrastructure suite

For Cloudinary-like providers:

- upload reliability
- search quality
- visual-search precision
- transform determinism
- metadata richness
- relation support
- delivery latency
- archive/recovery behavior
- provenance identifiers
- destructive-action safety

This benchmark is infrastructure-oriented, not aesthetic.

---

## 11. Human review protocol

For subjective creative tasks:

1. blind provider identity where possible
2. randomize output order
3. use a written rubric
4. score independently before discussion
5. record preference and confidence
6. preserve all outputs

Useful fields:

```yaml
reviewer: reviewer-01
fixture: character-poster-07
selected_output: B
scores:
  composition: 4
  fidelity: 5
  typography: 3
confidence: high
notes: Strongest character identity; minor title artifacts.
```

---

## 12. Repeatability

At least some fixtures should run multiple times for stochastic providers.

Record:

- run count
- success rate
- mean/median latency
- quality variance
- failure modes

A provider with rare spectacular outputs and frequent failures may be poor for production routing.

---

## 13. Benchmark freshness

Suggested starting budgets:

| Observation | Suggested freshness |
|---|---|
| outage/health | hours |
| latency | days |
| cost | days/weeks |
| generative quality | weeks |
| stable infrastructure semantics | months |

These are policy defaults, not laws.

A stale score remains historical evidence but receives a routing penalty.

---

## 14. Invalidation triggers

Invalidate or re-run when:

- provider changes underlying model/version
- action behavior changes
- pricing materially changes
- provider becomes newly connected
- fixture set changes
- scoring rubric changes
- output contract changes
- repeated real-world results contradict benchmark expectations

---

## 15. Regression thresholds

Example policy:

```yaml
regression:
  quality_drop_absolute: 0.10
  failure_rate_increase: 0.05
  latency_increase_ratio: 1.50
```

A threshold breach should trigger review, not automatically uninstall a provider.

---

## 16. Pareto evaluation

Provider A may be best quality, B best latency, C best privacy.

```text
             quality  latency  privacy
Magnific       ★★★★★    ★★       ★★
Cloudinary     ★★★★     ★★★★★    ★★
Local          ★★★      ★★★      ★★★★★
```

All three can be rational routing choices under different policies.

---

## 17. Composite workflow benchmark

Later phases should evaluate end-to-end workflows.

Example creator pipeline metrics:

- usable final-output rate
- number of retries
- manual correction time
- total latency
- total cost
- provenance completeness
- cross-stage compatibility

This catches local optima where each stage looks good individually but the workflow performs poorly.

---

## 18. Shadow evaluation

New providers should run against production-like fixtures without receiving real production writes.

```yaml
mode: shadow
production_eligible: false
```

After sufficient evidence, promote to candidate routing state.

---

## 19. Benchmark artifact layout

Suggested future structure:

```text
benchmarks/
  media-image-upscale/
    suite.yaml
    fixtures/
    runs/
      2026-08-19/
        manifest.json
        outputs/
        scores.json
        reviews.jsonl
```

Raw outputs should be stored in an appropriate asset system and referenced by stable IDs when large.

---

## 20. Benchmark-to-routing contract

Routing should consume normalized benchmark observations such as:

```yaml
capability: media.image.upscale
provider: magnific
snapshot: image-upscale-v3
scores:
  quality: 0.94
  latency: 0.61
  provenance: 0.77
confidence: 0.88
observed_at: 2026-08-19T23:00:00-04:00
```

The routing policy decides weights.

Benchmark code should never directly overwrite provider preference rankings.

---

## 21. Benchmark integrity checklist

- [ ] capability is specific
- [ ] fixtures are versioned
- [ ] provider state captured
- [ ] same task intent across providers
- [ ] raw outputs retained/referenced
- [ ] failures recorded
- [ ] subjective review blinded where practical
- [ ] cost/latency measured separately from quality
- [ ] provenance measured
- [ ] result timestamped
- [ ] lockfile attached
- [ ] routing consumes observation without treating it as permanent truth
