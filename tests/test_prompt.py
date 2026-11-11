"""Prompt construction and output formatting (no API access needed)."""
import tempfile
import unittest
from collections import namedtuple
from pathlib import Path

from rag.config import CONFIGURATIONS, GENERATION_MODEL, SIMILARITY_TOP_K, TRIALS
from rag.repair import output, prompt

Node = namedtuple("Node", ["score", "text"])


class ConfigurationTest(unittest.TestCase):
    def test_experimental_settings(self):
        self.assertEqual(GENERATION_MODEL, "gpt-4o")
        self.assertEqual(SIMILARITY_TOP_K, 60)
        self.assertEqual(TRIALS, 5)

    def test_databases_match_table_2(self):
        # (configuration, number of databases, databases searched)
        table = [
            ("1_D", 1, ["deprecated"]),
            ("2_L", 1, ["latest"]),
            ("3_DLm", 1, ["context"]),
            ("4_DL", 2, ["deprecated", "latest"]),
            ("5_Ds", 2, ["deprecated_natural_language", "deprecated_code"]),
            ("6_Ls", 2, ["latest_natural_language", "latest_code"]),
            ("7_DLs", 3, ["deprecated", "latest_natural_language", "latest_code"]),
            ("8_DsL", 3, ["deprecated_natural_language", "deprecated_code", "latest"]),
            (
                "9_DsLs",
                4,
                ["deprecated_natural_language", "deprecated_code", "latest_natural_language", "latest_code"],
            ),
            ("10_DcLc", 2, ["deprecated_code", "latest_code"]),
            ("11_DtLt", 2, ["deprecated_natural_language", "latest_natural_language"]),
        ]
        self.assertEqual([row[0] for row in table], list(CONFIGURATIONS))
        for configuration, count, databases in table:
            with self.subTest(configuration):
                self.assertEqual(len(CONFIGURATIONS[configuration]), count)
                self.assertEqual(sorted(CONFIGURATIONS[configuration]), sorted(databases))

    def test_template_variables_are_the_databases_plus_the_input(self):
        for configuration, databases in CONFIGURATIONS.items():
            with self.subTest(configuration):
                variables = prompt.template_variables(prompt.load_template(configuration))
                self.assertEqual(sorted(variables), sorted(list(databases) + ["user_query"]))


class LoadTemplateTest(unittest.TestCase):
    def test_rejects_configurations_that_the_pipeline_does_not_run(self):
        table = [
            ("baseline was run in ChatGPT, not by this pipeline", "0_BL"),
            ("unknown name", "12_XYZ"),
            ("empty", ""),
        ]
        for description, name in table:
            with self.subTest(description):
                with self.assertRaises(ValueError):
                    prompt.load_template(name)


class IndexNameTest(unittest.TestCase):
    def test_index_name(self):
        table = [
            ("deprecated", "deprecated"),
            ("latest", "latest"),
            ("context", "context"),
            ("deprecated_natural_language", "deprecated-natural-language"),
            ("latest_code", "latest-code"),
        ]
        for variable, expected in table:
            with self.subTest(variable):
                self.assertEqual(prompt.index_name(variable), expected)


class FormatNodesTest(unittest.TestCase):
    def test_format_nodes(self):
        table = [
            ("no node", [], ""),
            ("one node", [Node(0.5, "alpha")], "【Context No.1】\n[similarity: 0.5]\nalpha"),
            (
                "nodes are numbered and separated by a blank line",
                [Node(0.59, "alpha"), Node(0.41, "beta\ngamma")],
                "【Context No.1】\n[similarity: 0.59]\nalpha\n\n【Context No.2】\n[similarity: 0.41]\nbeta\ngamma",
            ),
        ]
        for description, nodes, expected in table:
            with self.subTest(description):
                self.assertEqual(prompt.format_nodes(nodes), expected)


class BuildPromptTest(unittest.TestCase):
    def test_fills_every_variable(self):
        template = "## Spec\n{latest}\n\n## Input Code\n{user_query}"
        built = prompt.build_prompt(template, {"latest": "SPEC", "user_query": "CODE {x}"})
        self.assertEqual(built, "## Spec\nSPEC\n\n## Input Code\nCODE {x}")

    def test_missing_variable_is_an_error(self):
        with self.assertRaises(KeyError):
            prompt.build_prompt("{latest}{user_query}", {"user_query": "CODE"})

    def test_matches_the_layout_of_a_stored_prompt(self):
        # 保存済みの DsLs のプロンプトを、テンプレートと値から同じ文面で組み立て直せること
        root = Path(__file__).resolve().parents[1]
        stored = (root / "results/9_DsLs/switchbot/commits/5/1.md").read_text(encoding="utf-8")
        stored = stored[stored.index("\n\n# User Query\n") + len("\n\n# User Query\n"):]
        template = prompt.load_template("9_DsLs")
        values = prompt.split_prompt(template, stored)
        self.assertEqual(
            values["user_query"], (root / "dataset/switchbot/commits/5.py").read_text(encoding="utf-8")
        )
        self.assertEqual(prompt.build_prompt(template, values), stored)


class WrapResponseTest(unittest.TestCase):
    def test_wrap_response(self):
        table = [
            ("bare code is fenced with the file extension", "x = 1", "py", "```py\nx = 1\n```"),
            ("already fenced code is kept", "```python\nx = 1\n```", "py", "```python\nx = 1\n```"),
            ("fence inside prose is kept", "Here:\n```\nx\n```", "rb", "Here:\n```\nx\n```"),
        ]
        for description, response, language, expected in table:
            with self.subTest(description):
                self.assertEqual(output.wrap_response(response, language), expected)


class SaveResultTest(unittest.TestCase):
    def test_file_layout(self):
        table = [
            ("response and prompt", "RESPONSE", "PROMPT", "# LLM Response\nRESPONSE\n\n# User Query\nPROMPT"),
            ("empty response", "", "PROMPT", "# LLM Response\nNone\n\n# User Query\nPROMPT"),
        ]
        for description, response, user_prompt, expected in table:
            with self.subTest(description), tempfile.TemporaryDirectory() as tmp:
                directory = output.result_dir(tmp, "9_DsLs", "switchbot", "commits", "5.py")
                self.assertEqual(directory, Path(tmp) / "9_DsLs" / "switchbot" / "commits" / "5")
                path = output.save_result(directory, 3, user_prompt, response)
                self.assertEqual(path, directory / "3.md")
                self.assertEqual(path.read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    unittest.main()
