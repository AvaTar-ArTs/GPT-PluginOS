from __future__ import annotations
import json
from .registry import Registry
from .router import Router

def compile_registry(registry: Registry) -> dict:
    router = Router(registry)
    routes = {}
    for capability in registry.capabilities:
        routes[capability.id] = {}
        for policy in registry.policies:
            result = router.route(capability.id, policy.id)
            routes[capability.id][policy.id] = {
                "selected": result.selected.provider.id if result.selected else None,
                "diagnostic": result.diagnostic,
                "candidates": [
                    {"provider": c.provider.id, "score": round(c.score, 6), "risk": c.provider.risk}
                    for c in result.candidates
                ],
            }
    return {
        "schema": "pluginos.compiled.v1",
        "source_versions": registry.source_versions,
        "providers": registry.provider_records(),
        "capabilities": [c.__dict__ for c in registry.capabilities],
        "policies": [{"id": p.id, "label": p.label, "description": p.description, "weights": p.weights, "constraints": p.constraints} for p in registry.policies],
        "routes": routes,
    }

def dumps_compiled(registry: Registry) -> str:
    return json.dumps(compile_registry(registry), indent=2, sort_keys=True) + "\n"
