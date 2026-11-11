"""Consistency of results/ with the prompt templates and the input programs.

The stored outputs are the raw material of Table 4, so these tests check that every
output file was produced from a prompt template and an input program in this repository.
"""
import string
import unittest
from pathlib import Path

from rag.config import CONFIGURATIONS, TRIALS

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"
RESULTS = ROOT / "results"
PROMPTS = ROOT / "rag" / "prompts"

BASELINE = "0_BL"
ALL_CONFIGURATIONS = [BASELINE] + list(CONFIGURATIONS)
RESPONSE_HEADER = "# LLM Response\n"
QUERY_HEADER = "\n\n# User Query\n"


def input_files():
    return sorted(
        p
        for service in ("switchbot", "fitbit")
        for source in ("commits", "issues", "pull-requests")
        for p in (DATASET / service / source).glob("*")
        if p.is_file()
    )


def result_files(configuration, input_file):
    relative = input_file.relative_to(DATASET)
    directory = RESULTS / configuration / relative.parent / relative.stem
    return [directory / f"{trial}.md" for trial in range(1, TRIALS + 1)]


def stored_prompt(result_file):
    text = result_file.read_text(encoding="utf-8")
    return text[text.index(QUERY_HEADER) + len(QUERY_HEADER):]


def literal_segments(template):
    return [literal for literal, _, _, _ in string.Formatter().parse(template)]


class ResultLayoutTest(unittest.TestCase):
    def test_twelve_configurations(self):
        stored = sorted(p.name for p in RESULTS.iterdir() if p.is_dir())
        self.assertEqual(stored, sorted(ALL_CONFIGURATIONS))
        self.assertEqual(len(stored), 12)

    def test_each_configuration_has_five_outputs_per_input(self):
        for configuration in ALL_CONFIGURATIONS:
            with self.subTest(configuration):
                expected = sorted(f for i in input_files() for f in result_files(configuration, i))
                actual = sorted((RESULTS / configuration).rglob("*.md"))
                self.assertEqual(actual, expected)
                self.assertEqual(len(actual), 80)

    def test_output_files_have_response_and_prompt_sections(self):
        for configuration in ALL_CONFIGURATIONS:
            for result_file in sorted((RESULTS / configuration).rglob("*.md")):
                with self.subTest(str(result_file.relative_to(RESULTS))):
                    text = result_file.read_text(encoding="utf-8")
                    self.assertTrue(text.startswith(RESPONSE_HEADER))
                    self.assertEqual(text.count(QUERY_HEADER), 1)


class ResultProvenanceTest(unittest.TestCase):
    def test_stored_prompt_follows_the_template_and_contains_the_input(self):
        for configuration in ALL_CONFIGURATIONS:
            segments = literal_segments((PROMPTS / f"{configuration}.md").read_text(encoding="utf-8"))
            for input_file in input_files():
                program = input_file.read_text(encoding="utf-8")
                for result_file in result_files(configuration, input_file):
                    with self.subTest(str(result_file.relative_to(RESULTS))):
                        prompt = stored_prompt(result_file)
                        position = 0
                        for segment in segments:
                            found = prompt.find(segment, position)
                            self.assertNotEqual(found, -1, f"template text missing: {segment[:60]!r}")
                            position = found + len(segment)
                        self.assertIn(program, prompt)

    def test_prompt_is_identical_across_the_five_trials(self):
        for configuration in ALL_CONFIGURATIONS:
            for input_file in input_files():
                with self.subTest(f"{configuration}/{input_file.relative_to(DATASET)}"):
                    prompts = {stored_prompt(f) for f in result_files(configuration, input_file)}
                    self.assertEqual(len(prompts), 1)

    def test_baseline_prompt_lists_exactly_the_specification_urls(self):
        for service in ("switchbot", "fitbit"):
            with self.subTest(service):
                urls = []
                for version in ("deprecated", "latest"):
                    urls += (DATASET / service / "url" / f"{version}.txt").read_text(encoding="utf-8").split()
                for result_file in sorted((RESULTS / BASELINE / service).rglob("*.md")):
                    prompt = stored_prompt(result_file)
                    links = prompt[prompt.index("## Link\n") + len("## Link\n"):prompt.index("\n\n## Code")]
                    self.assertEqual(sorted(links.split("\n")), sorted(urls))

    def test_retrieved_chunks_stay_within_top_k_per_database(self):
        # 1 DB あたり最大 60 チャンク。構成の DB 数を超える量が入っていないことを確かめる
        for configuration, databases in CONFIGURATIONS.items():
            limit = 60 * len(databases)
            for result_file in sorted((RESULTS / configuration).rglob("1.md")):
                with self.subTest(str(result_file.relative_to(RESULTS))):
                    chunks = stored_prompt(result_file).count("【Context No.")
                    self.assertGreater(chunks, 0)
                    self.assertLessEqual(chunks, limit)


if __name__ == "__main__":
    unittest.main()
