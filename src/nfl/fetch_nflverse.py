"""American football module — downloads the nflverse games file (free, no key).

Run from the repo root:   python -m src.nfl.fetch_nflverse
"""
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "nfl"
URL = "https://github.com/nflverse/nflverse-data/releases/download/games/games.csv"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    r = requests.get(URL, timeout=60)
    r.raise_for_status()
    dest = OUT / "games.csv"
    dest.write_bytes(r.content)
    print(f"saved {dest.name}  ({len(r.content)//1024} KB) — every NFL game since 1999")


if __name__ == "__main__":
    main()
