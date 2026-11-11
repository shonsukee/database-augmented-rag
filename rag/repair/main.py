"""Repair the input programs of one service with one RAG configuration.

    python -m rag.repair.main --service switchbot --source-types commits pull-requests \
        --configuration 9_DsLs --output-dir ./output
"""
import argparse
import logging
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from rag.config import CONFIGURATIONS, SERVICES, TRIALS
from rag.repair import output, prompt
from rag.repair.generator import generate
from rag.repair.retriever import retrieve

DATASET_DIR = Path(__file__).resolve().parents[2] / "dataset"


def repair_file(client: OpenAI, service: str, configuration: str, input_file: Path, output_dir: str) -> None:
    template = prompt.load_template(configuration)
    program = input_file.read_text(encoding="utf-8")

    # The input program itself is the search query for every database.
    values = {prompt.INPUT_VARIABLE: program}
    for database in CONFIGURATIONS[configuration]:
        nodes = retrieve(service, database, program)
        if not nodes:
            logging.warning("no chunk retrieved from %s for %s", database, input_file)
        values[database] = prompt.format_nodes(nodes)
    user_prompt = prompt.build_prompt(template, values)

    directory = output.result_dir(output_dir, configuration, service, input_file.parent.name, input_file.name)
    language = input_file.suffix.lstrip(".")
    for trial in range(1, TRIALS + 1):
        response = output.wrap_response(generate(client, service, user_prompt), language)
        output.save_result(directory, trial, user_prompt, response)
        logging.info("%s trial %d saved", directory, trial)


def main() -> None:
    parser = argparse.ArgumentParser(description="Repair REST API misuse with a RAG configuration")
    parser.add_argument("--service", required=True, choices=SERVICES)
    parser.add_argument("--source-types", nargs="+", required=True, help="commits, issues, pull-requests")
    parser.add_argument("--configuration", required=True, choices=list(CONFIGURATIONS))
    # The default is not results/, so a run never overwrites the outputs reported in the paper.
    parser.add_argument("--output-dir", default="./output")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    client = OpenAI()

    for source_type in args.source_types:
        for input_file in sorted((DATASET_DIR / args.service / source_type).iterdir()):
            if input_file.is_file():
                repair_file(client, args.service, args.configuration, input_file, args.output_dir)


if __name__ == "__main__":
    main()
