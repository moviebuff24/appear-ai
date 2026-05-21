"""
Appear AI — Visibility Tracker
Checks how often a dental practice appears in AI platform responses.
Run: python tracker.py
"""

import os
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# ── CONFIG ────────────────────────────────────────────────────────────────────
PRACTICE_NAME = "Maple Street Dental"
LOCATION = "Royal Oak, MI"

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

QUERIES = [
    "Best dentist near {location}",
    "Top-rated dental office in {location}",
    "Who are the best dentists in {location}?",
]

RESULTS_DIR = Path(__file__).parent / "results"

# ── COST ESTIMATES (per query) ─────────────────────────────────────────────────
COST_CLAUDE_PER_QUERY = 0.001     # Haiku 4.5 — very cheap
COST_PERPLEXITY_PER_QUERY = 0.005  # Sonar web search
COST_CHATGPT_PER_QUERY = 0.030    # gpt-4o-search-preview: $30/1000 searches + token costs

# ── DEPENDENCY CHECK ──────────────────────────────────────────────────────────
def check_deps():
    missing = []
    try:
        import anthropic  # noqa: F401
    except ImportError:
        missing.append("anthropic")
    try:
        from openai import OpenAI  # noqa: F401
    except ImportError:
        missing.append("openai")
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        sys.exit(1)

# ── COMPETITOR EXTRACTION ─────────────────────────────────────────────────────
def extract_competitors(text: str, exclude: str) -> list[str]:
    """Pull out capitalized dental practice names from response text."""
    dental_keywords = re.compile(
        r"\b(?:[A-Z][a-z]+ )+(?:Dental|Dentistry|Orthodontics|Smiles|Family Dental|Dental Care)\b"
    )
    matches = dental_keywords.findall(text)
    seen = []
    for m in matches:
        name = m.strip()
        if name.lower() != exclude.lower() and name not in seen:
            seen.append(name)
        if len(seen) >= 3:
            break
    return seen

# ── CLAUDE QUERY ──────────────────────────────────────────────────────────────
def query_claude(query: str) -> dict:
    import anthropic

    if not ANTHROPIC_API_KEY:
        return {"error": "ANTHROPIC_API_KEY not set", "text": ""}

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            system=(
                "You are a helpful local search assistant. When asked about dental practices "
                "in a specific area, provide a realistic list of well-known local options with "
                "brief descriptions, as if you were answering a patient's question."
            ),
            messages=[{"role": "user", "content": query}],
        )
        text = response.content[0].text
        return {"text": text, "error": None}
    except Exception as e:
        return {"text": "", "error": str(e)}

# ── CHATGPT QUERY (with web search) ──────────────────────────────────────────
def query_chatgpt(query: str) -> dict:
    from openai import OpenAI

    if not OPENAI_API_KEY:
        return {"error": "OPENAI_API_KEY not set", "text": ""}

    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-search-preview",
            web_search_options={},
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful local search assistant. Answer questions about local dental practices accurately based on real web results.",
                },
                {"role": "user", "content": query},
            ],
        )
        text = response.choices[0].message.content
        return {"text": text, "error": None}
    except Exception as e:
        return {"text": "", "error": str(e)}

# ── PERPLEXITY QUERY ──────────────────────────────────────────────────────────
def query_perplexity(query: str) -> dict:
    from openai import OpenAI

    if not PERPLEXITY_API_KEY:
        return {"error": "PERPLEXITY_API_KEY not set", "text": ""}

    client = OpenAI(
        api_key=PERPLEXITY_API_KEY,
        base_url="https://api.perplexity.ai",
    )
    try:
        response = client.chat.completions.create(
            model="sonar",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful local search assistant. Answer questions about local dental practices accurately based on real web results.",
                },
                {"role": "user", "content": query},
            ],
            max_tokens=512,
        )
        text = response.choices[0].message.content
        return {"text": text, "error": None}
    except Exception as e:
        return {"text": "", "error": str(e)}

# ── MAIN RUN ──────────────────────────────────────────────────────────────────
def run():
    check_deps()
    RESULTS_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now()
    ts_str = timestamp.strftime("%Y-%m-%d_%H%M%S")
    ts_iso = timestamp.isoformat()

    platforms = [
        ("Claude (Haiku)", query_claude),
        ("ChatGPT (Search)", query_chatgpt),
        ("Perplexity (Sonar)", query_perplexity),
    ]

    results = []
    rows = []  # for terminal table

    print(f"\n  Appear AI · Visibility Tracker")
    print(f"  Practice : {PRACTICE_NAME}")
    print(f"  Location : {LOCATION}")
    print(f"  Run time : {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    for platform_name, query_fn in platforms:
        for query_template in QUERIES:
            query = query_template.format(location=LOCATION)
            print(f"  Querying {platform_name}: \"{query}\" ...", end=" ", flush=True)

            result = query_fn(query)
            text = result["text"]
            error = result["error"]

            appeared = PRACTICE_NAME.lower() in text.lower() if text else False
            competitors = extract_competitors(text, PRACTICE_NAME) if text else []
            snippet = text[:200].replace("\n", " ") + ("..." if len(text) > 200 else "")

            status = "✓" if appeared else "✗"
            print(status)

            results.append({
                "platform": platform_name,
                "query": query,
                "appeared": appeared,
                "response_snippet": snippet,
                "competitors_seen": competitors,
                "error": error,
            })
            rows.append((platform_name, query, appeared, competitors))

    # ── SUMMARY TABLE ─────────────────────────────────────────────────────────
    col_w = [22, 44, 9, 32]
    divider = "  " + "-" * (sum(col_w) + len(col_w) * 3 + 1)
    header = ("  | " +
              " | ".join([
                  "Platform".ljust(col_w[0]),
                  "Query".ljust(col_w[1]),
                  "Appeared".ljust(col_w[2]),
                  "Competitors Seen".ljust(col_w[3]),
              ]) + " |")

    print()
    print(f"\n  ── Results for: {PRACTICE_NAME} ──")
    print(divider)
    print(header)
    print(divider)
    for platform, query, appeared, competitors in rows:
        comp_str = ", ".join(competitors) if competitors else "—"
        appeared_str = ("  YES ✓" if appeared else "  no  ✗").ljust(col_w[2])
        print("  | " + " | ".join([
            platform.ljust(col_w[0]),
            query.ljust(col_w[1]),
            appeared_str,
            comp_str[:col_w[3]].ljust(col_w[3]),
        ]) + " |")
    print(divider)

    appeared_count = sum(1 for r in results if r["appeared"])
    total = len(results)
    score = round((appeared_count / total) * 10) if total else 0
    print(f"\n  Visibility score: {appeared_count}/{total} queries · {score}/10")

    # ── COST ESTIMATE ──────────────────────────────────────────────────────────
    n_queries = len(QUERIES)
    cost = (n_queries * COST_CLAUDE_PER_QUERY) + (n_queries * COST_CHATGPT_PER_QUERY) + (n_queries * COST_PERPLEXITY_PER_QUERY)
    print(f"  Est. cost this run: ${cost:.3f}")

    # ── SAVE JSON ──────────────────────────────────────────────────────────────
    output = {
        "timestamp": ts_iso,
        "practice": PRACTICE_NAME,
        "location": LOCATION,
        "score": score,
        "appeared_count": appeared_count,
        "total_queries": total,
        "results": results,
    }
    out_path = RESULTS_DIR / f"{ts_str}.json"
    out_path.write_text(json.dumps(output, indent=2))
    print(f"\n  Results saved → results/{ts_str}.json\n")


if __name__ == "__main__":
    run()
