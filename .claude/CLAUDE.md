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
- `teaser-*.html` (DiPilla, Premier Birmingham, Premier Dental Center, Aligned House, TDR, Family Dentistry Royal Oak) — filled prospect teasers. ⚠️ **These are tracked and therefore PUBLIC at appearai.co** — despite older notes claiming they were gitignored, `.gitignore` only ever covered the template and sample draft. Verified Sep 2026, left as-is by Joe. Unsent teasers belong in the private `appear-ai-internal` repo instead
- `templates/` — monthly/quarterly client report templates (Chart.js-based)
- `ai-visibility-audit.py` — **the audit data collector. Use this, not `tracker.py`.** Lives in the private `appear-ai-internal` repo. Runs a practice's query set against the live answer engines and records rank position, citations, entity name used, and stated rationale per cell. See "Running an audit" below
- `tracker.py` — the original v1 checker (binary appeared/not-appeared, hardcoded to a sample practice). Superseded by `ai-visibility-audit.py`; kept for reference

## Running an audit — the API keys are live, don't ask Joe to paste results

All three API keys are set as Windows user env vars and verified working (Sep 2026):
`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `PERPLEXITY_API_KEY`. Python 3.12 + `anthropic` 1.x + `openai` 3.x installed.

```
cd appear-ai-internal && python ai-visibility-audit.py --practice aspire
```

Add a practice by appending to the `PRACTICES` dict (name, location, aliases, queries, prior baselines).
Results land in `appear-ai-internal/results/<practice>-<timestamp>.json` with full answer text per cell.
**The script and `results/` live in the PRIVATE repo `moviebuff24/appear-ai-internal`, not here** —
this repo is public and serves appearai.co, so raw client answers must never be committed to it.

**Platform coverage — three of four are automated:**

| Cell | How it's collected | Model / API |
|---|---|---|
| Claude | automated | `claude-opus-5` + server-side `web_search_20260209` |
| ChatGPT | automated | `gpt-5-search-api` (chat.completions) — **6,000 TPM cap**, script sleeps 70s between queries |
| Perplexity | automated | `sonar` — returns `citations` + `search_results`, the richest citation layer of the three |
| **Google AI Mode** | **manual — no API exists** | see below |

**Google is the one genuine gap** (verified Sep 2026, re-check before assuming it still holds):
- There is **no official Google API** returning AI Overviews / AI Mode answers.
- Search Console *does* have a Generative AI performance report (shipped Jun 3 2026, worldwide Aug 31 2026) — but it is **UI-only**: the Search Analytics API rejects `aiMode`/`aiOverview`/`generativeAi` as a `type` value, and BigQuery bulk export doesn't carry it either. It also reports *impressions by page*, not rank-within-answer, and has no query detail — so it would not fill these cells even with API access. And it needs the client to grant property access.
- Options if Google matters for a given report: have Joe run the 4 queries by hand (~5 min), or buy a third-party SERP API that scrapes AI Overviews (SerpApi, SearchAPI, Searlo, Apify, cloro) and add it as a fourth platform.

**Reading the output:** an API answer is not byte-identical to the consumer product — different system prompts, no account personalization, no location signal. Treat an automated run as a **new baseline series**, comparable to other automated runs; say so in the report rather than splicing it onto the hand-collected May/Aug 2026 numbers as if it were the same series.

**Cost:** roughly $0.50–1.50 per full 12-cell run (Opus 5 web search dominates). Not free — don't loop it casually.

## Conventions
- Follow the workspace UI style guide (`../.claude/style-guide.md`) for any new tool/export — Archetype B (Document) fits report-style pages
- Joe will not send outreach copy that reads as AI-generated — no em dashes, vary sentence length, no stock phrases ("worth a 2-minute look," "yours to keep either way"), no forward-me P.S.
- Reviews are a secondary signal in all client-facing materials — lead with AI-platform visibility, never lead with review counts
- Verify contact emails against the practice's own site before using them — scraper-sourced contacts have been wrong before (wrong city, wrong person, generic inbox)
- Two standing conflicts: don't contact Profound Orthodontics (Aspire's direct competitor) or push hard on Aligned House of Orthodontics without checking with Joe (airway focus overlaps Aspire's differentiator)
