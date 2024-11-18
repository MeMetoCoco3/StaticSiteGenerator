import unittest

from textnode import TextNode, TextType
from conversion import (
    block_to_block_type,
    markdown_to_blocks,
    split_nodes_images,
    split_nodes_links,
    text_node_to_html_node,
    split_nodes_delimiter,
    markdown_to_nodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        n1 = TextNode("This is a text node", TextType.BOLD)
        n2 = TextNode("This is a text node", TextType.BOLD)
        n3 = TextNode("This is a different one", TextType.BOLD)
        n4 = TextNode("This is a text node", TextType.ITALIC)

        self.assertEqual(n1, n2)
        self.assertNotEqual(n1, n3)
        self.assertNotEqual(n1, n4)
        self.assertEqual(n1.url, "")

    def test_text_node_to_html_node(self):
        n1 = TextNode("This is a text node", TextType.NORMAL)
        n2 = TextNode("This is a text node", TextType.BOLD)
        n3 = TextNode("This is a text node", TextType.ITALIC)
        n4 = TextNode("This is a text node", TextType.CODE)
        n5 = TextNode("This is a text node", TextType.LINKS, "www.linkedin.com")
        n6 = TextNode("This is a text node", TextType.IMAGES, "~/images/screenshots")

        t1 = text_node_to_html_node(n1).to_html()
        t2 = text_node_to_html_node(n2).to_html()
        t3 = text_node_to_html_node(n3).to_html()
        t4 = text_node_to_html_node(n4).to_html()
        t5 = text_node_to_html_node(n5).to_html()
        t6 = text_node_to_html_node(n6).to_html()

        r1 = "This is a text node"
        r2 = "<b>This is a text node</b>"
        r3 = "<i>This is a text node</i>"
        r4 = "<code>This is a text node</code>"
        r5 = '<a href="www.linkedin.com">This is a text node</a>'
        r6 = '<img src="~/images/screenshots" alt="This is a text node">'
        self.assertEqual(t1, r1)
        self.assertEqual(t2, r2)
        self.assertEqual(t3, r3)
        self.assertEqual(t4, r4)
        self.assertEqual(t5, r5)
        self.assertEqual(t6, r6)

    def test_split_nodes_delimiter(self):
        n1 = TextNode("This is text with a `code block` word", TextType.NORMAL)
        sn1 = split_nodes_delimiter([n1], "`", TextType.CODE)

        r1 = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(sn1, r1)

        n2 = TextNode("This is text with a *italic block* word", TextType.NORMAL)
        sn2 = split_nodes_delimiter([n2], "*", TextType.ITALIC)

        r2 = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(sn2, r2)

        n3 = TextNode("This is text with a **bold** word", TextType.NORMAL)
        sn3 = split_nodes_delimiter([n3], "**", TextType.BOLD)

        r3 = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(sn3, r3)

        n4 = TextNode(
            "This is text with a `code block` and a *italic block* and a **bold block** word",
            TextType.NORMAL,
        )
        sn4 = split_nodes_delimiter([n4], "`", TextType.CODE)
        sn4 = split_nodes_delimiter(sn4, "**", TextType.BOLD)
        sn4 = split_nodes_delimiter(sn4, "*", TextType.ITALIC)
        r4 = [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.NORMAL),
        ]
        self.assertEqual(sn4, r4)

    def test_split_nodes_images(self):
        n1 = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) abcd",
            TextType.NORMAL,
        )
        sn1 = split_nodes_images([n1])
        r1 = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGES, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.IMAGES, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(" abcd", TextType.NORMAL),
        ]
        self.assertEqual(sn1, r1)

    def test_split_nodes_links(self):
        n1 = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) abcd",
            TextType.NORMAL,
        )
        sn1 = split_nodes_links([n1])
        r1 = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(" abcd", TextType.NORMAL),
        ]

        self.assertEqual(sn1, r1)

    def test_markdown_to_node(self):
        n1 = "You can also use `inline code` to highlight specific parts of the text."
        n2 = "Here's an [example link](https://example.com) to a website."
        n3 = "Let's include an image of this ![Sunset](https://i.imgur.com/uYVqVdL.jpeg) and the beautiful Earth: ![Earth Image](https://i.imgur.com/ExQH6XE.jpeg)"
        n4 = "Now, let's add a mix of formats: Here's **bold**, *italic*, and a `code snippet` in a single line."
        n5 = "Finally, some closing text with another [helpful link](https://openai.com)."

        sn1 = markdown_to_nodes(n1)
        sn2 = markdown_to_nodes(n2)
        sn3 = markdown_to_nodes(n3)
        sn4 = markdown_to_nodes(n4)
        sn5 = markdown_to_nodes(n5)

        r1 = [
            TextNode("You can also use ", TextType.NORMAL),
            TextNode("inline code", TextType.CODE),
            TextNode(" to highlight specific parts of the text.", TextType.NORMAL),
        ]

        r2 = [
            TextNode("Here's an ", TextType.NORMAL),
            TextNode("example link", TextType.LINKS, "https://example.com"),
            TextNode(" to a website.", TextType.NORMAL),
        ]

        r3 = [
            TextNode("Let's include an image of this ", TextType.NORMAL),
            TextNode("Sunset", TextType.IMAGES, "https://i.imgur.com/uYVqVdL.jpeg"),
            TextNode(" and the beautiful Earth: ", TextType.NORMAL),
            TextNode(
                "Earth Image", TextType.IMAGES, "https://i.imgur.com/ExQH6XE.jpeg"
            ),
        ]

        r4 = [
            TextNode("Now, let's add a mix of formats: Here's ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(", and a ", TextType.NORMAL),
            TextNode("code snippet", TextType.CODE),
            TextNode(" in a single line.", TextType.NORMAL),
        ]

        r5 = [
            TextNode("Finally, some closing text with another ", TextType.NORMAL),
            TextNode("helpful link", TextType.LINKS, "https://openai.com"),
            TextNode(".", TextType.NORMAL),
        ]

        self.assertEqual(sn1, r1)
        self.assertEqual(sn2, r2)
        self.assertEqual(sn3, r3)
        self.assertEqual(sn4, r4)
        self.assertEqual(sn5, r5)

    def test_markdown_to_blocks(self):
        n1 = """# This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item
            """
        r1 = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
            * This is a list item
            * This is another list item\n""",
        ]
        self.assertEqual(markdown_to_blocks(n1), r1)

    def test_block_to_block_type(self):
        n1 = """# This is a heading

            ### This is a 3 heading

            ###### THIS IS 6H

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            ```const std = @import("std")
                pub fn main() void {
                    std.debug.print("This is zig code")
                }
            ```

            >Some random quote that we have over here yeayeaheayeayeyaeyae
            aeyayeyaeyaeyaeyae
            aeyaeyyeaye

            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""

        r1 = ["H1", "H3", "H6", "p", "codeblock", "blockquote", "ul"]

        zipped = zip(markdown_to_blocks(n1), r1)
        for q, a in zipped:
            self.assertEqual(block_to_block_type(q), a)


if __name__ == "__main__":
    unittest.main()
