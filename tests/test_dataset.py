"""Layout of dataset/: input programs, case counts and specification URL lists."""
import csv
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


CASES = DATASET / "cases.csv"
CASE_COLUMNS = ["service", "input_path", "cases", "rh_ep_cases", "ep_cases", "lines", "counted_as"]


def load_cases():
    with CASES.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def parse_lines(spec):
    """'5-7;37' -> [5, 6, 7, 37]"""
    numbers = []
    for part in spec.split(";"):
        start, _, end = part.partition("-")
        numbers.extend(range(int(start), int(end or start) + 1))
    return numbers


class CaseCountTest(unittest.TestCase):
    """dataset/cases.csv: how the misuse cases are counted in each input program."""

    def test_columns(self):
        with CASES.open(encoding="utf-8", newline="") as f:
            self.assertEqual(next(csv.reader(f)), CASE_COLUMNS)

    def test_one_row_per_input_program(self):
        rows = [f"{row['service']}/{row['input_path']}" for row in load_cases()]
        expected = [f"{service}/{path}" for service in ("switchbot", "fitbit") for path in input_files(service)]
        self.assertEqual(rows, expected)

    def test_totals(self):
        rows = load_cases()

        def total(column, service=None):
            return sum(int(r[column]) for r in rows if service in (None, r["service"]))

        table = [
            # (description, actual, expected)
            ("all cases", total("cases"), 21),
            ("SwitchBot cases", total("cases", "switchbot"), 8),
            ("Fitbit cases", total("cases", "fitbit"), 13),
            ("RH & EP cases", total("rh_ep_cases"), 9),
            ("EP cases", total("ep_cases"), 12),
            ("SwitchBot RH & EP", total("rh_ep_cases", "switchbot"), 8),
            ("SwitchBot EP", total("ep_cases", "switchbot"), 0),
            ("Fitbit RH & EP", total("rh_ep_cases", "fitbit"), 1),
            ("Fitbit EP", total("ep_cases", "fitbit"), 12),
        ]
        for description, actual, expected in table:
            with self.subTest(description):
                self.assertEqual(actual, expected)

    def test_each_row_adds_up(self):
        for row in load_cases():
            with self.subTest(row["input_path"]):
                self.assertGreaterEqual(int(row["cases"]), 1)
                self.assertEqual(int(row["cases"]), int(row["rh_ep_cases"]) + int(row["ep_cases"]))

    def test_lines_point_at_the_deprecated_usage(self):
        # 行番号が入力ファイルの範囲内にあり、旧仕様の記述を実際に指していることを確かめる
        markers = {"switchbot": ("v1.0", "Authorization"), "fitbit": ("/sleep/", "oauth", "OAuth")}
        for row in load_cases():
            with self.subTest(f"{row['service']}/{row['input_path']}"):
                text = (DATASET / row["service"] / row["input_path"]).read_text(encoding="utf-8").splitlines()
                numbers = parse_lines(row["lines"])
                self.assertGreaterEqual(min(numbers), 1)
                self.assertLessEqual(max(numbers), len(text))
                for number in numbers:
                    line = text[number - 1]
                    previous = text[number - 2] if number > 1 else ""
                    # 複数行にまたがる呼び出しは、直前の行までを同じ記述として扱う
                    self.assertTrue(
                        any(m in line or m in previous for m in markers[row["service"]]),
                        f"line {number}: {line!r}",
                    )


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
