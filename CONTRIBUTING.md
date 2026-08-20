# Contributing

GPT-PluginOS is contract-first. Changes to providers, capabilities, policies, schemas, or routing behavior should include tests and a changelog entry.

## Development

```bash
python -m pip install --no-build-isolation -e .
python -m unittest discover -s tests -v
pluginos validate
```

## Rules

1. Keep provider IDs and capability IDs stable once published.
2. Never silently widen routing constraints to manufacture an eligible provider.
3. Selection must never imply authorization.
4. Preserve source/provenance metadata as adapters are added.
5. Add tests for behavior changes before merging.
6. Keep the runtime free of credentials and provider secrets.
