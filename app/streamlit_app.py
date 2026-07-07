"""SportStats — interactive multi-league explorer.

Run from the repo root:   streamlit run app/streamlit_app.py
"""
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.soccer.standings import league_table  # noqa: E402

st.set_page_config(page_title="SportStats", page_icon="⚽", layout="wide")


@st.cache_data(ttl=600)
def load() -> pd.DataFrame:
    csv = ROOT / "data" / "matches.csv"
    if not csv.exists():
        return pd.DataFrame()
    return pd.read_csv(csv, parse_dates=["date"], dtype={"match_id": str})


df = load()
st.title("⚽ SportStats — multi-league explorer")

if df.empty:
    st.warning("No data yet. From the repo root run  `python -m src.soccer.fetch_espn`  then refresh this page.")
    st.stop()

names = df[["league", "league_name"]].drop_duplicates().set_index("league")["league_name"].to_dict()
code = st.sidebar.selectbox("League", options=list(names), format_func=names.get)
sub = df[df.league == code].sort_values("date", ascending=False)

st.sidebar.metric("Matches stored", len(sub))
if len(sub):
    st.sidebar.caption(f"Latest match date: {sub.date.max():%d %b %Y}")

results_tab, table_tab, charts_tab = st.tabs(["Results", "Table", "Charts"])

with results_tab:
    played = sub[sub.completed == True]  # noqa: E712
    upcoming = sub[sub.status == "pre"].sort_values("date")
    if played.empty:
        st.info("No finished matches stored for this league yet (off-season?).")
    else:
        st.dataframe(
            played[["date", "home_team", "home_score", "away_score", "away_team", "venue"]],
            use_container_width=True, hide_index=True,
        )
    if not upcoming.empty:
        st.subheader("Upcoming")
        st.dataframe(upcoming[["date", "home_team", "away_team", "venue"]],
                     use_container_width=True, hide_index=True)

with table_tab:
    table = league_table(sub)
    if table.empty:
        st.info("Table appears once finished matches are stored.")
    else:
        table.index = table.index + 1  # rank from 1
        st.dataframe(table, use_container_width=True)

with charts_tab:
    played = sub[sub.completed == True].copy()  # noqa: E712
    if played.empty:
        st.info("Nothing to chart yet.")
    else:
        played["total_goals"] = (
            pd.to_numeric(played.home_score, errors="coerce")
            + pd.to_numeric(played.away_score, errors="coerce")
        )
        daily = played.groupby(played.date.dt.date).total_goals.mean().reset_index()
        fig = px.line(daily, x="date", y="total_goals", markers=True,
                      title="Average goals per match, by day")
        st.plotly_chart(fig, use_container_width=True)

        top = league_table(sub).head(10)
        if not top.empty:
            fig2 = px.bar(top, x="team", y="Pts", title="Points — top 10")
            st.plotly_chart(fig2, use_container_width=True)
