from htmlnode import HTMLnode, LeafNode
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
