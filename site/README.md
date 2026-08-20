# GPT-PluginOS Field Site

A dependency-free static product/market field site for GPT-PluginOS.

## Pages

- `index.html` — product command center, architecture, routing demo, ecosystem map
- `advanced.html` — advanced routing, creator, engineering, security, research, benchmarks, drift, and provenance patterns
- `market.html` — positioning, offers, SaaS ladder, revenue flywheel, distribution, content engine, and 90-day commercialization plan

## Local preview

From the repository root:

```bash
python -m http.server 8080 --directory site
```

Then open `http://localhost:8080`.

## Deployment

The site is plain HTML/CSS/JS and can be published with GitHub Pages, Vercel, Netlify, Cloudflare Pages, or any static host.

For GitHub Pages, either:

1. configure Pages to deploy a workflow that copies `site/` into the published artifact, or
2. move/copy the contents to a Pages branch/root if you want the repository itself to act as the site.

The pages intentionally use relative links and no external runtime dependencies.

## Design intent

This site is a product narrative and interactive reference surface, not the PluginOS runtime. Examples describe intended architecture and policy behavior; they must not be read as claims that every illustrated CLI or automation capability is already implemented.
