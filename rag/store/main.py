"""Store the specifications of one service and version in Pinecone.

    python -m rag.store.main --service switchbot --version latest --method all --index-name latest
    python -m rag.store.main --service switchbot --version latest --method separate
"""
import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv

from rag.config import SERVICES
from rag.store.specification import store_separated, store_whole

DATASET_DIR = Path(__file__).resolve().parents[2] / "dataset"


def main() -> None:
    parser = argparse.ArgumentParser(description="Store REST API specifications in Pinecone")
    parser.add_argument("--service", required=True, choices=SERVICES)
    parser.add_argument("--version", required=True, choices=["latest", "deprecated"])
    parser.add_argument(
        "--method",
        required=True,
        choices=["all", "separate"],
        help="all: one document per page / separate: code snippets and natural-language text apart",
    )
    parser.add_argument(
        "--index-name",
        help="target index for --method all (default: the version; use 'context' for DLm)",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    urls = (DATASET_DIR / args.service / "url" / f"{args.version}.txt").read_text(encoding="utf-8").split()

    if args.method == "all":
        store_whole(args.service, urls, args.index_name or args.version)
    else:
        store_separated(args.service, urls, args.version)


if __name__ == "__main__":
    main()
