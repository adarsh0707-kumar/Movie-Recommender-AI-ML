# Gap Analysis
## Movie Recommender (AI/ML)

This documents every issue found during the initial review of the
project, whether it's been fixed, and what's still open. This is the
project's "why it didn't work, and what we did about it" record.

## Summary

The original repository could not run end-to-end on a fresh clone. The
recommendation algorithm itself was sound — the failures were entirely in
packaging, data handling, and deployment configuration.

## Issues found and resolved

| # | Issue | Root cause | Fix | Status |
|---|---|---|---|---|
| 1 | App couldn't load its similarity matrix | `similarity.pkl` was never actually committed — only a `.zip` and two split `.partaa`/`.partab` files existed, with no reassembly step | Rebuilt model at runtime from source CSVs (`recommender.py`) instead of depending on a prebuilt pickle | ✅ Fixed |
| 2 | App couldn't load its movie metadata | `movie_dict.pkl` was an unresolved Git LFS pointer stub (132 bytes), not the real data | Same fix as #1 — no pickle dependency at all now | ✅ Fixed |
| 3 | Wrong working directory on deploy | `app.py` lived in `Website/` and used relative paths (`../movie_dict.pkl`) assuming that cwd, but the `Procfile` ran `streamlit run app.py` from the repo root | Moved `app.py` to repo root; `recommender.py` resolves CSV paths relative to its own file location, not cwd | ✅ Fixed |
| 4 | `pip install` failed on any machine but the original author's | `requirements.txt` was a raw `conda`/`pip freeze` dump full of `file:///croot/...` local build paths | Rewrote `requirements.txt` with only the packages actually imported | ✅ Fixed |
| 5 | Live TMDB API key hardcoded and exposed in a public repo | Convenience during original development, never revisited | Read from `TMDB_API_KEY` env var/`st.secrets`; old key flagged for revocation | ✅ Fixed (see `07-security.md` open item to verify revocation) |
| 6 | Deployment target (Heroku) had no working free tier | Heroku discontinued its free tier in Nov 2022 | Removed `Procfile`/`setup.sh`; deployed to Streamlit Community Cloud instead | ✅ Fixed |
| 7 | README had no usable content | Never written past initial repeated headers | Full rewrite: description, setup, structure, dataset, limitations, roadmap | ✅ Fixed |
| 8 | No license | Never added | Added MIT `LICENSE` | ✅ Fixed |
| 9 | `numpy==2.2.4` (and other exact pins) failed to install on Python 3.14 | No prebuilt wheel yet for that Python version at time of testing, forcing a from-source compile that failed | Switched `requirements.txt` to `>=` ranges | ✅ Fixed |

## Issues found, still open

| # | Issue | Impact | Tracked in |
|---|---|---|---|
| 10 | Merging `movies.csv`/`credits.csv` on `title` instead of `id` creates duplicate rows for 3 titles ("Batman", "The Host", "Out of the Blue") that each refer to two different films | Recommendations involving these 3 titles may be inaccurate; one of the two films sharing a title is invisible to lookup | `03-data-model.md` §4, `05-roadmap-and-phases.md` Phase 4 |
| 11 | Intermittent missing poster images observed during manual testing (3 of 5 posters loaded in one test run) | Minor UX issue — titles still display correctly | `05-roadmap-and-phases.md` Phase 4 |
| 12 | No automated tests | Regressions in `recommend()`/`build_model()` would only be caught by manual spot-checking | `09-testing-strategy.md`, `05-roadmap-and-phases.md` Phase 5 |
| 13 | No CI pipeline | No automated check on push/PR | `05-roadmap-and-phases.md` Phase 5 |

## Not a gap — accepted limitations

These were identified during review but are intentional scope boundaries,
not bugs:

- Static dataset (TMDB 5000, ~2017) — no live data ingestion.
- No collaborative filtering/personalization — out of scope by design
  (see `01-product-requirements.md` Non-goals).
- ~20 second cold start per server restart — acceptable given dataset
  size and hosting model (see `01-product-requirements.md` NFR-2 in the
  requirements table).