# Development Guide
## Movie Recommender (AI/ML)

This covers local setup and day-to-day development workflow. For PR/issue
process, see [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## 1. Prerequisites

- Python 3.10–3.13 recommended.
- Python 3.14 works but requires the `>=` version ranges already in
  `requirements.txt` — exact pins can fail to install if a package (most
  often `numpy`) doesn't yet have a prebuilt wheel for a very new Python
  release, forcing a from-source compile that may fail depending on your
  machine's build toolchain.

## 2. Environment setup

```bash
git clone https://github.com/adarsh0707-kumar/Movie-Recommender-AI-ML.git
cd Movie-Recommender-AI-ML

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Running the app

```bash
export TMDB_API_KEY=your_key_here      # Windows: $env:TMDB_API_KEY="your_key_here"
streamlit run app.py
```

Open `http://localhost:8501`. First load takes ~20s while `build_model()`
runs; subsequent interactions are fast since the result is cached for the
life of the process (`st.cache_resource`).

Running without `TMDB_API_KEY` set works fine — you'll see a warning
banner and placeholder images instead of real posters.

## 4. Working on the model/data pipeline in isolation

You don't need Streamlit running to iterate on `recommender.py`:

```bash
python3 -c "
from recommender import build_model, recommend
movies_df, similarity = build_model()
print(len(movies_df), 'movies loaded')
print(recommend('Inception', movies_df, similarity))
"
```

This is the fastest feedback loop for changes to feature engineering or
the similarity computation, since it skips the Streamlit UI entirely.

## 5. Debugging tips

- **`FileNotFoundError` on startup**: `tmdb_5000_movies.csv` /
  `tmdb_5000_credits.csv` must sit in the same folder as `recommender.py`
  (the repo root). Check with `ls *.csv` from the repo root.
- **`ModuleNotFoundError: No module named 'recommender'`**: you're running
  `streamlit run app.py` from a different folder than the one containing
  `recommender.py`. `cd` to the repo root first.
- **Empty recommendation list**: `recommend()` does an exact string match
  against `movies_df["title"]` — check for a trailing space, different
  capitalization, or the movie genuinely not being in the dataset.
- **Posters not loading**: confirm `TMDB_API_KEY` is set in the same
  terminal session you launched `streamlit run` from (env vars don't
  carry over between separate terminal tabs unless exported in your shell
  profile).

## 6. Making a change to the model

If you change anything in the feature-engineering pipeline
(`build_model()`), sanity-check with a few well-known movies before
committing — e.g. confirm Batman films still recommend other Batman
films, confirm a well-known franchise entry recommends its sequels/
prequels. There's no automated regression test for recommendation
*quality* yet (only for the function not crashing) — see
`09-testing-strategy.md`.

## 7. Deploying your own copy

1. Fork the repo.
2. Go to https://share.streamlit.io, sign in with GitHub.
3. New app → select your fork, branch `main`, file `app.py`.
4. Advanced settings → add `TMDB_API_KEY = "your_key"` under Secrets.
5. Deploy.