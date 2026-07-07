"""Compute a league table from finished matches — pure pandas, no API.

This is your first 'stats brain' module: the app and the notebook both import it.
"""
import pandas as pd


def league_table(matches: pd.DataFrame) -> pd.DataFrame:
    """P/W/D/L/GF/GA/GD/Pts table from a matches dataframe (one league)."""
    df = matches[matches["completed"] == True].copy()  # noqa: E712
    if df.empty:
        return pd.DataFrame()
    df["home_score"] = pd.to_numeric(df["home_score"], errors="coerce")
    df["away_score"] = pd.to_numeric(df["away_score"], errors="coerce")
    df = df.dropna(subset=["home_score", "away_score"])

    rows = []
    for m in df.itertuples():
        rows.append({"team": m.home_team, "gf": m.home_score, "ga": m.away_score})
        rows.append({"team": m.away_team, "gf": m.away_score, "ga": m.home_score})
    t = pd.DataFrame(rows)

    g = t.groupby("team").agg(P=("gf", "size"), GF=("gf", "sum"), GA=("ga", "sum"))
    g["W"] = t[t.gf > t.ga].groupby("team").size()
    g["D"] = t[t.gf == t.ga].groupby("team").size()
    g["L"] = t[t.gf < t.ga].groupby("team").size()
    g = g.fillna(0).astype(int)
    g["GD"] = g.GF - g.GA
    g["Pts"] = 3 * g.W + g.D

    cols = ["team", "P", "W", "D", "L", "GF", "GA", "GD", "Pts"]
    return (
        g.reset_index()[cols]
        .sort_values(["Pts", "GD", "GF"], ascending=False)
        .reset_index(drop=True)
    )
