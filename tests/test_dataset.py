"""Layout of dataset/: input programs and specification URL lists."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "dataset"


def input_files(service):
    return sorted(
        p.relative_to(DATASET / service).as_posix()
        for source in ("commits", "issues", "pull-requests")
        for p in (DATASET / service / source).glob("*")
        if p.is_file()
    )


class InputProgramTest(unittest.TestCase):
    def test_input_programs(self):
        table = [
            (
                "switchbot",
                [
                    "commits/1.scala",
                    "commits/2.py",
                    "commits/3.py",
                    "commits/4.py",
                    "commits/5.py",
                    "pull-requests/1.py",
                    "pull-requests/2.py",
                    "pull-requests/3.rb",
                ],
            ),
            (
                "fitbit",
                [
                    "commits/1.go",
                    "commits/2.java",
                    "commits/3.json",
                    "commits/4.pm",
                    "commits/5.rb",
                    "issues/5.js",
                    "issues/6.py",
                    "pull-requests/1.py",
                ],
            ),
        ]
        for service, expected in table:
            with self.subTest(service):
                self.assertEqual(input_files(service), expected)


class SpecificationUrlTest(unittest.TestCase):
    def test_url_lists_exist_for_each_service_and_version(self):
        table = [
            ("switchbot", "deprecated", 1),
            ("switchbot", "latest", 1),
            ("fitbit", "deprecated", 1),
            ("fitbit", "latest", 126),
        ]
        for service, version, expected in table:
            with self.subTest(f"{service}/{version}"):
                urls = (DATASET / service / "url" / f"{version}.txt").read_text(encoding="utf-8").split()
                self.assertEqual(len(urls), expected)
                self.assertTrue(all(u.startswith("https://") for u in urls))


if __name__ == "__main__":
    unittest.main()
