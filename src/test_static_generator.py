import unittest
from static_generator import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_extract_title_basic(self):
        title = extract_title("# Hello")
        self.assertEqual("Hello", title)

    def test_extract_title_strips_whitespace(self):
        title = extract_title("#    Hello World   ")
        self.assertEqual("Hello World", title)

    def test_extract_title_multiple_blocks_returns_last(self):
        markdown = "# First\n\nSome text\n\n# Second"
        title = extract_title(markdown)
        self.assertEqual("First", title)

    def test_extract_title_ignores_non_h1_headers(self):
        markdown = "## Not this\n\n### Nor this\n\n# Yes This"
        title = extract_title(markdown)
        self.assertEqual("Yes This", title)

    def test_extract_title_no_title_raises_exception(self):
        markdown = "This has no title"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual("Title is required", str(context.exception))

    def test_extract_title_with_text_before(self):
        markdown = "Intro text\n\n# Real Title"
        title = extract_title(markdown)
        self.assertEqual("Real Title", title)