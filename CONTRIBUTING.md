# Contributing to Movie Recommender (AI/ML)

Thanks for your interest in improving this project! Whether it's a bug
report, a small fix, or a bigger feature, contributions are welcome.

## Before you start

This is a personal/portfolio project, actively being cleaned up. Check the
[Roadmap section in the README](README.md#roadmap--ideas-for-improvement)
and open issues first — it may already be planned or in progress.

For small fixes (typos, README improvements, minor bugs), feel free to
just open a PR directly. For anything larger (new features, architecture
changes), please open an issue first to discuss the approach before
writing code — it saves both of us time if the direction needs adjusting.

## Getting set up

```bash
git clone https://github.com/adarsh0707-kumar/Movie-Recommender-AI-ML.git
cd Movie-Recommender-AI-ML

python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Get a free TMDB API key from https://www.themoviedb.org/settings/api
(optional — the app runs without one, just with placeholder posters):

```bash
export TMDB_API_KEY=your_key_here      # Windows: $env:TMDB_API_KEY="your_key_here"
streamlit run app.py
```

Open `http://localhost:8501` and confirm the app loads and recommendations work
before making changes, so you know your baseline is working.

## Making a change

1. Fork the repo and create a branch off `main`:
```bash
   git checkout -b fix/short-description-of-change
```
2. Make your change.
3. Test it manually by running the app and trying a few different movie
   selections — there's no automated test suite yet (see Roadmap), so
   manual verification is currently the only check.
4. If you changed `recommender.py`, sanity check the core function directly:
```bash
   python3 -c "
   from recommender import build_model, recommend
   movies_df, similarity = build_model()
   print(recommend('Batman Begins', movies_df, similarity))
   "
```
   This should return 5 sensible titles without errors.

## Commit messages

Write commit messages that explain **why**, not just what — e.g.:

```
fix: dedupe merged movies to fix Batman/Host/Out of the Blue bug

Merging on title instead of TMDB id created duplicate rows for movies
that share a title with a different film. Switched the merge key to id
and drop exact duplicate rows before building tags.

```


rather than just `fix bug`.

## Submitting a pull request

- Keep PRs focused — one fix or feature per PR is easier to review than
  several bundled together.
- Describe what changed and why in the PR description.
- Mention how you tested it (which movies you tried, what you checked).
- Update the README if your change affects setup steps, project structure,
  or removes/adds a "Known limitation."

## Reporting bugs

Open an issue with:
- What you did (steps to reproduce)
- What you expected to happen
- What actually happened (include the full error/traceback if there is one)
- Your OS and Python version (`python3 --version`)

## Code style

Nothing enforced yet (no linter/formatter configured), but please:
- Match the existing style in the file you're editing
- Keep functions small and named for what they do (see `recommender.py`
  for the current pattern: small, single-purpose helper functions)
- Add a short docstring to any new function

## Questions

Open an issue with the `question` label, or reach out via the contact info
on the [GitHub profile](https://github.com/adarsh0707-kumar).
