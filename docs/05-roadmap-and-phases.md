# Roadmap & Phases
## Movie Recommender (AI/ML)

## Phase 0 — Original state (pre-fix)

The project as originally committed. Non-functional on a fresh clone.
Documented in full in [`08-gap-analysis.md`](08-gap-analysis.md).

## Phase 1 — Make it run (✅ complete)

| Item | Status |
|---|---|
| Replace missing/broken pickle files with runtime model building (`recommender.py`) | ✅ Done |
| Fix `app.py`/`Procfile` working-directory mismatch | ✅ Done |
| Remove hardcoded, exposed TMDB API key; read from env/secrets | ✅ Done |
| Replace unusable conda `pip freeze` dump with a real `requirements.txt` | ✅ Done |

## Phase 2 — Make it deployable (✅ complete)

| Item | Status |
|---|---|
| Remove dead Heroku `Procfile`/`setup.sh` | ✅ Done |
| Deploy to Streamlit Community Cloud | ✅ Done — live at the URL in the README |
| Move `TMDB_API_KEY` into platform secrets | ✅ Done |

## Phase 3 — Make it presentable (✅ complete)

| Item | Status |
|---|---|
| Rewrite README (description, setup, structure, limitations) | ✅ Done |
| Add `LICENSE` (MIT) | ✅ Done |
| Add `CONTRIBUTING.md` | ✅ Done |
| Add full docs set (this document set) | ✅ Done |

## Phase 4 — Fix known data/quality issues (open)

| Item | Priority | Notes |
|---|---|---|
| Merge datasets on `id` instead of `title` to fix the duplicate-title bug (Batman/The Host/Out of the Blue) | High | See `03-data-model.md` §4 |
| Add a lightweight evaluation step (e.g. precision@k against a small hand-labeled set) | Medium | Currently no quantitative measure of recommendation quality |
| Fix intermittent missing poster images observed in manual testing | Low | Likely placeholder-service flakiness or TMDB rate limiting on rapid parallel requests |

## Phase 5 — Strengthen engineering practices (open)

| Item | Priority | Notes |
|---|---|---|
| Add automated tests for `recommend()`/`build_model()` | High | See `09-testing-strategy.md` — currently manual only |
| Add CI (run tests on push/PR) | Medium | No CI configured yet |
| Add a `Dockerfile` for fully reproducible environments | Low | Would remove Python-version wheel issues entirely (see `06-development-guide.md`) |

## Phase 6 — Model improvements (exploratory / not scheduled)

| Item | Notes |
|---|---|
| Try TF-IDF instead of raw `CountVectorizer` counts | May better downweight very common terms |
| Blend content similarity with popularity/vote average | Could reduce recommending obscure, poorly-rated titles |
| Explore embeddings-based similarity (e.g. sentence embeddings on overview text) | Would meaningfully change the architecture — bigger lift |