# Movies-Recommender-System

A content-based movie recommendation system. Pick a movie you like, and it
suggests 5 similar titles based on plot overview, genres, keywords, cast,
and director — using `CountVectorizer` + cosine similarity on the
[TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).

Built with Python, pandas, scikit-learn, and served as a [Streamlit](https://streamlit.io/) app.

## How it works

1. Merge the movies and credits datasets on title.
2. For each movie, build a "tags" string from its overview + genres +
   keywords + top-3 billed cast + director.
3. Vectorize all tags with `CountVectorizer` (bag-of-words, 5000 features).
4. Compute pairwise cosine similarity across all ~4,800 movies.
5. Given a selected movie, return the 5 movies with the highest similarity score.

The model is built once at app startup (takes ~20 seconds) and cached for
the lifetime of the server — see `recommender.py`.

## Running it locally

```bash
git clone https://github.com/adarsh0707-kumar/Movie-Recommender-AI-ML.git
cd Movie-Recommender-AI-ML
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Get a free API key from [TMDB](https://www.themoviedb.org/settings/api) to
enable movie posters (optional — the app runs fine without one, it'll just
show placeholder images):

```bash
export TMDB_API_KEY=your_key_here      # Windows: $env:TMDB_API_KEY="your_key_here"
streamlit run app.py
```

Then open `http://localhost:8501`.

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

## Known limitations

- Three titles in the source dataset ("Batman", "The Host", "Out of the
  Blue") each refer to two different movies with the same name. Since the
  datasets are merged on `title` rather than a unique ID, this creates
  duplicate rows for those specific titles — recommendations for them may
  be slightly off. Not yet fixed.
- Recommendations are purely content-based (no collaborative filtering,
  no personalization, no popularity weighting).

## License

MIT — see [LICENSE](LICENSE).
