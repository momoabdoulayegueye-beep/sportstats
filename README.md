# SportStats

Multi-sport statistics platform — a student project. Soccer first (Europe's top 10 leagues + World Cup 2026), with module slots for NFL, tennis, basketball, MMA and boxing.

**Stack:** Python · pandas · Streamlit · Plotly · SQLite · GitHub Actions. All data sources are free, no API keys.

## Project layout

```
sportstats/
├── config.yaml                  # which leagues to track — edit freely
├── requirements.txt
├── src/
│   ├── soccer/fetch_espn.py     # data pipeline (ESPN public API, no key)
│   ├── soccer/standings.py      # league-table math (your first stats module)
│   ├── common/db.py             # builds SQLite from the CSV, for SQL practice
│   ├── tennis/fetch_sackmann.py # ATP/WTA match data (free CSVs)
│   └── nfl/fetch_nflverse.py    # every NFL game since 1999 (free CSV)
├── app/streamlit_app.py         # the interactive website
├── notebooks/explore.qmd        # Quarto notebook — stats playground
├── tests/test_standings.py
├── data/                        # matches.csv lands here (committed to git)
└── .github/workflows/refresh.yml  # fetches new results daily, auto-commits
```

## Quickstart (10 minutes)

```bash
cd sportstats
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m src.soccer.fetch_espn --days 30   # pull real data (~1 min)
python tests/test_standings.py              # sanity check
streamlit run app/streamlit_app.py          # opens the app in your browser
```

Optional: `python -m src.common.db` builds `data/sports.db` so you can practice SQL in the notebook or any SQL client.

## Put it on GitHub

Create an empty repo named `sportstats` at github.com/momoabdoulayegueye-beep (no README), then:

```bash
cd sportstats
git init
git add .
git commit -m "v1: multi-league pipeline + Streamlit app"
git branch -M main
git remote add origin https://github.com/momoabdoulayegueye-beep/sportstats.git
git push -u origin main
```

**Enable the daily auto-refresh:** on GitHub → repo → Settings → Actions → General → Workflow permissions → select "Read and write permissions". The workflow then fetches fresh results every morning and commits them — your tracker runs itself.

## Deploy (free, ~5 minutes)

1. Go to share.streamlit.io and sign in with GitHub.
2. New app → pick `sportstats` → main file `app/streamlit_app.py` → Deploy.
3. You get a public URL. Because Actions commits fresh data daily and Streamlit redeploys on new commits, the live site updates itself.

## Roadmap

- [ ] World Cup group-aware tables & knockout bracket view
- [ ] Elo ratings per league (`src/soccer/elo.py`) — then win probabilities
- [ ] Player-level stats (FBref/StatsBomb) — the Opta-style layer
- [ ] NFL + tennis pages in the app (data fetchers already work)
- [ ] Basketball (`nba_api`), MMA/boxing (ESPN endpoints, TheSportsDB)
- [ ] Custom domain

## Data sources & credit

ESPN public JSON API (soccer results) · [Jeff Sackmann](https://github.com/JeffSackmann) (tennis, CC BY-NC-SA) · [nflverse](https://github.com/nflverse) (NFL). Free for personal/student use — credit them if you publish.
