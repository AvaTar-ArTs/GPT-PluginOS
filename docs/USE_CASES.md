# GPT-PluginOS Use-Case Catalog

This catalog describes what GPT-PluginOS is meant to solve in practice. Each use case is provider-neutral first and provider-aware second.

## Use-case template

Every production use case should be describable with:

- **ID**: stable reference for docs, fixtures, tests, and benchmarks
- **Intent**: what the user or agent is trying to achieve
- **Capabilities**: dotted capability IDs required
- **Candidate providers**: providers that may satisfy each capability
- **Routing signals**: quality, cost, latency, privacy, health, install state, project preference
- **Risk**: read/write/destructive/financial/publication/code/deployment classes
- **Approval point**: where SuperAgents or a human must approve
- **Provenance sink**: where outputs and lineage should be recorded
- **Success criteria**: measurable definition of done
- **Degraded path**: what happens when the preferred provider is unavailable

---

# 1. Creator and media production

## UC-CREATOR-001: Character reference to multi-platform campaign

**Intent:** Turn an approved character reference into YouTube, short-form, social, and archive-ready creative variants without losing lineage.

**Capabilities:**

- `media.asset.ingest`
- `media.asset.visual_search`
- `media.image.upscale`
- `media.transform.image`
- `design.marketing.compose`
- `media.asset.register`
- `provenance.record`

**Candidate providers:**

- Cloudinary for ingest, transform, delivery, search, and relations
- Magnific for premium enhancement/upscale
- Canva for branded marketing composition
- Content Universe as provenance/lineage sink

**Routing signals:** character fidelity, output dimensions, cost ceiling, transformation determinism, provenance quality.

**Risk:** external write; publication only if a later stage actually posts the content.

**Success criteria:** every derivative points to the canonical source asset and records provider, transformation, project, and campaign relationship.

**Degraded path:** if Magnific is unavailable, use Cloudinary transformation or a local upscale provider and lower the route-confidence/quality expectation.

---

## UC-CREATOR-002: Find visually related assets across a huge library

**Intent:** Locate prior creations resembling a new reference or concept before generating duplicates.

**Capabilities:**

- `media.asset.visual_search`
- `media.asset.search`
- `content.graph.query`

**Candidate providers:** Cloudinary visual search plus Content Universe graph search.

**Advanced behavior:** combine visual similarity with semantic/project lineage. A visually similar image from another character series should rank below a slightly less similar image from the same canon branch if project policy prioritizes canon.

**Success criteria:** return results grouped into exact/near duplicate, visual sibling, same-character, and same-campaign classes.

---

## UC-CREATOR-003: Duplicate and near-duplicate prevention

**Intent:** Prevent asset libraries from filling with accidental copies, alternate crops, and indistinguishable exports.

**Capabilities:**

- `media.asset.hash`
- `media.asset.visual_search`
- `media.asset.compare`
- `media.asset.relate`

**Routing model:** exact hashes first, perceptual similarity second, semantic relationship third.

**Result classes:**

- exact duplicate
- derived transformation
- crop/resized sibling
- alternate generation
- same composition
- unrelated

**Provenance rule:** never delete automatically based only on similarity.

---

## UC-CREATOR-004: Creator campaign compiler

**Intent:** Convert a campaign brief into research, design, assets, video, schedule, and publishing-ready outputs.

**Capabilities:**

```text
research.market.discover
research.seo.keyword
design.product.ideate
media.image.generate
media.image.upscale
media.video.generate
media.video.edit
media.asset.register
design.marketing.compose
schedule.event.create
publication.prepare
```

**Candidate providers:** Product Hunt, Semrush, Product Design, media generators, Magnific, HeyGen, Descript, HyperFrames, Cloudinary, Canva, Google Calendar.

**Why PluginOS matters:** no single provider should own this entire workflow. PluginOS decomposes the intent into specialist capabilities and provides an advisory route per stage.

---

## UC-CREATOR-005: Reel production from existing creative universe

**Intent:** Build a reel from existing project assets rather than generating everything from scratch.

**Capabilities:**

- `content.graph.query`
- `media.asset.retrieve`
- `media.video.compose`
- `media.audio.align`
- `media.transform.video`
- `publication.prepare`

**Candidate providers:** Content Universe, `icho-reel-eng`, HyperFrames, Descript, Cloudinary.

**Advanced routing:** prefer first-party project assets with strong provenance over visually attractive but unrelated assets.

---

# 2. Product and design

## UC-DESIGN-001: Idea to validated product direction

**Intent:** Turn a product idea into researched UX directions and a selected prototype target.

**Capabilities:**

- `design.product.research`
- `design.product.audit`
- `design.product.ideate`
- `design.prototype.generate`
- `design.prototype.qa`

**Primary provider:** Product Design.

**Downstream providers:** Figma for canonical editable design; GitHub/Vercel for implementation and preview.

**Boundary:** Product Design discovers and validates directions. It does not become the canonical code or design-system repository.

---

## UC-DESIGN-002: Existing product flow audit

**Intent:** Audit onboarding, checkout, settings, or another multi-step flow.

**Capabilities:** `design.product.audit`.

**Routing signals:** source-capture ability, accessibility analysis, product-flow reasoning, evidence quality.

**Success criteria:** every finding is tied to captured evidence and classified by severity/impact.

---

## UC-DESIGN-003: Brand-safe asset adaptation

**Intent:** Adapt an approved design to multiple channels while maintaining brand rules.

**Capabilities:**

- `design.brand.validate`
- `design.marketing.compose`
- `media.transform.image`

**Candidate providers:** Canva, Figma, Cloudinary.

**Routing distinction:** Canva is preferred for bulk branded collateral, Figma for product-design source of truth, Cloudinary for programmatic transformation/delivery.

---

# 3. Research and intelligence

## UC-RESEARCH-001: SEO opportunity discovery

**Intent:** Identify keyword and competitor opportunities using structured current data.

**Capabilities:**

- `research.seo.keyword`
- `research.seo.competitor`
- `research.web.verify`

**Candidate providers:** Semrush as structured authority; public web research as contextual fallback.

**Success criteria:** metrics are source-grounded and timestamped; advice distinguishes measured facts from strategic inference.

---

## UC-RESEARCH-002: Academic evidence synthesis

**Intent:** Build a source-grounded research brief from papers.

**Capabilities:**

- `research.academic.search`
- `research.academic.retrieve`
- `research.synthesize`
- `research.citation.trace`

**Candidate provider:** Sider Scholar for paper discovery and collection analysis, plus native reasoning for synthesis.

**Risk:** read-only.

**Success criteria:** every major claim is traceable to papers or explicitly labeled interpretation.

---

## UC-RESEARCH-003: Product-market radar

**Intent:** Track emerging AI tools/products relevant to current creator and automation work.

**Capabilities:**

- `research.market.discover`
- `research.product.compare`
- `research.trend.rank`

**Candidate providers:** Product Hunt, web research, Semrush where domain traction matters.

**Advanced pattern:** PluginOS can distinguish “interesting new provider” from “capability already saturated by installed providers.”

---

## UC-RESEARCH-004: Legacy plugin archaeology

**Intent:** Study how old ChatGPT plugins evolved into apps, actions, modern plugins, MCP servers, or native features.

**Capabilities:**

- `research.plugin.history`
- `provider.lifecycle.map`
- `provider.successor.resolve`

**Sources:** Awesome-Plugins, current plugin directory, GitHub, vendor documentation.

**Output:** migration graph, survival rates, capability-category changes, successor mappings.

---

# 4. Software engineering and agent systems

## UC-DEV-001: Capability-aware code change

**Intent:** Route a requested software change through the correct engineering stack.

**Capabilities:**

- `code.repository.read`
- `code.repository.modify`
- `code.test.run`
- `code.review`
- `security.scan`

**Candidate providers:** GitHub, Codex Security, local/Codex tooling.

**Risk:** code change.

**Approval:** SuperAgents execution policy remains authoritative.

**Success criteria:** changes are tested, reviewable, provenance-linked, and do not bypass repository workflow.

---

## UC-DEV-002: Agent selects provider by capability, not vendor name

**Intent:** An agent needs image upscaling but should not hard-code Magnific.

**Capability:** `media.image.upscale`.

**PluginOS role:** return ranked providers and route explanation.

**SuperAgents role:** choose/approve execution path and run adapter.

**Benefit:** provider replacement does not require rewriting the agent’s core workflow.

---

## UC-DEV-003: Specialist repository as provider

**Intent:** Expose an existing repository such as `pythons`, `n8n_workflows`, or `icho-reel-eng` as a capability provider.

**Capabilities:** declared via `pluginos-provider.yaml` or compatible manifest.

**Provider type:** local/repository-backed rather than marketplace plugin.

**Advanced value:** first-party tooling can compete in the same routing graph as external SaaS providers.

---

## UC-DEV-004: Cross-repo schema drift detection

**Intent:** Detect when SuperSkills, gpt-plugs, or SuperAgents changes in a way that invalidates PluginOS projections.

**Capabilities:**

- `ecosystem.source.scan`
- `ecosystem.schema.validate`
- `ecosystem.lock.diff`

**Success criteria:** CI reports affected capabilities/providers before route behavior silently changes.

---

# 5. Knowledge and operational systems

## UC-KNOWLEDGE-001: Email/document/project context assembly

**Intent:** Assemble context from Gmail, Drive, Notion, Slack, and Airtable for a project decision.

**Capabilities:**

- `knowledge.email.search`
- `knowledge.document.search`
- `knowledge.workspace.search`
- `operations.records.query`

**Routing policy:** provider follows data ownership. PluginOS should not copy canonical data into its registry.

**Risk:** read-only unless the workflow later drafts or writes changes.

---

## UC-KNOWLEDGE-002: Structured project handoff

**Intent:** Turn research and conversation outputs into durable project records.

**Capabilities:**

- `knowledge.document.create`
- `operations.record.create`
- `communication.notify`

**Candidate providers:** Drive/Notion for documents, Airtable for structured state, Slack for notification.

**Governance:** creation is external write; notification/publication requires separate approval semantics.

---

# 6. Scheduling and temporal orchestration

## UC-TIME-001: Release calendar from repository milestones

**Intent:** Turn a software/content release plan into scheduled checkpoints.

**Capabilities:**

- `code.release.read`
- `schedule.event.create`
- `schedule.event.update`

**Candidate providers:** GitHub + Google Calendar.

**Advanced rule:** schedule state should reference the originating release/project ID so later changes can be reconciled.

---

## UC-TIME-002: Content production cadence

**Intent:** Coordinate research, creation, review, and publication windows for a recurring content system.

**Capabilities:**

- `schedule.window.plan`
- `schedule.event.create`
- `operations.task.reference`

**Provider:** Google Calendar as temporal system; Airtable/Notion may remain work-state systems.

**Boundary:** PluginOS should not invent a second task/calendar database.

---

# 7. Commerce and monetization

## UC-COMMERCE-001: Product/payment infrastructure decision

**Intent:** Determine whether Stripe is the appropriate provider for a payment-related capability.

**Capabilities:**

- `commerce.product.create`
- `commerce.price.create`
- `commerce.payment.manage`

**Provider:** Stripe.

**Risk:** financial and external write.

**PluginOS behavior:** classify and explain route; never infer authorization from installation.

---

## UC-COMMERCE-002: Campaign-to-product workflow

**Intent:** Move a creator campaign from concept into product page/payment readiness.

**Capabilities:**

```text
research.market.discover
design.marketing.compose
commerce.product.create
commerce.price.create
deploy.web.publish
```

**Approval gates:** product creation, pricing, and deployment are separate write events.

---

# 8. Security and governance

## UC-SEC-001: Security review before provider promotion

**Intent:** Evaluate a new code-based provider before it becomes a preferred route.

**Capabilities:**

- `security.scan`
- `provider.risk.classify`
- `provider.provenance.verify`

**Candidate provider:** Codex Security for repository scanning.

**Success criteria:** provider cannot become preferred for sensitive workflows while unresolved high-risk findings remain.

---

## UC-SEC-002: Destructive action guardrail

**Intent:** A provider supports both read/search and delete actions.

**PluginOS behavior:** action-level risk remains explicit.

```text
media.asset.search -> read_only
media.asset.update -> external_write
media.asset.delete -> destructive_write
```

**Anti-pattern:** assigning one blanket risk level to the provider.

---

## UC-SEC-003: Permission drift detection

**Intent:** Detect that a provider’s action surface or permission model has expanded.

**Capabilities:**

- `provider.permissions.observe`
- `ecosystem.lock.diff`
- `governance.risk.audit`

**Response:** flag for review before new write-capable actions enter normal routing.

---

# 9. Provider benchmarking and overlap

## UC-BENCH-001: Choose the best image upscaler per project

**Candidates:** Magnific, Cloudinary, local provider.

**Dimensions:** detail recovery, artifact rate, character fidelity, latency, cost, provenance.

**Expected result:** Pareto frontier, not one permanent winner.

---

## UC-BENCH-002: Presentation provider comparison

**Candidates:** native Presentations, Gamma, SlidesGPT, Genspark.

**Dimensions:** structure, editable output, source grounding, visual hierarchy, export quality, iteration ergonomics.

**Project policy examples:**

- client deck: prioritize visual polish + editable export
- technical report: prioritize source fidelity + structure
- rapid ideation: prioritize latency + iteration

---

## UC-BENCH-003: Research-provider benchmark

**Candidates:** Sider Scholar, Semrush, web research depending on capability.

**Rule:** do not compare unlike capabilities as though they were interchangeable. Academic-paper retrieval and SEO keyword metrics belong to different capability families even though both are “research.”

---

# 10. Ecosystem maintenance

## UC-ECO-001: Plugin installation audit

**Intent:** Reassess installed providers after a wave of new plugin additions.

**Capabilities:**

- `provider.inventory.scan`
- `provider.overlap.analyze`
- `provider.role.assign`
- `provider.gap.detect`

**Output:** keep / benchmark / de-prioritize / remove-candidate classifications.

**Key question:** What unique job does each installed provider own?

---

## UC-ECO-002: Capability-gap analysis

**Intent:** Decide whether to install/build another provider.

**Process:**

1. Inventory required capabilities.
2. Map existing providers.
3. Identify unsupported capabilities.
4. Identify capabilities with only one fragile provider.
5. Search/install/build only where a real gap or resilience need exists.

This avoids plugin hoarding.

---

## UC-ECO-003: Promote experimental skill to canonical capability

**Intent:** A useful skill in `agent-skills` proves stable and should become part of SuperSkills.

**Flow:**

```text
agent-skills experiment
  -> evaluation
  -> SuperSkills promotion
  -> capability ID becomes canonical
  -> PluginOS recompiles provider graph
  -> SuperAgents route projection updates
```

---

# 11. Anti-use-cases

These are intentionally **not** jobs for PluginOS itself.

## AU-001: “Delete these Cloudinary assets”

PluginOS may identify Cloudinary as the provider and classify deletion as destructive. SuperAgents/human approval and the provider adapter perform the action.

## AU-002: “Publish this campaign now”

PluginOS can route publication capabilities and expose risk. It should not publish autonomously.

## AU-003: “Charge/refund this customer”

PluginOS classifies Stripe and financial risk. Execution belongs behind explicit financial approval.

## AU-004: “Rewrite SuperSkills definitions inside PluginOS”

Wrong source of truth. PluginOS references SuperSkills; it does not fork its canonical definitions.

## AU-005: “Store every generated image in PluginOS”

Wrong substrate. Use Cloudinary/Content Universe for media storage and lineage.

---

# 12. High-value future use cases

As the runtime matures, PluginOS can support:

- automatic provider de-prioritization after repeated health failures
- capability-specific canary routing
- per-project provider policies
- privacy-sensitive local/provider zoning
- benchmark regression alerts
- provider-cost anomaly detection
- route explanation histories
- workflow reproducibility from lockfiles
- historical ecosystem research dashboards
- provider migration/successor recommendation
- first-party-vs-SaaS cost/quality comparisons
- synthetic capability-gap proposals
- generated SuperAgents routing projections
- Content Universe provenance envelopes for provider-assisted creative work

The common thread is always the same: **make capability choice explicit, evidence-backed, reversible, and governable.**
