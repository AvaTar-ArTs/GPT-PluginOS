from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

ALLOWED_RISKS = {
    "read_only", "external_write", "destructive_write", "financial",
    "identity_or_access", "publication", "code_change", "deployment",
}
ALLOWED_STATUS = {"discovered", "available", "installed", "connected", "healthy", "degraded", "deprecated", "unavailable", "legacy", "replaced"}

@dataclass(frozen=True)
class Provider:
    id: str
    name: str
    kind: str
    category: str
    status: str
    cost: float
    latency: float
    privacy: float
    quality: float
    risk: str
    capabilities: tuple[str, ...]

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Provider":
        required = {"id","name","kind","category","status","cost","latency","privacy","quality","risk","capabilities"}
        missing = sorted(required - raw.keys())
        if missing:
            raise ValueError(f"provider missing required fields: {', '.join(missing)}")
        if raw["risk"] not in ALLOWED_RISKS:
            raise ValueError(f"provider {raw['id']} has invalid risk {raw['risk']}")
        if raw["status"] not in ALLOWED_STATUS:
            raise ValueError(f"provider {raw['id']} has invalid status {raw['status']}")
        caps = tuple(str(x) for x in raw["capabilities"])
        if not caps:
            raise ValueError(f"provider {raw['id']} has no capabilities")
        return cls(
            id=str(raw["id"]), name=str(raw["name"]), kind=str(raw["kind"]),
            category=str(raw["category"]), status=str(raw["status"]),
            cost=float(raw["cost"]), latency=float(raw["latency"]),
            privacy=float(raw["privacy"]), quality=float(raw["quality"]),
            risk=str(raw["risk"]), capabilities=caps,
        )

@dataclass(frozen=True)
class Capability:
    id: str
    label: str
    domain: str
    description: str = ""

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Capability":
        if not raw.get("id") or not raw.get("label"):
            raise ValueError("capability requires id and label")
        return cls(str(raw["id"]), str(raw["label"]), str(raw.get("domain", "other")), str(raw.get("description", "")))

@dataclass(frozen=True)
class Policy:
    id: str
    label: str
    description: str
    weights: dict[str, float]
    constraints: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Policy":
        weights = {str(k): float(v) for k, v in dict(raw.get("weights", {})).items()}
        expected = {"quality", "privacy", "latency", "cost", "health"}
        if not expected.issubset(weights):
            raise ValueError(f"policy {raw.get('id')} missing weights: {sorted(expected - set(weights))}")
        if sum(weights.values()) <= 0:
            raise ValueError(f"policy {raw.get('id')} has non-positive total weight")
        return cls(str(raw["id"]), str(raw["label"]), str(raw.get("description", "")), weights, dict(raw.get("constraints", {})))

@dataclass(frozen=True)
class RouteCandidate:
    provider: Provider
    score: float
    components: dict[str, float]

@dataclass(frozen=True)
class RouteResult:
    capability: str
    policy: str
    candidates: tuple[RouteCandidate, ...]
    diagnostic: str | None = None

    @property
    def selected(self) -> RouteCandidate | None:
        return self.candidates[0] if self.candidates else None
