# Glossary
## Movie Recommender (AI/ML)

**Bag-of-words**
A text representation where a document is represented as an unordered
collection ("bag") of its words, ignoring grammar and word order —
counting only which words appear and how often.

**Content-based filtering**
A recommendation approach that suggests items similar to a given item
based on the item's own attributes (genre, cast, plot, etc.), as opposed
to collaborative filtering, which uses other users' behavior.

**Collaborative filtering**
A recommendation approach based on patterns across many users' behavior
(e.g. "users who liked X also liked Y"). Not used in this project — see
`01-product-requirements.md` Non-goals.

**Cosine similarity**
A measure of similarity between two vectors based on the cosine of the
angle between them, ranging from -1 to 1 (in this project's case, 0 to 1,
since term counts are never negative). A value of 1 means the vectors
point in exactly the same direction (maximally similar content); 0 means
no shared terms.

**`CountVectorizer`**
A scikit-learn tool that converts a collection of text documents into a
matrix of token (word) counts — the bag-of-words representation used as
input to the similarity computation in this project.

**Cold start (in this project's context)**
The one-time delay (~20 seconds) incurred when the app process starts and
`build_model()` runs for the first time, before any user request can be
served. Not to be confused with the "cold start problem" in recommender
systems generally (how to recommend for a new user/item with no history),
which does not apply here since this project has no per-user data.

**Git LFS (Large File Storage)**
A Git extension for versioning large binary files by storing a small
"pointer" file in the repository and the actual content in separate LFS
storage. A misconfigured LFS setup was the direct cause of one of the
original bugs in this project — see `08-gap-analysis.md` #2.

**Porter stemming**
An algorithm that reduces words to a common root/stem form (e.g.
"loving," "loved," "loves" → "love"), used here so related word forms are
treated as the same feature during vectorization.

**Stop words**
Very common words (e.g. "the," "and," "is") that are typically excluded
from text analysis because they carry little distinguishing meaning.
`CountVectorizer` is configured to remove English stop words in this
project.

**TMDB (The Movie Database)**
A public, community-built movie/TV database with a free API. This
project's dataset originates from a TMDB export ("TMDB 5000"), and the
live app also calls TMDB's API directly to fetch poster images.

**Vectorization**
The process of converting non-numeric data (here, text) into numeric
vectors so mathematical operations (like cosine similarity) can be
applied to it.