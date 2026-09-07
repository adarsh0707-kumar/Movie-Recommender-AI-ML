# 🎬 Movies-Recommender-System (AI/ML)

**🔗 Live demo:** https://movie-recommender-ai-ml-tlwmplmuwglcjjlqxqg2kx.streamlit.app/


[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-support-yellow?logo=buy-me-a-coffee\&logoColor=white)](https://buymeacoffee.com/adarsh12kumar)' README.md

A content-based movie recommendation system built with Python and scikit-learn.
Pick any movie from the TMDB 5000 dataset, and the app suggests 5 similar
titles based on plot, genre, keywords, cast, and director — served through
a simple [Streamlit](https://streamlit.io/) web interface with live posters
from [TMDB](https://www.themoviedb.org/).

---

## Table of contents

- [Features](#features)
- [How it works](#how-it-works)
- [Tech stack](#tech-stack)
- [Running it locally](#running-it-locally)
- [Project structure](#project-structure)
- [Dataset](#dataset)
- [Known limitations](#known-limitations)
- [Roadmap / ideas for improvement](#roadmap--ideas-for-improvement)
- [License](#license)

---

## Features

- Select any of ~4,800 movies from a dropdown and get 5 similar recommendations instantly
- Recommendations are computed from actual content (plot, genre, cast, crew) — not ratings or popularity
- Live poster images pulled from TMDB's API
- Model is built once at startup and cached, so recommendations after the first load are near-instant
- Runs with no API key too — falls back to placeholder images if `TMDB_API_KEY` isn't set

## How it works

This is a **content-based filtering** recommender, not collaborative filtering — it doesn't
use other users' ratings, only the movie's own metadata:

1. **Merge** `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` on movie title.
2. **Extract features** from each movie: overview text, genres, keywords, the
   top 3 billed cast members, and the director.
3. **Build a "tags" string** per movie by concatenating all of the above into
   one bag of words, then apply Porter stemming (e.g. "loving"/"loved" → "love")
   so related word forms count as the same feature.
4. **Vectorize** all tags using `CountVectorizer` (bag-of-words, capped at the
   5,000 most frequent terms, English stop words removed).
5. **Compute cosine similarity** between every pair of movies based on their
   vectors — this produces a 4,800 × 4,800 similarity matrix.
6. **Recommend**: given a selected movie, look up its row in the similarity
   matrix, sort every other movie by similarity score, and return the top 5.

All of this happens in `recommender.py`, and is triggered once per server
process by `app.py` via `st.cache_resource` — so the ~20 second build cost
is paid once at startup, not per user request.

## Tech stack

| Layer | Tool |
|---|---|
| Language | Python 3 |
| Data processing | pandas |
| ML / vectorization | scikit-learn (`CountVectorizer`, `cosine_similarity`) |
| Text normalization | NLTK (`PorterStemmer`) |
| Web app / UI | Streamlit |
| External data | TMDB API (poster images) |
| Hosting | Streamlit Community Cloud |

## Running it locally

```bash
git clone https://github.com/adarsh0707-kumar/Movie-Recommender-AI-ML.git
cd Movie-Recommender-AI-ML

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Get a free API key from [TMDB's settings page](https://www.themoviedb.org/settings/api)
to enable real movie posters. This is optional — without it, the app still
works and shows placeholder images instead.

```bash
export TMDB_API_KEY=your_key_here      # Windows: $env:TMDB_API_KEY="your_key_here"
streamlit run app.py
```

Open **http://localhost:8501** in your browser. The first load takes about
20 seconds while the model builds — subsequent recommendations are instant.

## Project structure

```
├── 📁 .clj-kondo
├── 📁 .lsp
├── ⚙️ .gitattributes
├── ⚙️ .gitignore
├── 📄 LICENSE
├── 📄 Procfile
├── 📝 README.md
├── 🐍 app.py
├── 📄 movie-recommender-system.ipynb
├── 🐍 recommender.py
├── 📄 requirements.txt
├── 📄 setup.sh
├── 📄 tmdb_5000_credits.csv
└── 📄 tmdb_5000_movies.csv
```


## Dataset

Built on the [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata),
a public dataset on Kaggle containing metadata for ~5,000 movies from TMDB,
including overviews, genres, keywords, cast, and crew.

## Known limitations

- **Duplicate titles**: three movies in the dataset — "Batman," "The Host,"
  and "Out of the Blue" — each refer to two different films with the same
  title. Since the datasets are merged on `title` rather than a unique ID,
  this produces duplicate rows for those specific entries, and recommendations
  involving them may be slightly off. Not yet fixed.
- **No personalization**: recommendations are purely content-based and
  identical for every user — there's no account system, watch history, or
  collaborative filtering signal.
- **No evaluation metric**: recommendation quality is currently judged by
  eyeballing results, not by any quantitative benchmark (e.g. precision@k).
- **Cold start on deploy**: since the model builds from raw CSVs at startup
  rather than loading a precomputed file, each fresh deployment/restart pays
  a one-time ~20 second build cost before the app is ready.

## Roadmap / ideas for improvement

- [ ] Fix the duplicate-title merge bug (merge on TMDB `id` instead of `title`)
- [ ] Add a lightweight evaluation step (e.g. precision@k against a hand-labeled sample)
- [ ] Try TF-IDF instead of raw `CountVectorizer`, or blend in popularity/vote average
- [ ] Add unit tests for `recommend()`
- [ ] Add a Dockerfile for fully reproducible local/deploy environments
- [ ] Better error handling around TMDB API timeouts/rate limits

Contributions and suggestions are welcome — feel free to open an issue or PR.

## License

MIT — see [LICENSE](LICENSE).

---

If this project was useful to you, consider [buying me a coffee ☕](https://buymeacoffee.com/adarsh12kumar).