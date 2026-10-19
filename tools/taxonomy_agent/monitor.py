"""
EU Taxonomy Amendment Monitor
Checks EUR-Lex for new amendments to Commission Delegated Regulation (EU) 2021/2139.

Usage:
    python monitor.py                    # Check for updates, print report
    python monitor.py --save             # Check and save report to file
    python monitor.py --activity 4.29   # Show full detail for one activity
"""

import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from knowledge_base import ACTIVITIES, SE_TAXONOMY_FY2025, KNOWN_AMENDMENTS, BASE_REGULATION_URL

try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# ─── EUR-Lex Check ────────────────────────────────────────────────────────────

EURLEX_CONSLEG_URL = (
    "https://eur-lex.europa.eu/legal-content/EN/TXT/"
    "?uri=CONSLEG:2021R2139:{date}&from=EN"
)

def check_eurlex_for_updates() -> dict:
    """
    Queries EUR-Lex to check for amendments to 2021/2139 published after
    the last known amendment in our knowledge base.

    Returns a dict with: {checked_at, status, latest_known, new_items, error}
    """
    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "status": "unknown",
        "latest_known_amendment": KNOWN_AMENDMENTS[-1]["date"] if KNOWN_AMENDMENTS else "none",
        "new_items": [],
        "error": None,
    }

    if not REQUESTS_AVAILABLE:
        result["status"] = "offline"
        result["error"] = (
            "requests/beautifulsoup4 not installed. "
            "Run: pip install requests beautifulsoup4 --break-system-packages"
        )
        return result

    try:
        headers = {"User-Agent": "Mozilla/5.0 (thesis-research-tool; emad.okour1@gmail.com)"}
        # Query EUR-Lex for all documents amending 2021/2139
        search_url = (
            "https://eur-lex.europa.eu/search.html"
            "?query=amends+2021%2F2139&type=quick&lang=en&scope=EURLEX"
        )
        resp = requests.get(search_url, headers=headers, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        # Results appear in <li class="result"> elements
        results = soup.select("li.result")

        known_dates = {a["date"] for a in KNOWN_AMENDMENTS}
        new_items = []

        for r in results[:10]:  # Check first 10 results
            date_tag = r.select_one(".date")
            title_tag = r.select_one(".title a")
            if date_tag and title_tag:
                item_date = date_tag.get_text(strip=True)
                item_title = title_tag.get_text(strip=True)
                item_url = "https://eur-lex.europa.eu" + title_tag.get("href", "")
                if item_date not in known_dates:
                    new_items.append({
                        "date": item_date,
                        "title": item_title,
                        "url": item_url,
                    })

        result["status"] = "ok"
        result["new_items"] = new_items
        result["items_found"] = len(results)

    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    return result


# ─── Report Generation ────────────────────────────────────────────────────────

def generate_report(check_result: dict, verbose: bool = False) -> str:
    lines = []
    lines.append("=" * 70)
    lines.append("EU TAXONOMY MONITOR — Commission Delegated Regulation 2021/2139")
    lines.append(f"Report generated: {check_result['checked_at']}")
    lines.append("=" * 70)

    lines.append("\n📋 SE FY2025 TAXONOMY SNAPSHOT")
    lines.append("-" * 40)
    for metric, data in SE_TAXONOMY_FY2025.items():
        if isinstance(data, dict):
            lines.append(
                f"  {metric.upper():8s}  Eligible: {data['eligible_pct']}%   "
                f"Aligned: {data['aligned_pct']}%   Gap: {data['gap_pp']}pp"
            )

    lines.append("\n🔍 EUR-LEX UPDATE CHECK")
    lines.append("-" * 40)
    lines.append(f"  Status:           {check_result['status']}")
    lines.append(f"  Last known amend: {check_result['latest_known_amendment']}")

    if check_result.get("error"):
        lines.append(f"  ⚠️  Error: {check_result['error']}")
    elif check_result["new_items"]:
        lines.append(f"\n  🚨 {len(check_result['new_items'])} NEW ITEM(S) FOUND:")
        for item in check_result["new_items"]:
            lines.append(f"    • [{item['date']}] {item['title']}")
            lines.append(f"      {item['url']}")
    else:
        lines.append("  ✅  No new amendments found beyond known list.")

    lines.append("\n📌 KNOWN AMENDMENTS (cumulative)")
    lines.append("-" * 40)
    for amend in KNOWN_AMENDMENTS:
        lines.append(f"  [{amend['date']}] {amend['amendment']}")
        lines.append(f"    → {amend['summary']}")
        lines.append(f"    → URL: {amend['eurlex_url']}")

    lines.append("\n⚠️  HIGH-PRIORITY MONITORING FLAGS")
    lines.append("-" * 40)
    for act_id, act in ACTIVITIES.items():
        flag = act.get("monitoring_flag")
        if flag:
            lines.append(f"  Activity {act_id} ({act['name'][:45]}...)")
            lines.append(f"    {flag}")

    if verbose:
        lines.append("\n📊 SE-RELEVANT ACTIVITIES — FULL DETAIL")
        lines.append("-" * 40)
        for act_id, act in ACTIVITIES.items():
            lines.append(f"\n  ▸ {act_id}: {act['name']}")
            lines.append(f"    Business Area: {act['business_area']}")
            st = act["se_status"]
            lines.append(
                f"    SE Status: Eligible={st['revenue_eligible']}  "
                f"Aligned={st['revenue_aligned']}"
            )
            lines.append(f"    TSC Threshold: {act['tsc']['threshold']}")
            if isinstance(act["gap_notes"], list):
                for note in act["gap_notes"]:
                    lines.append(f"    Gap: {note}")
            else:
                lines.append(f"    Gap: {act['gap_notes']}")
            lines.append(f"    EUR-Lex ref: {act['eurlex_ref']}")

    lines.append("\n" + "=" * 70)
    return "\n".join(lines)


# ─── Activity Query ───────────────────────────────────────────────────────────

def query_activity(activity_id: str) -> str:
    act = ACTIVITIES.get(activity_id)
    if not act:
        available = ", ".join(ACTIVITIES.keys())
        return f"Activity '{activity_id}' not in knowledge base.\nAvailable: {available}"

    lines = []
    lines.append(f"\n{'=' * 60}")
    lines.append(f"Activity {activity_id}: {act['name']}")
    lines.append(f"{'=' * 60}")
    lines.append(f"Objective:      {act['objective']}")
    lines.append(f"Business Area:  {act['business_area']}")
    lines.append(f"EUR-Lex ref:    {act['eurlex_ref']}")

    st = act["se_status"]
    lines.append(f"\nSE FY2025 Status:")
    lines.append(f"  Revenue eligible: {st['revenue_eligible']}")
    lines.append(f"  Revenue aligned:  {st['revenue_aligned']}")
    lines.append(f"  Note: {st['note']}")

    tsc = act["tsc"]
    lines.append(f"\nTechnical Screening Criteria:")
    lines.append(f"  Description: {tsc['description']}")
    lines.append(f"  Threshold:   {tsc['threshold']}")
    lines.append(f"  Key DNSH criteria:")
    for k, v in tsc["key_dnsh"].items():
        lines.append(f"    • {k}: {v}")

    lines.append(f"\nGap Analysis:")
    gap_notes = act["gap_notes"]
    if isinstance(gap_notes, list):
        for note in gap_notes:
            lines.append(f"  • {note}")
    else:
        lines.append(f"  • {gap_notes}")

    if act.get("monitoring_flag"):
        lines.append(f"\n⚠️  Monitoring flag: {act['monitoring_flag']}")

    if act.get("amendments"):
        lines.append(f"\nAmendments affecting this activity:")
        for a in act["amendments"]:
            lines.append(f"  • {a}")

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="EU Taxonomy 2021/2139 monitor and query tool"
    )
    parser.add_argument(
        "--activity", "-a",
        help="Show full detail for a specific activity (e.g. 4.29)"
    )
    parser.add_argument(
        "--save", "-s",
        action="store_true",
        help="Save report to reports/ directory"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Include full activity detail in report"
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Skip EUR-Lex check, use knowledge base only"
    )
    args = parser.parse_args()

    # Single activity query
    if args.activity:
        print(query_activity(args.activity))
        return

    # Update check + report
    if args.offline:
        check_result = {
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "status": "offline (--offline flag set)",
            "latest_known_amendment": KNOWN_AMENDMENTS[-1]["date"],
            "new_items": [],
            "error": None,
        }
    else:
        print("Checking EUR-Lex for updates...")
        check_result = check_eurlex_for_updates()

    report = generate_report(check_result, verbose=args.verbose)
    print(report)

    if args.save:
        reports_dir = Path(__file__).parent / "reports"
        reports_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        out_path = reports_dir / f"taxonomy_monitor_{timestamp}.txt"
        out_path.write_text(report)
        print(f"\nReport saved: {out_path}")


if __name__ == "__main__":
    main()
