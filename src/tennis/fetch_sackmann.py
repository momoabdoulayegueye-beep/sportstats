"""Tennis module — downloads Jeff Sackmann's ATP/WTA match CSVs (free, no key).

Run from the repo root:   python -m src.tennis.fetch_sackmann
"""
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "tennis"
BASE = "https://raw.githubusercontent.com/JeffSackmann/{repo}/master/{repo}_matches_{year}.csv"

YEARS = [2024, 2025, 2026]
REPOS = ["tennis_atp", "tennis_wta"]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for repo in REPOS:
        for year in YEARS:
            url = BASE.format(repo=repo, year=year)
            r = requests.get(url, timeout=30)
            if r.status_code != 200:
                print(f"skip {repo} {year} (not published yet)")
                continue
            dest = OUT / f"{repo}_{year}.csv"
            dest.write_bytes(r.content)
            print(f"saved {dest.name}  ({len(r.content)//1024} KB)")


if __name__ == "__main__":
    main()
