from __future__ import annotations
import json
from importlib.resources import files
from pathlib import Path
from .models import Provider, Capability, Policy

class Registry:
    def __init__(self, providers: list[Provider], capabilities: list[Capability], policies: list[Policy], source_versions: dict[str,str] | None = None):
        self.providers = tuple(providers)
        self.capabilities = tuple(capabilities)
        self.policies = tuple(policies)
        self.source_versions = source_versions or {}
        self.provider_by_id = {p.id: p for p in self.providers}
        self.capability_by_id = {c.id: c for c in self.capabilities}
        self.policy_by_id = {p.id: p for p in self.policies}
        self.validate()

    @classmethod
    def bundled(cls) -> "Registry":
        base = files("pluginos").joinpath("data")
        return cls.from_directory(Path(str(base)))

    @classmethod
    def from_directory(cls, directory: Path) -> "Registry":
        def load(name: str):
            with (directory / name).open("r", encoding="utf-8") as fh:
                return json.load(fh)
        p_raw, c_raw, pol_raw = load("providers.json"), load("capabilities.json"), load("policies.json")
        versions = {
            "providers": str(p_raw.get("version", "unknown")),
            "capabilities": str(c_raw.get("version", "unknown")),
            "policies": str(pol_raw.get("version", "unknown")),
        }
        return cls(
            [Provider.from_dict(x) for x in p_raw["providers"]],
            [Capability.from_dict(x) for x in c_raw["capabilities"]],
            [Policy.from_dict(x) for x in pol_raw["policies"]],
            versions,
        )

    def validate(self) -> None:
        if len(self.provider_by_id) != len(self.providers): raise ValueError("duplicate provider id")
        if len(self.capability_by_id) != len(self.capabilities): raise ValueError("duplicate capability id")
        if len(self.policy_by_id) != len(self.policies): raise ValueError("duplicate policy id")
        unknown = sorted({cap for p in self.providers for cap in p.capabilities if cap not in self.capability_by_id})
        if unknown: raise ValueError(f"providers reference unknown capabilities: {', '.join(unknown)}")

    def provider_records(self) -> list[dict]:
        return [p.__dict__ | {"capabilities": list(p.capabilities)} for p in self.providers]
