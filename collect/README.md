# Dataset collection

Scripts used to find candidate misuse cases on GitHub. They produce links; the input
programs under `dataset/` were then selected and extracted by hand.

| Step | Script | What it does |
| --- | --- | --- |
| 1 | `search.py` | Sends the queries in `queries.py` to the GitHub Search API and saves the links to commits, closed issues and closed pull requests |
| 2 | `dedupe.py` | Merges the link lists and removes duplicates and documentation files |
| 3 | `keyword_filter.py` | Keeps a link only when the commit diff, the issue comments, or the pull request comments and patches contain a keyword of the deprecated API (`FILTER_KEYWORDS` in `queries.py`) |
| 4 | manual | The remaining links are inspected by hand |

```bash
export GITHUB_TOKEN=...
python -m collect.search --service switchbot --source commits --out-dir collected/switchbot/commits
python -m collect.dedupe collected/switchbot/commits/*.txt > collected/switchbot/commits.urls
python -m collect.keyword_filter --service switchbot --source commits collected/switchbot/commits.urls
```

`--source` is one of `commits`, `issues`, `pull-requests`. The GitHub Search API returns
at most 1000 results per query, and search results change over time, so a new run does
not return the same links as the original collection.
