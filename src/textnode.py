from enum import Enum
from htmlnode import LeafNode
from extract import extract_markdown_links, extract_markdown_images


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


def split_nodes_images(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        image_nodes = extract_markdown_images(node.text)
        cursor = 0
        for alt_text, link in image_nodes:
            i_formated = f"![{alt_text}]({link})"
            start_image = node.text.find(i_formated, cursor)
            if start_image > cursor:
                new_nodes.append(
                    TextNode(node.text[cursor:start_image], TextType.NORMAL)
                )
            new_nodes.append(TextNode(alt_text, TextType.IMAGES, link))
            cursor = start_image + len(i_formated)
        if len(node.text) > cursor:
            new_nodes.append(TextNode(node.text[cursor:], TextType.NORMAL))
    return new_nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        url_nodes = extract_markdown_links(node.text)
        cursor = 0
        for alt_text, link in url_nodes:
            i_formated = f"[{alt_text}]({link})"
            start_image = node.text.find(i_formated, cursor)
            if start_image > cursor:
                new_nodes.append(
                    TextNode(node.text[cursor:start_image], TextType.NORMAL)
                )
            new_nodes.append(TextNode(alt_text, TextType.LINKS, link))
            cursor = start_image + len(i_formated)
        if len(node.text) > cursor:
            new_nodes.append(TextNode(node.text[cursor:], TextType.NORMAL))
    return new_nodes


def main():
    pass


main()
