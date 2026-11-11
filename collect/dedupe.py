"""Step 2: merge the link lists of all queries and drop duplicates.

    python -m collect.dedupe collected/switchbot/commits/*.txt > collected/switchbot/commits.urls
"""
import sys
from typing import Iterable, List

from collect.keyword_filter import extract_urls

# Documentation files cannot contain a client-side misuse.
DOCUMENT_SUFFIXES = (".txt", ".md", ".rst", ".plist", ".readme", ".mdx", ".sample")


def dedupe(urls: Iterable[str]) -> List[str]:
    seen = set()
    kept = []
    for url in urls:
        url = url.strip()
        if not url or url in seen or url.endswith(DOCUMENT_SUFFIXES):
            continue
        seen.add(url)
        kept.append(url)
    return kept


def main() -> None:
    urls: List[str] = []
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            urls += extract_urls(f.read())
    print("\n".join(dedupe(urls)))


if __name__ == "__main__":
    main()
