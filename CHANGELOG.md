# Changelog

All notable GPT-PluginOS changes are documented here.

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

### Notes

- CLI commands shown in documentation describe the intended future interface and are not claimed as implemented in v0.1.0.
- Provider benchmark scores in examples are illustrative until the benchmark harness exists.
- Provider selection remains advisory; authorization and execution remain the responsibility of SuperAgents/human policy.
