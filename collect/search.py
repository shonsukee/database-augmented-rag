"""Step 1: collect links to commits, closed issues and closed pull requests.

    python -m collect.search --service switchbot --source commits --out-dir collected/switchbot/commits

One JSON file of URLs is written per search query.
"""
import argparse
import json
import os
from pathlib import Path
from typing import List
from urllib.parse import quote

import requests
from dotenv import load_dotenv

from collect.queries import SEARCH_QUERIES

SOURCES = ("commits", "issues", "pull-requests")
PER_PAGE = 100
# The GitHub Search API returns at most 1000 results per query.
MAX_RESULTS = 1000


def search_url(query: str, source: str, page: int) -> str:
    encoded = quote(query)
    if source == "commits":
        url = f"https://api.github.com/search/commits?q={encoded}"
    elif source == "issues":
        url = f"https://api.github.com/search/issues?q={encoded}+is:issue+is:closed"
    elif source == "pull-requests":
        url = f"https://api.github.com/search/issues?q={encoded}+is:pr+is:closed"
    else:
        raise ValueError(f"unknown source: {source!r} (choose from {', '.join(SOURCES)})")
    return f"{url}&per_page={PER_PAGE}&page={page}"


def output_name(query: str, existing_files: int) -> str:
    """File name for the results of one query: a running number and the last word of the query."""
    word = query.split(" ")[-1] if " " in query else query.split("/")[-1]
    return f"{existing_files + 1}-{word}.txt"


def search(query: str, source: str, token: str) -> List[str]:
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}"}
    urls: List[str] = []
    page = 1
    while len(urls) < MAX_RESULTS:
        response = requests.get(search_url(query, source, page), headers=headers)
        if response.status_code != 200:
            print(f"Failed query: {query} | Status: {response.status_code}")
            break
        items = response.json().get("items", [])
        if not items:
            break
        urls += [item["html_url"] for item in items]
        page += 1
    return urls


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect candidate links with the GitHub Search API")
    parser.add_argument("--service", required=True, choices=sorted(SEARCH_QUERIES))
    parser.add_argument("--source", required=True, choices=SOURCES)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN is not set")

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for query in SEARCH_QUERIES[args.service]:
        urls = search(query, args.source, token)
        print(f"{query}: {len(urls)} links")
        if urls:
            existing = sum(1 for path in out_dir.iterdir() if path.is_file())
            (out_dir / output_name(query, existing)).write_text(json.dumps(urls, indent=4), encoding="utf-8")


if __name__ == "__main__":
    main()
