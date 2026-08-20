from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from .registry import Registry

def canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def build_lock(registry: Registry) -> dict:
    graph = {
        "providers": registry.provider_records(),
        "capabilities": [c.__dict__ for c in registry.capabilities],
        "policies": [{"id": p.id, "label": p.label, "description": p.description, "weights": p.weights, "constraints": p.constraints} for p in registry.policies],
    }
    graph_hash = hashlib.sha256(canonical_json(graph).encode()).hexdigest()
    return {
        "schema": "pluginos.lock.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_versions": registry.source_versions,
        "provider_count": len(registry.providers),
        "capability_count": len(registry.capabilities),
        "policy_count": len(registry.policies),
        "graph_sha256": graph_hash,
    }

def write_lock(registry: Registry, path: Path) -> dict:
    lock = build_lock(registry)
    path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    return lock

def diff_locks(a: dict, b: dict) -> dict:
    keys = sorted(set(a) | set(b))
    return {k: {"from": a.get(k), "to": b.get(k)} for k in keys if a.get(k) != b.get(k)}
