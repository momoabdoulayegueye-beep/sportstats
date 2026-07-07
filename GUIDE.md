# SportStats — the complete walkthrough

Follow this top to bottom. Every command is written for macOS (Windows variants noted where they differ). Total time: ~45 minutes to a live website.

**Accounts you need: GitHub only** (you have it). No BallDontLie, no API keys, no signups. Every data source in this project is free and keyless.

---

## Part 0 — Know your files

Three kinds of files here: ones you **run**, ones you **edit**, and ones you **never touch**.

| File | What it is | What you do with it |
|---|---|---|
| `config.yaml` | Control panel: the list of leagues to track | **Edit** when you want more/fewer leagues |
| `requirements.txt` | Shopping list of Python libraries | Used once by `pip` in Part 1 |
| `src/soccer/fetch_espn.py` | The data collector — asks ESPN for results, saves them | **Run** it (Part 1, step 5) |
| `src/soccer/standings.py` | Stats brain — turns raw results into league tables | Never run — the app imports it |
| `src/common/db.py` | Builds a SQLite database from the CSV, for SQL practice | **Run** it when you want SQL |
| `app/streamlit_app.py` | The website itself | **Run** it (Part 1, step 8) |
| `notebooks/explore.qmd` | Your stats playground — open in RStudio | **Edit/experiment** freely |
| `tests/test_standings.py` | Proof the table math is correct | **Run** once to verify |
| `src/tennis/…`, `src/nfl/…` | Future sport modules (already functional) | Ignore for now |
| `.github/workflows/refresh.yml` | The robot: fetches new results daily | Never touch — activates in Part 3 |
| `.gitignore` | Tells git which files not to upload | Never touch |
| `data/` | Where `matches.csv` will land after your first fetch | Never touch by hand |
| `README.md` / `GUIDE.md` | The manual / this walkthrough | Read |

The flow of the whole machine:

```
fetch_espn.py ──▶ data/matches.csv ──▶ streamlit_app.py (+ standings.py) ──▶ your browser
                        ▲
        refresh.yml refreshes this daily, once on GitHub
```

---

## Part 1 — Make it run on your Mac (~15 min)

**1. Unzip** `sportstats.zip` and move the `sportstats` folder somewhere sane, e.g. `Documents/projects/`.

**2. Open a terminal in that folder.** Easiest: open RStudio → Terminal tab (next to Console), then:

```bash
cd ~/Documents/projects/sportstats
```

(Adjust the path to wherever you put it. `pwd` shows where you are, `ls` lists files — you should see `config.yaml`, `src`, `app`…)

**3. Create a virtual environment** — a private bubble so this project's libraries don't pollute your Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Your prompt now starts with `(.venv)`. You'll re-run that `source` line each time you come back to the project. *(Windows: `.venv\Scripts\activate`)*

**4. Install the libraries** (one-time, ~1 min):

```bash
pip install -r requirements.txt
```

**5. Fetch real data — the big moment:**

```bash
python -m src.soccer.fetch_espn --days 30
```

Expected output, one line per league:

```
FIFA World Cup 2026            64 matches
Premier League                  0 matches
...
Saved 312 total matches -> data/matches.csv
```

Zeros for club leagues are **normal right now** — Europe is on summer break until August. The World Cup line is the one that should be full. A file `data/matches.csv` now exists — open it, it's readable.

**6. Verify the math:**

```bash
python tests/test_standings.py        # → All standings checks passed ✔
```

**7. (Optional) Build the SQL database:**

```bash
python -m src.common.db               # → creates data/sports.db
```

**8. Launch your app:**

```bash
streamlit run app/streamlit_app.py
```

Your browser opens `localhost:8501`. Pick *FIFA World Cup 2026* in the sidebar, click through Results / Table / Charts. That's your website — running locally. `Ctrl+C` in the terminal stops it.

---

## Part 2 — Put it on GitHub (~10 min)

**1. Create the repo:** github.com → **+** → *New repository* → name `sportstats` → Public → **do NOT check "Add a README"** → Create.

**2. Back in your terminal** (inside the sportstats folder), run these one at a time:

```bash
git init                     # start version control in this folder
git add .                    # stage every file
git commit -m "v1: multi-league pipeline + Streamlit app"
git branch -M main
git remote add origin https://github.com/momoabdoulayegueye-beep/sportstats.git
git push -u origin main      # upload
```

The push will ask you to authenticate — a browser window handles it. When done, refresh your GitHub page: all your files are there.

---

## Part 3 — Turn on the robot (~5 min)

The workflow file only works once it lives on GitHub. Activate it:

1. On your repo page → **Settings** → **Actions** → **General** → scroll to *Workflow permissions* → select **Read and write permissions** → Save.
2. **Actions** tab → *Daily data refresh* (left sidebar) → **Run workflow** button → run it manually once.
3. Watch it turn green (~1 min). Check the repo's commit history: a new commit *"data: daily refresh"* appeared. A robot just updated your data.

From now on it runs every morning at 06:00 UTC without you.

---

## Part 4 — Put it on the internet (~5 min)

1. Go to **share.streamlit.io** → *Sign in with GitHub*.
2. **New app** → repository `momoabdoulayegueye-beep/sportstats` → branch `main` → main file `app/streamlit_app.py` → **Deploy**.
3. Two minutes later you have a public URL like `sportstats-xyz.streamlit.app`. Send it to a friend.

The loop is now closed: Actions commits fresh data daily → Streamlit sees the new commit → your live site updates itself. You built an automated daily tracker.

---

## Part 5 — Living with it

**Each time you work on the project:**

```bash
cd ~/Documents/projects/sportstats
source .venv/bin/activate
```

**After you change code:** `git add .` → `git commit -m "what you did"` → `git push` (the live site auto-updates).

**To explore stats:** open `notebooks/explore.qmd` in RStudio and play. Ideas queued in the README roadmap — Elo ratings are the natural next build, then player-level data (the Opta layer).

**To change leagues:** edit `config.yaml`, re-run the fetch.

---

## Troubleshooting

- **`command not found: python`** → use `python3` (and `pip3`).
- **`streamlit: command not found`** → your venv isn't active; run `source .venv/bin/activate`.
- **Every league shows 0 matches** → network/firewall issue; try again, or from another connection.
- **`git push` rejected** → you probably checked "Add a README" when creating the repo. Run `git pull origin main --rebase` then `git push` again.
- **Actions run fails** → re-check Part 3 step 1 (write permissions).

Stuck anywhere? Paste me the exact error message and I'll fix it with you.
