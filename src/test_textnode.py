import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


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


if __name__ == "__main__":
    unittest.main()
