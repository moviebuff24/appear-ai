# Appear AI

## What this is
Public site and client deliverables for Appear AI — an AI SEO/GEO (Generative Engine Optimization) audit agency targeting dental practices, run by Joe under Kazz Tech Holdings LLC. Audit-first model: free/cheap AI-visibility audit → retainer ($1,000–2,000/month).

For Joe's full business context (LLC details, Calendly/Formspree accounts, positioning history, outreach status) see the workspace root `../.claude/memory.md` and `../.claude/CLAUDE.md`.

## Live site
- **URL:** https://appearai.co
- **Repo:** `github.com/moviebuff24/appear-ai`, deployed via GitHub Pages on push to `main`
- **Local source:** this folder (`index.html`, `CNAME`, `robots.txt`, `sitemap.xml`)

## Key files
- `index.html` — the landing page. Navy/orange theme, Plus Jakarta Sans + Inter fonts, GA4 wired (`G-HNP161FMD5`)
- `sample-report.html` — generic sample audit report, publicly linked from the site
- `aspire-audit-2026.html` — real client deliverable for Jason (Aspire Orthodontics & Airway) — **do not edit casually**, it's a live reference a real client has seen
- `teaser-report-template.html` — canonical template for cold-outreach teaser reports (blurred/locked sections, frosted-glass CTA). Fill `[[TOKENS]]` in the FILL comment block per prospect
- `teaser-*.html` (DiPilla, Premier, Aligned House, TDR, Family Dentistry Royal Oak) — filled prospect teasers, `.gitignore`'d from the public repo so they stay private until sent
- `templates/` — monthly/quarterly client report templates (Chart.js-based)
- `tracker.py` — queries Claude, ChatGPT Search, and Perplexity Sonar for AI-visibility data (~$0.11/run). Needs `pip install anthropic openai` plus `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `PERPLEXITY_API_KEY` env vars

## Conventions
- Follow the workspace UI style guide (`../.claude/style-guide.md`) for any new tool/export — Archetype B (Document) fits report-style pages
- Joe will not send outreach copy that reads as AI-generated — no em dashes, vary sentence length, no stock phrases ("worth a 2-minute look," "yours to keep either way"), no forward-me P.S.
- Reviews are a secondary signal in all client-facing materials — lead with AI-platform visibility, never lead with review counts
- Verify contact emails against the practice's own site before using them — scraper-sourced contacts have been wrong before (wrong city, wrong person, generic inbox)
- Two standing conflicts: don't contact Profound Orthodontics (Aspire's direct competitor) or push hard on Aligned House of Orthodontics without checking with Joe (airway focus overlaps Aspire's differentiator)
