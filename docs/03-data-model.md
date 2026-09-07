# Data Model
## Movie Recommender (AI/ML)

## 1. Source data

### `tmdb_5000_movies.csv`

| Column (used) | Type | Notes |
|---|---|---|
| `id` | int | TMDB movie ID — unique per film |
| `title` | string | Movie title — **not unique**, see §4 |
| `overview` | string | Plot summary paragraph |
| `genres` | JSON-string list | e.g. `[{"id":28,"name":"Action"}, ...]` |
| `keywords` | JSON-string list | e.g. `[{"id":123,"name":"space"}, ...]` |

Other columns exist in the raw file (budget, revenue, release_date,
runtime, vote_average, etc.) but are not currently used by the model.

### `tmdb_5000_credits.csv`

| Column (used) | Type | Notes |
|---|---|---|
| `title` | string | Join key back to movies.csv |
| `cast` | JSON-string list | List of cast members with `name`, ordered by billing |
| `crew` | JSON-string list | List of crew members with `name` and `job` (director extracted via `job == "Director"`) |

## 2. Derived data (built in-memory at runtime)

### `movies` (intermediate, inside `build_model()`)

After merge + parsing, before tag construction:

| Column | Type | Description |
|---|---|---|
| `id` | int | TMDB id |
| `title` | string | Movie title |
| `overview` | list[str] | Overview split into words |
| `genres` | list[str] | Genre names, spaces stripped (`"Science Fiction"` → `"ScienceFiction"`) |
| `keywords` | list[str] | Keyword names, spaces stripped |
| `cast` | list[str] | Top 3 billed actor names, spaces stripped |
| `crew` | list[str] | Director name only (0 or 1 entries), spaces stripped |

Spaces are stripped within multi-word names so `CountVectorizer` treats
e.g. "Chris Evans" as one token (`ChrisEvans`), not two separate common
words that would collide with other people's first/last names.

### `new_df` (returned as `movies_df`)

| Column | Type | Description |
|---|---|---|
| `id` | int | TMDB id — used to fetch poster |
| `title` | string | Displayed and matched against the dropdown selection |
| `tags` | string | Final stemmed, lowercased, space-joined bag of words used as the vectorization input |

### `similarity` (returned alongside `movies_df`)

A dense NumPy array of shape `(N, N)` where `N ≈ 4,800` (the row count of
`movies_df` after dropping nulls). `similarity[i][j]` is the cosine
similarity between movie at row `i` and movie at row `j`. Row/column order
matches `movies_df`'s row order exactly — this alignment is what lets
`recommend()` look up a row index in one and use it directly in the other.

## 3. Vectorization details

- **Vectorizer**: `sklearn.feature_extraction.text.CountVectorizer`
- **Max features**: 5,000 (most frequent terms across the whole corpus)
- **Stop words**: English, removed
- **Normalization**: Porter stemming applied to every word in `tags`
  before vectorization (e.g. "loving" → "love")
- **Output**: sparse term-frequency matrix, densified (`.toarray()`)
  before computing cosine similarity

## 4. Known data quality issue: duplicate titles

Three titles exist twice in the source data, referring to two genuinely
different films:

| Title | Films |
|---|---|
| "Batman" | 1989 Tim Burton film vs. a different `id` sharing the same title |
| "The Host" | Two different films sharing this title |
| "Out of the Blue" | Two different films sharing this title |

Because the merge join key is `title` (not `id`), rows for these three
titles get duplicated during the `movies.merge(credits, on="title")` step,
inflating the dataset from 4,803 to 4,809 rows. `recommend()` looks up
`movies_df.index[movies_df["title"] == movie_title]` and only uses the
**first** match — so the second film sharing that title is effectively
invisible to lookups by title, and its row still pollutes the similarity
matrix as a near-duplicate of the first. See `08-gap-analysis.md` for the
proposed fix (merge on `id` instead).

## 5. Data lifecycle

There is no write path — the app never modifies the source CSVs. Every
process start reads them fresh, rebuilds `movies_df`/`similarity` in
memory, and discards them on process exit. No caching layer persists
across restarts; `st.cache_resource` only caches within a single running
process's lifetime.