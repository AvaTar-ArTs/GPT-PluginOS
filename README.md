# GPT-PluginOS

> A federated capability control plane for discovering, comparing, routing, governing, and explaining the provider ecosystem around AvaTar-ArTs agents, skills, plugins, tools, and creative infrastructure.

GPT-PluginOS answers a deceptively hard question:

> **Given an intent, which capability is needed, which providers can satisfy it, and which route is best under current quality, privacy, cost, risk, health, and project constraints?**

It is not another agent runtime and not another plugin list.

## Field site

A dependency-free static field site now lives in [`site/`](site/):

- [`site/index.html`](site/index.html) — product command center and capability-routing demo
- [`site/advanced.html`](site/advanced.html) — advanced routing, governance, creator, engineering, research, benchmark, and drift scenarios
- [`site/market.html`](site/market.html) — market positioning, sellable offers, SaaS ladder, revenue flywheel, launch channels, and commercialization roadmap

Preview locally:

```bash
python -m http.server 8080 --directory site
```

The field site is intentionally dependency-free and presents architecture/reference behavior. It does not imply that every illustrated future CLI or automation capability is already implemented.
