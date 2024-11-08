import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a different one", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.ITALIC)

        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, node4)
        self.assertEqual(node1.url, None)


if __name__ == "__main__":
    unittest.main()
