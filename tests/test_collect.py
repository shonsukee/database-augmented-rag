"""Pure helpers of the dataset collection scripts (no GitHub access needed)."""
import unittest

from collect import dedupe, keyword_filter, queries, search


class SearchUrlTest(unittest.TestCase):
    def test_search_url(self):
        table = [
            (
                "commits",
                "switchbot API v1.1",
                2,
                "https://api.github.com/search/commits?q=switchbot%20API%20v1.1&per_page=100&page=2",
            ),
            (
                "issues",
                "fitbit support oauth2",
                1,
                "https://api.github.com/search/issues?q=fitbit%20support%20oauth2+is:issue+is:closed&per_page=100&page=1",
            ),
            (
                "pull-requests",
                "api.fitbit.com/oauth2",
                1,
                "https://api.github.com/search/issues?q=api.fitbit.com/oauth2+is:pr+is:closed&per_page=100&page=1",
            ),
        ]
        for source, query, page, expected in table:
            with self.subTest(source):
                self.assertEqual(search.search_url(query, source, page), expected)

    def test_unknown_source_is_rejected(self):
        with self.assertRaises(ValueError):
            search.search_url("switchbot", "code", 1)


class OutputNameTest(unittest.TestCase):
    def test_output_name(self):
        table = [
            ("last word of a phrase", "switchbot support v1.1", 3, "4-v1.1.txt"),
            ("last path element of a URL-like query", "api.fitbit.com/1.2/user/-/sleep/date/", 0, "1-.txt"),
            ("single word", "www.fitbit.com/oauth/authorize", 9, "10-authorize.txt"),
        ]
        for description, query, existing, expected in table:
            with self.subTest(description):
                self.assertEqual(search.output_name(query, existing), expected)


class QueriesTest(unittest.TestCase):
    def test_queries_exist_for_both_services(self):
        self.assertEqual(sorted(queries.SEARCH_QUERIES), ["fitbit", "switchbot"])
        for service, items in queries.SEARCH_QUERIES.items():
            with self.subTest(service):
                self.assertTrue(items)
                self.assertEqual(len(items), len(set(items)))

    def test_keywords_exist_for_both_services(self):
        self.assertEqual(sorted(queries.FILTER_KEYWORDS), ["fitbit", "switchbot"])


class DedupeTest(unittest.TestCase):
    def test_dedupe(self):
        table = [
            ("keeps first occurrence and order", ["a/commit/1", "b/commit/2", "a/commit/1"], ["a/commit/1", "b/commit/2"]),
            ("drops documentation files", ["a/blob/README.md", "a/blob/x.py", "a/notes.txt"], ["a/blob/x.py"]),
            ("ignores blank lines", ["", "a/commit/1", "  "], ["a/commit/1"]),
        ]
        for description, urls, expected in table:
            with self.subTest(description):
                self.assertEqual(dedupe.dedupe(urls), expected)


class KeywordFilterTest(unittest.TestCase):
    def test_split_url(self):
        table = [
            (
                "commit",
                "https://github.com/y-yu/kindle-clock/commit/17ea869",
                ("https://github.com/y-yu/kindle-clock", "17ea869"),
            ),
            (
                "issue",
                "https://github.com/googleworkspace/apps-script-oauth1/issues/8",
                ("https://github.com/googleworkspace/apps-script-oauth1", "8"),
            ),
            (
                "pull request",
                "https://github.com/ytkg/switchbot/pull/15",
                ("https://github.com/ytkg/switchbot", "15"),
            ),
        ]
        for description, url, expected in table:
            with self.subTest(description):
                self.assertEqual(keyword_filter.split_url(url), expected)

    def test_split_url_rejects_other_urls(self):
        with self.assertRaises(ValueError):
            keyword_filter.split_url("https://github.com/ytkg/switchbot/blob/main/README.md")

    def test_contains_keyword(self):
        table = [
            ("match", "url = 'https://api.switch-bot.com/v1.0/devices'", ["v1.0", "v1.1"], True),
            ("no match", "print('hello')", ["v1.0", "v1.1"], False),
            ("empty text", "", ["v1.0"], False),
        ]
        for description, text, keywords, expected in table:
            with self.subTest(description):
                self.assertEqual(keyword_filter.contains_keyword(text, keywords), expected)

    def test_extract_urls(self):
        text = '[\n    "https://github.com/a/b/commit/1",\n    "https://github.com/c/d/pull/2"\n]'
        self.assertEqual(
            keyword_filter.extract_urls(text),
            ["https://github.com/a/b/commit/1", "https://github.com/c/d/pull/2"],
        )


if __name__ == "__main__":
    unittest.main()
