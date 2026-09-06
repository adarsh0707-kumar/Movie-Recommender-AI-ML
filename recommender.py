"""
Core data pipeline + model for the movie recommender.

This replaces the old approach of loading pre-pickled `movie_dict.pkl` /
`similarity.pkl` files. Those files were never reliably present in the repo
(one was an unresolved Git LFS pointer, the other was split into
`.partaa`/`.partab` chunks with no reassembly step), so the app could not
start on a fresh clone.

Building the model at runtime from the two source CSVs takes on the order
of ~20 seconds for ~4,800 movies (mostly text preprocessing + stemming),
which is a one-time cost. `app.py` calls `build_model()` once per server
process and caches the result with `st.cache_resource`, so end users never
pay this cost — only the server does, once, on startup/first request.
"""

import ast
import os

import pandas as pd
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Resolve paths relative to this file, not the process's current working
# directory, so it works whether you run `streamlit run app.py` from the
# repo root, from Website/, or from anywhere else.
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_CSV = os.path.join(_BASE_DIR, "tmdb_5000_movies.csv")
CREDITS_CSV = os.path.join(_BASE_DIR, "tmdb_5000_credits.csv")

_ps = PorterStemmer()


def _convert(obj):
    """Parse a JSON-like string column (genres/keywords) into a list of names."""
    return [i["name"] for i in ast.literal_eval(obj)]


def _convert_top3(obj):
    """Parse the cast column into the top 3 billed actor names."""
    names = []
    for i in ast.literal_eval(obj):
        if len(names) == 3:
            break
        names.append(i["name"])
    return names


def _fetch_director(obj):
    """Pull the director's name out of the crew column."""
    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            return [i["name"]]
    return []


def _stem(text):
    return " ".join(_ps.stem(word) for word in text.split())


def build_model():
    """
    Rebuild the movies dataframe + cosine similarity matrix from the raw
    TMDB CSVs. Returns (movies_df, similarity_matrix).

    movies_df has columns: id, title, tags (kept for reference/debugging)
    similarity_matrix[i] gives similarity scores for movies_df.iloc[i]
    against every other movie, aligned by row position.
    """
    if not os.path.exists(MOVIES_CSV) or not os.path.exists(CREDITS_CSV):
        raise FileNotFoundError(
            "tmdb_5000_movies.csv / tmdb_5000_credits.csv not found next to "
            "recommender.py. Make sure both CSVs are present in the repo root."
        )

    movies = pd.read_csv(MOVIES_CSV)
    credits = pd.read_csv(CREDITS_CSV)
    movies = movies.merge(credits, on="title")

    movies = movies[["genres", "id", "keywords", "title", "overview", "cast", "crew"]]
    movies = movies.dropna().reset_index(drop=True)

    movies["genres"] = movies["genres"].apply(_convert)
    movies["keywords"] = movies["keywords"].apply(_convert)
    movies["cast"] = movies["cast"].apply(_convert_top3)
    movies["crew"] = movies["crew"].apply(_fetch_director)
    movies["overview"] = movies["overview"].apply(lambda x: x.split())

    for col in ("genres", "keywords", "cast", "crew"):
        movies[col] = movies[col].apply(lambda items: [i.replace(" ", "") for i in items])

    movies["tags"] = (
        movies["overview"] + movies["genres"] + movies["keywords"] + movies["cast"] + movies["crew"]
    )

    new_df = movies[["id", "title", "tags"]].copy()
    new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x).lower())
    new_df["tags"] = new_df["tags"].apply(_stem)

    cv = CountVectorizer(max_features=5000, stop_words="english")
    vectors = cv.fit_transform(new_df["tags"]).toarray()

    similarity = cosine_similarity(vectors)

    return new_df.reset_index(drop=True), similarity


def recommend(movie_title, movies_df, similarity, top_n=5):
    """Return up to top_n (title, tmdb_id) tuples similar to movie_title."""
    matches = movies_df.index[movies_df["title"] == movie_title]
    if len(matches) == 0:
        return []

    movie_index = matches[0]
    distances = similarity[movie_index]
    ranked = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1 : top_n + 1]

    return [(movies_df.iloc[i].title, int(movies_df.iloc[i].id)) for i, _ in ranked]