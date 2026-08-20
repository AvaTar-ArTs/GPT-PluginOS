# GPT-PluginOS Governance Playbook

Governance exists to keep provider selection, authorization, and execution from collapsing into one opaque decision.

## 1. Core rule

> **Selection never implies authorization.**

PluginOS may recommend a provider. SuperAgents and human policy determine whether an action may execute.

---

## 2. Risk classes

### `read_only`

Reads data without changing external state.

Examples: search assets, inspect repositories, query calendars, fetch SEO metrics.

Default: routable under normal read policy.

### `external_write`

Creates or modifies external state.

Examples: upload asset, create document, add Airtable record, create calendar event.

Default: require write-capable policy; provider-specific approval may apply.

### `destructive_write`

Deletes or irreversibly mutates external state.

Examples: delete Cloudinary asset, remove record, delete calendar event.

Default: explicit human approval near action time.

### `financial`

Moves money or materially affects financial state.

Examples: refund, create/alter payment-related state.

Default: explicit approval plus strong audit record.

### `identity_or_access`

Changes accounts, access, permissions, or security posture.

Default: explicit approval, least privilege, and auditable identity context.

### `publication`

Makes content public or sends it to an audience.

Examples: publish page, post campaign, send outbound announcement.

Default: final-content confirmation unless a narrow pre-approved automation exists.

### `code_change`

Changes source code or repository state.

Default: repository workflow, tests, diff review, and change provenance.

### `deployment`

Publishes software to an environment.

Default: environment-aware approval and deployment policy.

---

## 3. Action-level classification

Never classify only the provider.

Example Cloudinary:

```text
search       read_only
upload       external_write
metadata     external_write
delete       destructive_write
```

Example GitHub:

```text
read file    read_only
create issue external_write
change code  code_change
merge PR     code_change
```

Provider-level risk may be a summary, but action risk controls execution.

---

## 4. Approval matrix

Recommended baseline:

| Action class | Route automatically | Execute automatically | Human confirmation |
|---|---:|---:|---:|
| read_only | yes | policy-dependent | usually no |
| external_write | yes | narrow policy only | often |
| destructive_write | yes | no | yes |
| financial | yes | no | yes |
| identity_or_access | yes | no | yes |
| publication | yes | narrow policy only | usually yes |
| code_change | yes | through controlled workflow | review-dependent |
| deployment | yes | controlled environments only | production usually yes |

---

## 5. Governance inheritance

Recommended order:

```text
global
  -> domain
    -> project
      -> workflow
        -> action
```

A lower level can tighten restrictions. Relaxing high-risk restrictions should require explicit policy review.

---

## 6. Failure class: stale install state

**Symptom:** PluginOS routes to a provider believed connected, but the provider is no longer authenticated or installed.

**Detection:** compare fresh plugin inventory observation with lockfile.

**Response:**

1. mark provider state stale/degraded
2. lower route confidence
3. reroute if an equivalent provider exists
4. emit drift finding
5. do not rewrite the authoritative provider record to “removed” without evidence

---

## 7. Failure class: provider outage

**Symptom:** provider repeatedly fails or authoritative status says unavailable.

**Response:**

```text
healthy -> degraded -> unavailable
```

- preserve last successful observation
- identify affected capabilities
- route to eligible fallbacks
- lower confidence where fallback is semantically weaker
- canary provider after recovery before restoring preferred status for critical workloads

---

## 8. Failure class: schema drift

**Symptom:** source catalog changes shape and adapter can no longer normalize it.

**Response:**

- fail adapter independently
- retain prior source observation as stale
- emit diagnostic with source revision
- block lockfile promotion if affected domains are critical
- update adapter/schema through versioned migration

Never silently drop unknown fields that may carry risk or permission meaning.

---

## 9. Failure class: alias collision

**Symptom:** one alias maps to multiple canonical capability/provider IDs.

**Response:** compilation failure.

Do not resolve ambiguous aliases by fuzzy name similarity.

Resolution requires:

- authoritative identity evidence
- explicit precedence rule
- or removal of ambiguous alias

---

## 10. Failure class: silent capability expansion

**Symptom:** a provider gains new write/destructive actions or broader capability scope.

**Response:**

1. mark as governance drift
2. classify new actions before normal routing
3. compare permission implications
4. require review for newly sensitive actions
5. update lockfile only after review

This protects against a provider becoming more powerful without the control plane noticing.

---

## 11. Failure class: provenance loss

**Symptom:** result exists but source/provider/input linkage is missing.

**Response depends on workflow:**

- exploratory task: allow with warning if policy permits
- benchmark: invalidate result
- creative canon: quarantine until provenance repaired
- publication: block if provenance is mandatory
- security/financial: treat missing audit evidence as failure

---

## 12. Failure class: benchmark gaming

A provider can look best if fixtures accidentally favor it.

Mitigations:

- multiple fixture families
- blinded human review for subjective media tasks
- hidden holdout fixtures
- repeat runs
- dimension-level scoring
- preserve raw outputs
- compare confidence intervals where enough runs exist
- never let vendor-specific benchmark features dominate the capability definition

---

## 13. Failure class: cost runaway

**Symptom:** retries, expensive provider selection, or high-volume generation exceeds expected cost.

Controls:

- cost class policy
- per-workflow budget envelope
- retry caps
- batch-size limits
- route to cheaper preview provider before final provider
- anomaly alert when cost per successful result rises materially

PluginOS should record cost observations, not billing credentials.

---

## 14. Failure class: recursive orchestration

**Symptom:** PluginOS routes to an agent/provider that routes back to PluginOS indefinitely.

Mitigation:

- execution envelope includes route depth
- maintain visited provider/capability path
- set maximum orchestration depth
- distinguish control-plane resolution from executor invocation

---

## 15. Failure class: provider output incompatibility

**Symptom:** provider satisfies the broad capability but output cannot feed the next stage.

Example: presentation provider returns only rendered images when workflow requires editable PPTX.

Mitigation:

- model output constraints
- include MIME/artifact classes in capability contract
- route based on downstream compatibility

---

## 16. Failure class: false equivalence

Do not compare providers that share a category but solve different problems.

Examples:

- Semrush SEO metrics vs Sider Scholar academic research
- Product Design UX audit vs Canva marketing graphics
- Cloudinary media infrastructure vs Magnific premium enhancement

Provider overlap should be capability-specific.

---

## 17. Failure class: source-of-truth inversion

**Symptom:** a generated PluginOS projection is edited as though it were authoritative.

Rules:

- fix SuperSkills capability definitions in SuperSkills
- fix external provider/action definitions in gpt-plugs
- fix agent runtime contracts in SuperAgents
- fix creative lineage in Content Universe
- regenerate PluginOS projection afterward

Generated projections are disposable.

---

## 18. Publication guard

Before a publication-capable route executes, verify:

- target destination
- final artifact identity
- project/campaign association
- approval policy
- provider connected state
- last-minute content review if required
- provenance record exists

---

## 19. Financial guard

Before a financial route executes, verify:

- exact provider/action
- exact amount/state change if applicable
- target customer/product/account identity
- duplicate-action prevention
- explicit approval
- audit record

PluginOS should never infer consent from prior unrelated financial actions.

---

## 20. Destructive-action guard

A destructive route explanation should include:

- resource identity
- provider
- action
- reversibility/backup state if known
- blast radius
- approval requirement

Bulk destructive actions deserve stronger review than single-resource changes.

---

## 21. Code-change guard

Preferred flow:

```text
route
 -> inspect source
 -> isolate branch/worktree
 -> test-driven change
 -> verification
 -> security review where appropriate
 -> diff review
 -> merge/deploy approval
```

PluginOS describes the provider/capability route. It does not bypass development methodology.

---

## 22. Governance review checklist

For every preferred provider:

- [ ] stable canonical ID
- [ ] authoritative source
- [ ] capabilities are specific
- [ ] action-level risk declared
- [ ] aliases unambiguous
- [ ] install/connection state observable or explicitly unknown
- [ ] fallback behavior defined for critical capabilities
- [ ] provenance support documented
- [ ] benchmark coverage exists when overlap matters
- [ ] lifecycle state current
- [ ] no secrets stored in registry

---

## 23. Incident record

A provider-routing incident should record:

```yaml
incident_id: route-incident-2026-001
capability: media.image.upscale
expected_provider: magnific
actual_provider: cloudinary
cause: stale_connection_observation
impact: quality_regression
lockfile: pluginos.lock.json
source_revisions: {}
resolution: refreshed provider inventory and invalidated stale route cache
```

Incidents become useful test fixtures after the immediate issue is fixed.

---

## 24. Governance principle

The goal is not maximal automation. The goal is **maximal clarity about what the automation is allowed to do, why it chose a provider, and how to recover when that choice is wrong.**
