# Security Policy

GPT-PluginOS v0.2 is a read-only advisory control plane. It must not store provider credentials or treat route selection as permission to execute.

## Report a vulnerability

Use GitHub's private vulnerability reporting for this repository when available. Do not include live secrets, tokens, or private customer data in public issues.

## Security-sensitive areas

- manifest/data parsing
- path handling for `--data-dir` and export paths
- action-risk classification
- policy constraint handling
- provenance integrity
- future remote adapters

## Invariants

- constraints are fail-closed
- destructive/financial/publication/deployment execution is out of scope for this runtime
- no OAuth/API credentials are persisted by PluginOS
- imported metadata is treated as untrusted input
