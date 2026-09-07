# Testing Strategy
## Movie Recommender (AI/ML)

## Current state: manual testing only

There is no automated test suite yet. Verification happens by running
the app locally and manually checking behavior. This document describes
both the current manual process and the intended automated strategy.

## 1. Manual test checklist (run before every commit/PR)

- [ ] `streamlit run app.py` starts with no traceback.
- [ ] Model build spinner appears and completes (~20s) on first load.
- [ ] Movie dropdown populates with titles.
- [ ] Selecting a well-known movie (e.g. "Batman Begins") and clicking
      Recommend returns 5 sensible, related titles.
- [ ] Recommendations display correctly with the app running **without**
      `TMDB_API_KEY` set — placeholder images should appear, no crash.
- [ ] Recommendations display correctly **with** `TMDB_API_KEY` set —
      real posters should load.
- [ ] Quick manual sanity check via the isolated pipeline (no UI needed):
```bash
      python3 -c "
      from recommender import build_model, recommend
      movies_df, similarity = build_model()
      print(recommend('Inception', movies_df, similarity))
      "
```

## 2. Known-good spot-check cases

Useful reference points — these are cases where "obviously correct"
recommendations are easy to judge by eye:

| Input movie | Expect recommendations to include |
|---|---|
| "Batman Begins" | Other Batman films (The Dark Knight, Batman, etc.) |
| "The Dark Knight Rises" | Other Batman/Nolan-era films |
| A well-known franchise entry (e.g. an Iron Man film) | Other films in the same franchise |

Note: due to the known duplicate-title bug (`08-gap-analysis.md` #10),
avoid using "Batman", "The Host", or "Out of the Blue" as the *sole*
verification case, since lookups against these are currently ambiguous
between two different films.

## 3. Planned automated tests (not yet implemented)

Once a test framework (`pytest`) is added:

### Unit tests — `recommender.py`

- `recommend()` returns exactly `top_n` results for a known valid title.
- `recommend()` returns `[]` for a title not in the dataset.
- `recommend()` never returns the input movie itself in its own results.
- `build_model()` returns a `similarity` matrix whose shape is
  `(len(movies_df), len(movies_df))`.
- `build_model()` raises `FileNotFoundError` with a clear message when
  CSVs are missing (can be tested by pointing at a temp dir without them).

### Integration-style tests — `app.py`

- Given `TMDB_API_KEY` unset, `fetch_poster()` returns the placeholder
  URL without making a network call.
- Given a mocked `requests.get` that raises `RequestException`,
  `fetch_poster()` returns the placeholder URL rather than propagating
  the exception.

### Regression tests — model quality

- A small hand-labeled set of "movie X should recommend movie Y" pairs,
  checked after any change to the feature engineering or vectorization
  step, to catch unintended quality regressions (this is a soft/fuzzy
  check, not a hard pass/fail — see Phase 4 in `05-roadmap-and-phases.md`
  regarding precision@k).

## 4. CI (not yet configured)

Once tests exist, a simple GitHub Actions workflow would run
`pip install -r requirements.txt && pytest` on every push/PR — no such
workflow exists yet.