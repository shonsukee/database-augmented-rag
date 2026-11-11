"""Step 3: keep only the links whose diff or discussion mentions the deprecated API.

    python -m collect.keyword_filter --service switchbot --source commits collected/switchbot/commits.urls

Prints the kept links first and the rejected links after a separator. The kept links
are then inspected by hand.
"""
import argparse
import os
import re
import shutil
import tempfile
from typing import Iterable, List, Tuple

import requests
from dotenv import load_dotenv

from collect.queries import FILTER_KEYWORDS

SOURCES = ("commits", "issues", "pull-requests")
URL_PATTERN = re.compile(r"""https?://[^\s,\[\]"'<>]+""")
SEPARATORS = {"commits": "/commit/", "issues": "/issues/", "pull-requests": "/pull/"}


def extract_urls(text: str) -> List[str]:
    return URL_PATTERN.findall(text)


def split_url(url: str) -> Tuple[str, str]:
    """Split a commit, issue or pull request URL into (repository URL, commit hash or number)."""
    for separator in SEPARATORS.values():
        if separator in url:
            repository, identifier = url.split(separator, 1)
            return repository, identifier
    raise ValueError(f"not a commit, issue or pull request URL: {url}")


def contains_keyword(text: str, keywords: Iterable[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def api_url(repository: str) -> str:
    return repository.replace("https://github.com/", "https://api.github.com/repos/")


def commit_matches(repository: str, commit_hash: str, keywords: List[str]) -> bool:
    """True when the diff of the commit against its first parent contains a keyword."""
    import git  # GitPython; imported here so the other sources work without it

    directory = tempfile.mkdtemp(prefix="collect-")
    try:
        commit = git.Repo.clone_from(repository + ".git", directory).commit(commit_hash)
        diffs = commit.diff(commit.parents[0], create_patch=True) if commit.parents else commit.diff(None, create_patch=True)
        return any(contains_keyword(diff.diff.decode("utf-8", errors="replace"), keywords) for diff in diffs)
    except git.exc.GitError as error:
        print(f"Git error: {error}")
        return False
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def issue_matches(repository: str, number: str, keywords: List[str], headers: dict) -> bool:
    """True when a comment of the issue contains a keyword."""
    response = requests.get(f"{api_url(repository)}/issues/{number}/comments", headers=headers)
    response.raise_for_status()
    return any(contains_keyword(comment.get("body") or "", keywords) for comment in response.json())


def pull_request_matches(repository: str, number: str, keywords: List[str], headers: dict) -> bool:
    """True when a review comment or the patch of a changed file contains a keyword."""
    base = f"{api_url(repository)}/pulls/{number}"
    comments = requests.get(f"{base}/comments", headers=headers)
    comments.raise_for_status()
    if any(contains_keyword(comment.get("body") or "", keywords) for comment in comments.json()):
        return True
    files = requests.get(f"{base}/files", headers=headers)
    files.raise_for_status()
    return any(contains_keyword(changed.get("patch") or "", keywords) for changed in files.json())


def matches(source: str, url: str, keywords: List[str], headers: dict) -> bool:
    repository, identifier = split_url(url)
    try:
        if source == "commits":
            return commit_matches(repository, identifier, keywords)
        if source == "issues":
            return issue_matches(repository, identifier, keywords, headers)
        return pull_request_matches(repository, identifier, keywords, headers)
    except requests.exceptions.RequestException as error:
        print(f"Request error: {error}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Filter collected links by keywords of the deprecated API")
    parser.add_argument("--service", required=True, choices=sorted(FILTER_KEYWORDS))
    parser.add_argument("--source", required=True, choices=SOURCES)
    parser.add_argument("files", nargs="+", help="files that list the collected URLs")
    args = parser.parse_args()

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    keywords = FILTER_KEYWORDS[args.service]

    kept, rejected = [], []
    for path in args.files:
        with open(path, encoding="utf-8") as f:
            for url in extract_urls(f.read()):
                (kept if matches(args.source, url, keywords, headers) else rejected).append(url)

    print(f"URLs contain({len(kept)}):")
    print("\n".join(kept))
    print(f"\nURLs not contain({len(rejected)}):")
    print("\n".join(rejected))


if __name__ == "__main__":
    main()
