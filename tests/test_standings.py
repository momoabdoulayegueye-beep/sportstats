"""Sanity checks for the standings math. Run:  python tests/test_standings.py"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.soccer.standings import league_table

matches = pd.DataFrame([
    # A beats B 2-0 | B draws C 1-1 | C beats A 3-1
    dict(home_team="A", away_team="B", home_score=2, away_score=0, completed=True),
    dict(home_team="B", away_team="C", home_score=1, away_score=1, completed=True),
    dict(home_team="C", away_team="A", home_score=3, away_score=1, completed=True),
    dict(home_team="A", away_team="C", home_score=0, away_score=0, completed=False),  # ignored
])

t = league_table(matches).set_index("team")

assert list(t.columns) == ["P", "W", "D", "L", "GF", "GA", "GD", "Pts"]
assert t.loc["A", "Pts"] == 3 and t.loc["A", "P"] == 2
assert t.loc["B", "Pts"] == 1 and t.loc["B", "GD"] == -2
assert t.loc["C", "Pts"] == 4 and t.loc["C", "GF"] == 4
assert t.index[0] == "C"  # C tops the table
assert int(t.P.sum()) == 6  # 3 finished matches x 2 teams

print("All standings checks passed ✔")
