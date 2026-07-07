"""SQLite helpers — build a queryable database from the CSV store.

data/matches.csv is the canonical, git-friendly store.
data/sports.db is a local convenience for practicing SQL (notebooks, RStudio, DBeaver).

Rebuild it any time:   python -m src.common.db
"""
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
CSV = DATA / "matches.csv"
DB = DATA / "sports.db"


def load_matches() -> pd.DataFrame:
    if not CSV.exists():
        return pd.DataFrame()
    return pd.read_csv(CSV, parse_dates=["date"], dtype={"match_id": str})


def build_db() -> None:
    df = load_matches()
    if df.empty:
        print("No data yet — run: python -m src.soccer.fetch_espn")
        return
    DATA.mkdir(exist_ok=True)
    with sqlite3.connect(DB) as con:
        df.to_sql("matches", con, if_exists="replace", index=False)
        con.execute("CREATE INDEX IF NOT EXISTS idx_matches_league ON matches(league)")
    print(f"Built {DB.name} with {len(df):,} matches. Try:")
    print('  SELECT league_name, COUNT(*) FROM matches GROUP BY 1 ORDER BY 2 DESC;')


if __name__ == "__main__":
    build_db()
