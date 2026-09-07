# Security
## Movie Recommender (AI/ML)

This is a small, stateless, unauthenticated public web app. The security
surface is correspondingly small, but here's what applies and how it's
handled.

## 1. Secrets management

**Current approach**: `TMDB_API_KEY` is read at runtime from either the
`TMDB_API_KEY` environment variable or `st.secrets` (Streamlit's secrets
mechanism), with no hardcoded fallback value in source code.

```python
TMDB_API_KEY = os.environ.get("TMDB_API_KEY") or st.secrets.get("TMDB_API_KEY", None)
```

- Locally: set via `export TMDB_API_KEY=...` or a gitignored
  `.streamlit/secrets.toml`.
- In production (Streamlit Community Cloud): set via the platform's
  Secrets UI, injected as `st.secrets` — never stored in the repo.
- `.gitignore` explicitly excludes `.streamlit/secrets.toml` so a local
  secrets file can never be committed by accident.

**Prior state (fixed)**: an earlier version of this project had a live
TMDB API key hardcoded directly in `app.py` and committed to a public
repository. That key should be treated as permanently compromised (it
remains visible in the git history) — it was regenerated on TMDB's side
as part of this fix. See `08-gap-analysis.md` item on this.

## 2. Input handling

- The only user input is a movie title selected from a Streamlit
  `st.selectbox` populated directly from `movies_df["title"]` — the user
  cannot submit arbitrary free text, which eliminates injection-style
  concerns for this input (no SQL, no shell execution, no template
  rendering of user input).
- `movie_id` values passed to the TMDB API originate only from the
  dataset's own `id` column (never from user input), so there's no
  path for a user to control the URL/parameters sent to TMDB.

## 3. Third-party API calls

- All TMDB calls use `requests` with an explicit `timeout=5` to avoid the
  app hanging indefinitely on a slow/unresponsive third party.
- Failures are caught broadly (`requests.RequestException`) and degrade
  to a placeholder image rather than raising an unhandled exception —
  this also means a malicious or misbehaving TMDB response can't crash
  the app.

## 4. Data privacy

- No user accounts, no cookies beyond what Streamlit's framework sets for
  session state, no analytics, no data collected or stored about
  visitors beyond what Streamlit Community Cloud's platform itself may
  log (outside this project's control).
- The two CSV datasets contain only public movie metadata — no personal
  data of any kind.

## 5. Dependency hygiene

- `requirements.txt` lists only the packages actually imported by the
  code (previously it was a full conda environment dump with ~180
  unrelated packages — see `08-gap-analysis.md`). A smaller, accurate
  dependency list reduces the attack surface from unused/outdated
  transitive dependencies.
- No automated dependency vulnerability scanning (e.g. Dependabot,
  `pip-audit`) is currently configured — listed as an open item below.

## 6. Open items

| Item | Priority |
|---|---|
| Enable GitHub Dependabot alerts for the repo | Low |
| Add `pip-audit` or similar as a manual/CI check | Low |
| Confirm the previously-exposed TMDB key was revoked/regenerated on TMDB's side (not just replaced in code) | High — should already be done, verify |