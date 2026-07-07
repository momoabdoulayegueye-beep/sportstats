"""Fetch match results for every league in config.yaml from ESPN's public JSON API.

No API key required. Run from the repo root:

    python -m src.soccer.fetch_espn             # last N days (config: default_days_back)
    python -m src.soccer.fetch_espn --days 60   # deeper backfill
    python -m src.soccer.fetch_espn --league fifa.world --days 30
"""
import argparse
import sys
import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests
import yaml

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / "data" / "matches.csv"
URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard"


def load_config() -> dict:
    with open(ROOT / "config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def parse_event(ev: dict, league_code: str, league_name: str) -> dict | None:
    """Turn one ESPN 'event' into a flat match row. Defensive: returns None on odd shapes."""
    comp = (ev.get("competitions") or [{}])[0]
    status = (ev.get("status") or {}).get("type") or {}
    home = away = None
    for c in comp.get("competitors", []):
        side = {
            "team": (c.get("team") or {}).get("displayName"),
            "score": c.get("score"),
        }
        if c.get("homeAway") == "home":
            home = side
        elif c.get("homeAway") == "away":
            away = side
    if not home or not away:
        return None
    return {
        "match_id": str(ev.get("id")),
        "league": league_code,
        "league_name": league_name,
        "date": (ev.get("date") or "")[:10],
        "home_team": home["team"],
        "away_team": away["team"],
        "home_score": home["score"],
        "away_score": away["score"],
        "status": status.get("state"),          # pre | in | post
        "completed": bool(status.get("completed")),
        "venue": (comp.get("venue") or {}).get("fullName"),
    }


def fetch_league(code: str, name: str, start: date, end: date, session: requests.Session) -> list[dict]:
    """One request per league: ESPN accepts a date *range* in ?dates=."""
    params = {"dates": f"{start:%Y%m%d}-{end:%Y%m%d}", "limit": 350}
    r = session.get(URL.format(league=code), params=params, timeout=25)
    r.raise_for_status()
    events = r.json().get("events", [])
    rows = [parse_event(e, code, name) for e in events]
    return [row for row in rows if row]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--days", type=int, default=None, help="how many days back to fetch")
    ap.add_argument("--league", default=None, help="fetch a single ESPN league code")
    args = ap.parse_args()

    cfg = load_config()
    leagues: dict = cfg["soccer"]
    if args.league:
        leagues = {args.league: leagues.get(args.league, args.league)}
    days = args.days or cfg.get("default_days_back", 14)
    start, end = date.today() - timedelta(days=days), date.today() + timedelta(days=7)

    rows: list[dict] = []
    session = requests.Session()
    session.headers["User-Agent"] = "sportstats-student-project"
    for code, name in leagues.items():
        try:
            found = fetch_league(code, name, start, end, session)
            rows += found
            print(f"{name:28s} {len(found):4d} matches")
        except Exception as exc:  # keep going if one league fails
            print(f"  ! {code}: {exc}", file=sys.stderr)
        time.sleep(0.4)  # be polite

    if not rows:
        print("Nothing fetched — check your connection and league codes.")
        return

    new = pd.DataFrame(rows)
    if CSV.exists():
        old = pd.read_csv(CSV, dtype={"match_id": str})
        merged = pd.concat([old, new]).drop_duplicates("match_id", keep="last")
    else:
        merged = new
    CSV.parent.mkdir(exist_ok=True)
    merged.sort_values(["league", "date"]).to_csv(CSV, index=False)
    print(f"\nSaved {len(merged):,} total matches -> {CSV.relative_to(ROOT)}")
    print("Next: build the SQL practice db with  python -m src.common.db")


if __name__ == "__main__":
    main()
