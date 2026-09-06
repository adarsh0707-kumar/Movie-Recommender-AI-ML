import os

import requests
import streamlit as st

from recommender import build_model, recommend

TMDB_API_KEY = os.environ.get("TMDB_API_KEY") or st.secrets.get("TMDB_API_KEY", None)
PLACEHOLDER_POSTER = "https://via.placeholder.com/500x750?text=No+Image+Available"


@st.cache_resource(show_spinner="Building recommendation model (first run only)...")
def load_model():
    return build_model()


def fetch_poster(movie_id):
    if not TMDB_API_KEY:
        return PLACEHOLDER_POSTER
    try:
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}",
            params={"api_key": TMDB_API_KEY, "language": "en-US"},
            timeout=5,
        )
        response.raise_for_status()
        poster_path = response.json().get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except requests.RequestException:
        pass
    return PLACEHOLDER_POSTER


st.title("Movie Recommendation System")

if not TMDB_API_KEY:
    st.warning(
        "No TMDB API key found. Posters will show as placeholders. "
        "Set the TMDB_API_KEY environment variable or add it to "
        "`.streamlit/secrets.toml` to enable posters.",
        icon="⚠️",
    )

movies_df, similarity = load_model()

selected_movie_name = st.selectbox("Select a movie:", movies_df["title"].values)

if st.button("Recommend"):
    results = recommend(selected_movie_name, movies_df, similarity)

    if not results:
        st.error("No recommendations found for that title.")
    else:
        columns = st.columns(len(results))
        for col, (title, movie_id) in zip(columns, results):
            with col:
                st.text(title)
                st.image(fetch_poster(movie_id))