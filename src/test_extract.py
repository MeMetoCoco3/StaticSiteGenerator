import unittest
from extract import extract_markdown_images, extract_markdown_links


class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        # Basic tests
        self.assertEqual(
            extract_markdown_images("![alt text](https://example.com/image.jpg)"),
            [("alt text", "https://example.com/image.jpg")],
        )
        self.assertEqual(
            extract_markdown_images(
                "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
            ),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")],
        )
        self.assertEqual(
            extract_markdown_images(
                "Multiple images: ![one](https://img1.png) and ![two](https://img2.png)"
            ),
            [("one", "https://img1.png"), ("two", "https://img2.png")],
        )

        # Edge cases
        self.assertEqual(extract_markdown_images("No images here!"), [])
        self.assertEqual(
            extract_markdown_images("![alt](missing-url)"), [("alt", "missing-url")]
        )
        self.assertEqual(
            extract_markdown_images("Malformed ![no end link](https://example.com"), []
        )

        # Nested parentheses in URLs
        """
        self.assertEqual(
            extract_markdown_images("![nested](https://example.com/path_(extra).png)"),
            [("nested", "https://example.com/path_(extra).png")],
        )
        """

    def test_extract_markdown_links(self):
        # Basic tests
        self.assertEqual(
            extract_markdown_links(
                "This is a link [to Google](https://www.google.com)"
            ),
            [("to Google", "https://www.google.com")],
        )
        self.assertEqual(
            extract_markdown_links(
                "Multiple links: [one](https://one.com) and [two](https://two.com)"
            ),
            [("one", "https://one.com"), ("two", "https://two.com")],
        )

        # Edge cases
        self.assertEqual(extract_markdown_links("No links here."), [])
        self.assertEqual(extract_markdown_links("[Invalid](missing-url)"), [])
        self.assertEqual(
            extract_markdown_links("Malformed [no end link](https://example.com"), []
        )

        # Links with spaces before and after
        self.assertEqual(
            extract_markdown_links(
                " A link [to GitHub](https://github.com) and another [to Python](https://python.org) "
            ),
            [("to GitHub", "https://github.com"), ("to Python", "https://python.org")],
        )

        # Nested parentheses in URLs
        self.assertEqual(
            extract_markdown_links(
                "Check [this](https://example.com/path_(extra)) link."
            ),
            [("this", "https://example.com/path_(extra)")],
        )


if __name__ == "__main__":
    unittest.main()
