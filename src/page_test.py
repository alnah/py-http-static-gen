import unittest

from page import MarkdownTitleError, extract_title


class TestExtractTitle(unittest.TestCase):
    def test_correct_h1_md(self):
        want = "Title"
        got = extract_title("# Title")
        self.assertEqual(want, got)

    def test_incorrect_markdown_heading(self):
        with self.assertRaises(MarkdownTitleError):
            extract_title("## Incorrect heading level")

    def test_not_markdown_heading(self):
        with self.assertRaises(MarkdownTitleError):
            extract_title("Not markdown heading")

    def test_empty_text(self):
        with self.assertRaises(ValueError):
            extract_title("")

class TestGeneratePage(unittest.TestCase):
    
