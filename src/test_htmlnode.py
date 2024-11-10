from htmlnode import HTMLnode, LeafNode, ParentNode
import unittest


class Test_htmlnode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLnode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            node1.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

        self.assertNotEqual(
            node1.props_to_html(), ' href="https://www.Alicuecano.com" target="_blank"'
        )

    def test_to_html(self):
        l1 = LeafNode("p", "This is a paragraph of text.").to_html()
        self.assertEqual(l1, "<p>This is a paragraph of text.</p>")
        l2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html()
        self.assertEqual(l2, '<a href="https://www.google.com">Click me!</a>')


class Test_parentnode(unittest.TestCase):
    def test_to_html(self):
        p1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode("", "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode("", "Normal text"),
            ],
        )
        r1 = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(p1.to_html(), r1)
        p2 = ParentNode(
            "div",
            [
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode("", "Item 1")]),
                        ParentNode("li", [LeafNode("", "Item 2")]),
                    ],
                ),
                LeafNode("p", "Paragraph"),
            ],
        )
        r2 = "<div><ul><li>Item 1</li><li>Item 2</li></ul><p>Paragraph</p></div>"
        self.assertEqual(p2.to_html(), r2)
