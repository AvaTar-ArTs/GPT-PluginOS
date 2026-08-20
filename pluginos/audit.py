from __future__ import annotations
from collections import Counter, defaultdict
from .registry import Registry

def audit_registry(registry: Registry) -> dict:
    coverage = defaultdict(list)
    for p in registry.providers:
        for c in p.capabilities:
            coverage[c].append(p.id)
    uncovered = [c.id for c in registry.capabilities if not coverage[c.id]]
    single_source = sorted([cap for cap, ids in coverage.items() if len(ids) == 1])
    degraded = sorted([p.id for p in registry.providers if p.status == "degraded"])
    risk_counts = Counter(p.risk for p in registry.providers)
    return {
        "provider_count": len(registry.providers),
        "capability_count": len(registry.capabilities),
        "uncovered_capabilities": uncovered,
        "single_source_capabilities": single_source,
        "degraded_providers": degraded,
        "risk_counts": dict(sorted(risk_counts.items())),
    }
