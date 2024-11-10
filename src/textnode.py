from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = "") -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        ):
            return True
        return False

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(node: TextNode) -> LeafNode:
    match node.text_type:
        case TextType.NORMAL:
            return LeafNode("", node.text)
        case TextType.BOLD:
            return LeafNode("b", node.text)
        case TextType.ITALIC:
            return LeafNode("i", node.text)
        case TextType.CODE:
            return LeafNode("code", node.text)
        case TextType.LINKS:
            return LeafNode("a", node.text, {"href": node.url})
        case TextType.IMAGES:
            return LeafNode("img", "", {"src": node.url, "alt": node.text})


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL or delimiter not in node.text:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        for idx, text in enumerate(split_text):
            if idx % 2 != 0:
                new_nodes.append(TextNode(text, text_type))
            else:
                new_nodes.append(TextNode(text, TextType.NORMAL))
    return new_nodes


def main():
    pass


main()
