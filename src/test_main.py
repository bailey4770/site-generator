import unittest
from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_with_heading(self):
        md = "# title\n\nsome paragraph"
        actual = extract_title(md)
        expected = "title"
        self.assertEqual(actual, expected)

    def test_long_heading(self):
        md = "# This is a long heading"
        actual = extract_title(md)
        expected = "This is a long heading"
        self.assertEqual(actual, expected)

    def test_no_title(self):
        md = "there is no heading"
        with self.assertRaises(ValueError):
            _ = extract_title(md)

    def test_heading_but_no_title(self):
        md = """## small heading

- list
- list
"""
        with self.assertRaises(ValueError):
            _ = extract_title(md)

    def test_misplace_title(self):
        md = """some paragraph

- unordered

1. ordered
2. list

# title
"""
        actual = extract_title(md)
        expected = "title"
        self.assertEqual(actual, expected)
