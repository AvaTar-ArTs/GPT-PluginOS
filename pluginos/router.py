from __future__ import annotations
from .models import Provider, Policy, RouteCandidate, RouteResult
from .registry import Registry

class Router:
    def __init__(self, registry: Registry): self.registry = registry

    @staticmethod
    def _quality(value: float) -> float: return max(0.0, min(5.0, value / 2.0))
    @staticmethod
    def _cost(value: float) -> float: return max(0.0, 5.0 - value)
    @staticmethod
    def _health(status: str) -> float:
        return {"healthy": 5.0, "connected": 5.0, "installed": 4.0, "available": 4.0, "degraded": 2.0, "deprecated": 1.0}.get(status, 0.0)

    def eligible(self, capability: str, policy: Policy) -> list[Provider]:
        out = []
        for p in self.registry.providers:
            if capability not in p.capabilities: continue
            c = policy.constraints
            if c.get("localOnly") and p.kind not in {"local", "first_party"}: continue
            if c.get("maxCost") is not None and p.cost > float(c["maxCost"]): continue
            if c.get("excludeDegraded") and p.status == "degraded": continue
            if c.get("readOnly") and p.risk != "read_only": continue
            out.append(p)
        return out

    def score(self, provider: Provider, policy: Policy) -> RouteCandidate:
        comp = {
            "quality": self._quality(provider.quality),
            "privacy": max(0.0, min(5.0, provider.privacy)),
            "latency": max(0.0, min(5.0, provider.latency)),
            "cost": self._cost(provider.cost),
            "health": self._health(provider.status),
        }
        score = sum(comp[k] * policy.weights[k] for k in policy.weights)
        return RouteCandidate(provider, score, comp)

    def route(self, capability: str, policy_id: str = "balanced") -> RouteResult:
        if capability not in self.registry.capability_by_id:
            return RouteResult(capability, policy_id, (), f"unknown capability: {capability}")
        if policy_id not in self.registry.policy_by_id:
            return RouteResult(capability, policy_id, (), f"unknown policy: {policy_id}")
        policy = self.registry.policy_by_id[policy_id]
        candidates = [self.score(p, policy) for p in self.eligible(capability, policy)]
        candidates.sort(key=lambda c: (-c.score, -c.provider.quality, c.provider.id))
        if not candidates:
            return RouteResult(capability, policy_id, (), "no eligible provider under current policy; constraints were not widened")
        return RouteResult(capability, policy_id, tuple(candidates))
