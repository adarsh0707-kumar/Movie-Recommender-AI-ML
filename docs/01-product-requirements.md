# Product Requirements Document

## Movie Recommender (AI/ML)

|                        |                                                                       |
| ---------------------- | --------------------------------------------------------------------- |
| **Status**       | Active                                                                |
| **Owner**        | Adarsh Kumar                                                          |
| **Last updated** | September 2026                                                        |
| **Live product** | https://movie-recommender-ai-ml-tlwmplmuwglcjjlqxqg2kx.streamlit.app/ |

## 1. Problem statement

People often want a new movie similar to one they already liked, but
generic search or genre browsing doesn't capture what actually made them
like it — plot tone, specific actors, a director's style, thematic
keywords. This project solves that specific, narrow problem: **given one
movie a person likes, suggest others that share its content
characteristics.**

## 2. Goals

- Let a user pick a movie and instantly get similar recommendations.
- Keep the logic transparent and explainable — grounded in explicit
  features (genre, cast, plot), not a black box.
- Ship as a free, public web app with zero login friction.
- Serve as a clean, well-documented example of an end-to-end ML pipeline:
  ingestion → feature engineering → model → UI → deployment.

## 3. Non-goals

- Not a "where to watch" streaming guide.
- Not collaborative filtering — no accounts, ratings, or watch history.
- Not personalized — the same input movie always returns the same output.
- Not covering movies outside the fixed TMDB 5000 dataset (mostly pre-2017).

## 4. Target users

| Persona                   | Need                                                               |
| ------------------------- | ------------------------------------------------------------------ |
| Casual moviegoer          | "I liked X, what else is like it?"                                 |
| Recruiter/hiring manager  | Wants to see a working, documented ML project                      |
| Other developers/students | Want a minimal reference implementation of content-based filtering |

## 5. User stories

- *As a visitor*, I want to select a movie from a dropdown so I don't have
  to type an exact title.
- *As a visitor*, I want to see poster images so I recognize titles faster.
- *As a visitor*, I want the app to keep working even if poster images
  fail to load.
- *As a developer evaluating this repo*, I want documentation that
  explains what it does and how to run it, without reading all the code
  first.

## 6. Requirements

See [`04-api-reference.md`](04-api-reference.md) for the callable interface
and [`03-data-model.md`](03-data-model.md) for the data schema. Full
functional/non-functional requirements live in this document's companion
spec — see the Requirements table below.

| ID   | Requirement                                                                                            | Priority |
| ---- | ------------------------------------------------------------------------------------------------------ | -------- |
| FR-1 | Display a searchable dropdown of all movie titles.                                                     | Must     |
| FR-2 | Return exactly 5 movies most similar to the selection.                                                 | Must     |
| FR-3 | Display each recommendation's title and poster.                                                        | Must     |
| FR-4 | Degrade to a placeholder image if no API key is set.                                                   | Must     |
| FR-5 | Degrade to a placeholder image if the TMDB call fails/times out.                                       | Must     |
| FR-6 | Build the model from source CSVs at startup — no dependency on prebuilt binary artifacts in the repo. | Must     |
| FR-7 | Cache the built model for the process lifetime.                                                        | Must     |

## 7. Success metrics

Qualitative, since this is a portfolio project, not a monetized product:

- App is reachable and functional at the public URL at all times.
- New visitor reaches recommendations in ≤3 interactions.
- New contributor can clone and run it using only the README.
- Recommendations are subjectively sensible for well-known movies
  (spot-checked manually).

## 8. Risks

See [`08-gap-analysis.md`](08-gap-analysis.md) for the full list of
issues found, fixed, and still open.

## 9. Roadmap

See [`05-roadmap-and-phases.md`](05-roadmap-and-phases.md).
