from __future__ import annotations
import argparse, json, sys
from importlib.resources import files
from pathlib import Path
from . import __version__
from .audit import audit_registry
from .compile import compile_registry
from .lockfile import diff_locks, write_lock
from .registry import Registry
from .router import Router

def _registry(args):
    return Registry.from_directory(Path(args.data_dir)) if args.data_dir else Registry.bundled()

def _json(value):
    print(json.dumps(value, indent=2, sort_keys=True))

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="pluginos", description="GPT-PluginOS capability control plane")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--data-dir", help="override registry data directory")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    scan = sub.add_parser("scan"); scan.add_argument("--json", action="store_true")
    providers = sub.add_parser("providers"); providers.add_argument("--json", action="store_true")
    capabilities = sub.add_parser("capabilities"); capabilities.add_argument("--json", action="store_true")
    route = sub.add_parser("route"); route.add_argument("capability"); route.add_argument("--policy", default="balanced"); route.add_argument("--json", action="store_true")
    explain = sub.add_parser("explain"); explain.add_argument("capability"); explain.add_argument("--policy", default="balanced")
    compile_cmd = sub.add_parser("compile"); compile_cmd.add_argument("--output")
    lock = sub.add_parser("lock"); lock.add_argument("--output", default="pluginos.lock.json")
    diff = sub.add_parser("diff"); diff.add_argument("left"); diff.add_argument("right")
    graph = sub.add_parser("graph"); graph.add_argument("--format", choices=["mermaid", "json"], default="mermaid")
    overlaps = sub.add_parser("overlaps"); overlaps.add_argument("--json", action="store_true")
    benchmark = sub.add_parser("benchmark"); benchmark.add_argument("suite"); benchmark.add_argument("--policy", default="balanced"); benchmark.add_argument("--json", action="store_true")
    export_site = sub.add_parser("export-site"); export_site.add_argument("directory")
    sub.add_parser("audit")
    args = parser.parse_args(argv)
    try:
        if args.command == "diff":
            left = json.loads(Path(args.left).read_text())
            right = json.loads(Path(args.right).read_text())
            _json(diff_locks(left, right))
            return 0
        registry = _registry(args)
        if args.command == "validate":
            print(f"OK: {len(registry.providers)} providers, {len(registry.capabilities)} capabilities, {len(registry.policies)} policies")
            return 0
        if args.command == "scan":
            payload = {"source_versions": registry.source_versions, "providers": len(registry.providers), "capabilities": len(registry.capabilities), "policies": len(registry.policies), "status_counts": {}}
            for provider in registry.providers:
                payload["status_counts"][provider.status] = payload["status_counts"].get(provider.status, 0) + 1
            if args.json:
                _json(payload)
            else:
                print(f"providers: {payload['providers']}")
                print(f"capabilities: {payload['capabilities']}")
                print(f"policies: {payload['policies']}")
                print("status: " + ", ".join(f"{k}={v}" for k, v in sorted(payload["status_counts"].items())))
            return 0
        if args.command == "providers":
            records = registry.provider_records()
            if args.json: _json(records)
            else:
                for row in records: print(f"{row['id']}\t{row['status']}\t{row['category']}\t{row['risk']}")
            return 0
        if args.command == "capabilities":
            records = [c.__dict__ for c in registry.capabilities]
            if args.json: _json(records)
            else:
                for row in records: print(f"{row['id']}\t{row['label']}")
            return 0
        if args.command in {"route", "explain"}:
            result = Router(registry).route(args.capability, args.policy)
            payload = {
                "capability": result.capability,
                "policy": result.policy,
                "selected": result.selected.provider.id if result.selected else None,
                "diagnostic": result.diagnostic,
                "authorization_implied": False,
                "candidates": [{"provider": c.provider.id, "score": round(c.score, 6), "risk": c.provider.risk, "components": c.components} for c in result.candidates],
            }
            if getattr(args, "json", False) or args.command == "explain": _json(payload)
            else:
                if payload["selected"]: print(f"{payload['selected']}\t{payload['candidates'][0]['score']:.3f}\t{payload['candidates'][0]['risk']}")
                else:
                    print(payload["diagnostic"], file=sys.stderr)
                    return 2
            return 0 if payload["selected"] else 2
        if args.command == "compile":
            payload = compile_registry(registry)
            text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
            if args.output: Path(args.output).write_text(text)
            else: print(text, end="")
            return 0
        if args.command == "lock":
            _json(write_lock(registry, Path(args.output)))
            return 0
        if args.command == "overlaps":
            payload = {c.id: [p.id for p in registry.providers if c.id in p.capabilities] for c in registry.capabilities}
            payload = {k: v for k, v in payload.items() if len(v) > 1}
            if args.json: _json(payload)
            else:
                for capability_id, provider_ids in sorted(payload.items()): print(f"{capability_id}\t{','.join(provider_ids)}")
            return 0
        if args.command == "benchmark":
            matches = [c.id for c in registry.capabilities if c.id == args.suite or c.domain == args.suite]
            if not matches:
                print(f"pluginos: unknown benchmark suite/domain: {args.suite}", file=sys.stderr)
                return 2
            router = Router(registry)
            payload = {}
            for capability_id in matches:
                result = router.route(capability_id, args.policy)
                payload[capability_id] = [{"provider": c.provider.id, "score": round(c.score, 6), "quality": c.provider.quality, "privacy": c.provider.privacy, "latency": c.provider.latency, "cost": c.provider.cost, "health": c.provider.status} for c in result.candidates]
            if args.json: _json({"suite": args.suite, "policy": args.policy, "mode": "metadata_snapshot", "results": payload})
            else:
                for capability_id, rows in payload.items():
                    print(f"[{capability_id}]")
                    for row in rows: print(f"{row['provider']}\t{row['score']:.3f}\tquality={row['quality']}\tstatus={row['health']}")
            return 0
        if args.command == "export-site":
            out = Path(args.directory); out.mkdir(parents=True, exist_ok=True)
            for name in ("providers.json", "capabilities.json", "policies.json"):
                src = files("pluginos").joinpath("data", name)
                (out / name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            (out / "compiled.json").write_text(json.dumps(compile_registry(registry), indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(f"exported runtime datasets to {out}")
            return 0
        if args.command == "audit":
            _json(audit_registry(registry))
            return 0
        if args.command == "graph":
            if args.format == "json":
                _json({c.id: [p.id for p in registry.providers if c.id in p.capabilities] for c in registry.capabilities})
                return 0
            print("graph LR")
            for capability in registry.capabilities:
                cid = capability.id.replace('.', '_').replace('-', '_')
                print(f'  {cid}["{capability.id}"]')
                for provider in registry.providers:
                    if capability.id in provider.capabilities:
                        print(f'  {cid} --> p_{provider.id.replace("-", "_")}["{provider.name}"]')
            return 0
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"pluginos: {exc}", file=sys.stderr)
        return 1
    return 1
