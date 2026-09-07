# API Reference
## Movie Recommender (AI/ML)

This project has no REST/HTTP API of its own — it's a single Streamlit
app, not a client-server split. This document instead covers:

1. The internal Python interface (`recommender.py`) — the closest thing
   to a stable "API" in this codebase, and the place a future HTTP layer
   would wrap.
2. The one external API this project calls (TMDB).

## 1. Internal interface — `recommender.py`

### `build_model() -> tuple[pandas.DataFrame, numpy.ndarray]`

Rebuilds the full model from the source CSVs.

**Returns**: `(movies_df, similarity)`
- `movies_df`: columns `id`, `title`, `tags` — see `03-data-model.md`
- `similarity`: dense `(N, N)` cosine similarity matrix aligned to
  `movies_df`'s row order

**Raises**: `FileNotFoundError` if either source CSV is missing from the
repo root.

**Cost**: ~20 seconds for the current dataset size (~4,800 rows). Intended
to be called once per process and cached by the caller (`app.py` does
this via `st.cache_resource`).

```python
from recommender import build_model
movies_df, similarity = build_model()
```

### `recommend(movie_title, movies_df, similarity, top_n=5) -> list[tuple[str, int]]`

Looks up `movie_title` in `movies_df` and returns the `top_n` most similar
titles.

| Parameter | Type | Description |
|---|---|---|
| `movie_title` | str | Must exactly match a value in `movies_df["title"]` |
| `movies_df` | DataFrame | As returned by `build_model()` |
| `similarity` | ndarray | As returned by `build_model()` |
| `top_n` | int | Number of recommendations to return (default 5) |

**Returns**: list of `(title, tmdb_id)` tuples, longest `top_n`, ordered
by descending similarity. Returns `[]` if `movie_title` has no exact
match.

```python
from recommender import recommend
results = recommend("Batman Begins", movies_df, similarity)
# [("The Dark Knight", 155), ("Batman", 268), ...]
```

## 2. External API — TMDB

Used only for poster image lookup.

**Endpoint called**: `GET https://api.themoviedb.org/3/movie/{movie_id}`

**Auth**: API key passed as a query parameter (`api_key`), read from
`TMDB_API_KEY` (env var or `st.secrets`) — never hardcoded. See
`07-security.md`.

**Fields consumed from the response**: `poster_path` only.

**Failure handling**: any `requests.RequestException` (timeout, network
error, non-2xx status) is caught in `fetch_poster()` and results in a
placeholder image being shown instead — the app never surfaces a raw
API error to the user.

**Rate limits**: governed by TMDB's own API terms; not something this
project currently monitors or handles beyond the timeout/fallback above.
Full TMDB API docs: https://developer.themoviedb.org/reference/intro/getting-started