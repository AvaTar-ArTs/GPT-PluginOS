# Changelog

All notable GPT-PluginOS changes are documented here.

## [Unreleased]

## [0.2.0] - 2026-08-20

### Added

- Installable Python 3.11+ `gpt-pluginos` package and `pluginos` CLI.
- Read-only normalized registry with 12 seed providers, 36 declared capabilities, and 5 policy presets.
- Strict graph validation for duplicate IDs and unknown provider capability references.
- Deterministic provider ranking across quality, privacy, latency, cost, and health signals.
- Hard policy constraints including local-only, max-cost, read-only, and degraded-provider exclusion without silent widening.
- Route explanation payloads that explicitly report `authorization_implied: false`.
- `scan`, `providers`, `capabilities`, `route`, `explain`, `overlaps`, `benchmark`, `compile`, `lock`, `diff`, `graph`, `audit`, and `export-site` commands.
- Deterministic ecosystem graph hash and committed `pluginos.lock.json` seed snapshot.
- Compiled route-projection model and Studio dataset export.
- JSON Schema contracts for providers, capabilities, policies, route projections, lockfiles, compiled registries, and provenance envelopes.
- 17 regression tests covering registry invariants, routing, fail-closed constraints, lockfiles, compiler output, CLI behavior, and schema syntax.
- GitHub Actions validation workflow plus Makefile release-check targets.
- Runtime operator guide, security policy, contribution rules, and executable-runtime checkpoint.
- Dependency-free static field site under `site/` with command center, advanced uses, market/revenue pages, Studio, and Revenue Studio.

### Changed

- Expanded the capability catalog so every provider capability edge resolves to a declared capability.
- Tuned the `quality-first` policy so its behavior matches its name for the seed image-upscale route.
- Synchronized Studio provider/capability/policy datasets with the canonical v0.2 runtime registry.
- Updated project status from architecture/design-only to an executable foundation runtime.

### Security

- Preserved selection-versus-authorization separation as a runtime invariant.
- Kept v0.2 read-only with no credential storage or provider action execution.
- Added fail-closed handling for policy constraints and explicit security-sensitive areas in `SECURITY.md`.

## [0.1.0] - 2026-08-19

### Added

- Federated architecture design defining GPT-PluginOS as a capability control plane rather than an execution runtime.
- Canonical ecosystem boundaries for SuperSkills, SuperAgents, agent-skills, gpt-plugs, Content Universe, CreativeOS, and specialist repositories.
- Comprehensive operator handbook covering scan/validate/compile/audit concepts, provider lifecycle, routing contexts, overlap review, degraded operation, lockfiles, drift, and debugging.
- Extensive use-case catalog across creator/media production, product design, research, software engineering, knowledge operations, scheduling, commerce, security, benchmarking, and ecosystem maintenance.
- Worked provider, route, and workflow examples designed to become future runtime/compiler fixtures.
- Advanced routing patterns including provider ensembles, local-first/privacy routing, cost and latency constraints, shadow/canary providers, capability aliases, provider successor graphs, provenance-first routing, Pareto selection, staleness budgets, circuit breakers, and route regression detection.
- Governance playbook with action-level risk classes, approval matrix, destructive/financial/publication/code/deployment guards, and failure-response patterns.
- Benchmark and evaluation playbook for media, video, presentations, research, development, and asset infrastructure.
- Cross-repository ecosystem integration guide and provider-maturity model.
- Initial implementation plan for the operator handbook/reference layer.

### Reference examples

- `examples/provider-cloudinary.yaml`
- `examples/provider-product-design.yaml`
- `examples/provider-google-calendar.yaml`
- `examples/route-media-upscale.yaml`
- `examples/route-product-audit.yaml`
- `examples/workflow-creator-campaign.yaml`
- `examples/workflow-code-release.yaml`
