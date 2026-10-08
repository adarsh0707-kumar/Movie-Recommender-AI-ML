# Movie Recommender — Content-Based AI/ML

> **A content-based movie recommendation system built with Python, pandas, scikit-learn, NLTK, and Streamlit.**

urlLive demohttps://movie-recommender-ai-ml-tlwmplmuwglcjjlqxqg2kx.streamlit.app/

The application recommends **five movies similar to a selected title** using the movie's own metadata rather than user ratings. It combines plot, genres, keywords, top-billed cast, and director information into a text representation, vectorizes that representation, and ranks movies with cosine similarity.

> **Status:** Working demo  
> **Recommendation type:** Content-based filtering  
> **Dataset:** TMDB 5000 Movie Dataset  
> **Hosting:** Streamlit Community Cloud

---

## What it does

- Select a movie from the dataset.
- Generate the five most similar titles.
- Use movie metadata rather than user-rating history.
- Display live TMDB posters when `TMDB_API_KEY` is configured.
- Fall back to placeholder posters when no API key is available.
- Build and cache the recommendation model once per Streamlit process.

This is **not collaborative filtering** and does not learn personalized preferences from users.

---

## How the recommender works

```text
TMDB Movies + Credits
        │
        ▼
 Merge movie metadata
        │
        ▼
 Extract overview / genres / keywords
 + top 3 cast + director
        │
        ▼
 Combine into "tags"
        │
        ▼
 Porter stemming
        │
        ▼
 CountVectorizer
 max_features = 5,000
        │
        ▼
 Movie feature vectors
        │
        ▼
 Cosine similarity
        │
        ▼
 Top 5 similar movies
```

### 1. Prepare the dataset

`tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` are merged using the movie title.

The implementation extracts:

- overview
- genres
- keywords
- top three cast members
- director

These fields are combined into a single text representation for each movie.

### 2. Normalize and vectorize

The combined tags are processed with NLTK's `PorterStemmer`, then transformed using scikit-learn's `CountVectorizer`.

Current vectorizer configuration:

- bag-of-words representation
- English stop-word removal
- maximum of 5,000 features

### 3. Rank recommendations

The application computes cosine similarity between movie vectors. For a selected movie, its similarity row is sorted and the highest-scoring other titles are returned.

The current dataset produces a similarity matrix of roughly **4,800 × 4,800** entries after preprocessing.

---

## Performance behavior

The model is built once through Streamlit's `st.cache_resource`.

That means:

- the expensive model-building step is not repeated for every recommendation;
- a fresh process/deployment still has to build the model;
- recommendation lookup is performed against the precomputed similarity matrix.

The repository currently does **not** contain a formal benchmark suite, so no throughput or latency numbers are claimed here.

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Data processing | pandas, NumPy |
| ML | scikit-learn |
| Text processing | NLTK / PorterStemmer |
| Vectorization | CountVectorizer |
| Similarity | cosine similarity |
| Web UI | Streamlit |
| Posters | TMDB API |
| Hosting | Streamlit Community Cloud |

---

## Run locally

### Requirements

- Python 3
- pip
- Internet access if you want live TMDB posters

### Setup

```bash
git clone https://github.com/adarsh0707-kumar/Movie-Recommender-AI-ML.git
cd Movie-Recommender-AI-ML

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Optional TMDB API key

Posters are optional. Without a key, the recommender still runs and uses placeholder images.

Linux/macOS:

```bash
export TMDB_API_KEY=your_key_here
```

Windows PowerShell:

```powershell
$env:TMDB_API_KEY="your_key_here"
```

You can also provide the key through Streamlit secrets.

### Start the app

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

The first startup builds the model from the CSV data; later interactions reuse the cached model within the running process.

---

## Repository structure

```text
Movie-Recommender-AI-ML/
├── app.py
├── recommender.py
├── movie-recommender-system.ipynb
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
├── requirements.txt
├── setup.sh
├── Procfile
└── README.md
```

---

## Dataset

The project uses the **TMDB 5000 Movie Dataset**, containing movie metadata such as titles, overviews, genres, keywords, cast, and crew.

The dataset is used for experimentation and recommendation generation. It is not a live database of all TMDB titles.

---

## Known limitations

### Duplicate-title merge

The current preprocessing merges movies and credits by **title** rather than a globally unique movie ID. This creates duplicate-row ambiguity for titles that appear more than once in the dataset, including examples such as:

- `Batman`
- `The Host`
- `Out of the Blue`

A future version should merge using the TMDB movie ID.

### No personalization

Every user receives recommendations based on the same movie-content representation. There is no:

- user profile
- watch history
- ratings model
- collaborative filtering
- personalized ranking

### No quantitative evaluation yet

Recommendation quality has not been validated with a formal offline evaluation. Metrics such as Precision@K, Recall@K, NDCG, coverage, or diversity are not currently reported.

### Startup cost

The model is constructed from the raw CSV files when a new Streamlit process starts. This creates a one-time startup cost before recommendations are available.

### TMDB dependency

Poster retrieval depends on the TMDB API when an API key is configured. Network failures or missing poster metadata fall back to the placeholder image.

---

## Roadmap

- [ ] Merge movies and credits using TMDB IDs.
- [ ] Add automated tests for preprocessing and `recommend()`.
- [ ] Add offline recommendation evaluation.
- [ ] Compare CountVectorizer against TF-IDF.
- [ ] Measure recommendation latency and startup/model-build time.
- [ ] Add recommendation diversity and coverage metrics.
- [ ] Experiment with hybrid content + popularity signals.
- [ ] Persist a precomputed model/vector representation to reduce cold-start work.
- [ ] Improve TMDB API error handling and caching.

---

## Why this project matters

This project demonstrates a complete, understandable ML application path:

```text
Raw dataset
   ↓
Feature engineering
   ↓
Text normalization
   ↓
Vectorization
   ↓
Similarity computation
   ↓
Recommendation ranking
   ↓
Interactive web application
```

It is a useful applied-ML project because the recommendation logic is visible and reproducible rather than hidden behind a third-party recommendation API.

---

## License

MIT — see [LICENSE](LICENSE).
