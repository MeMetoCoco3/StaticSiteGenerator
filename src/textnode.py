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


def text_to_nodes(text: str) -> list[TextNode]:
    node = [TextNode(text, TextType.NORMAL)]

    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "*", TextType.ITALIC)
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    node = split_nodes_images(node)
    node = split_nodes_links(node)
    return node


def markdown_to_blocks(text: str) -> list[str]:
    split_text = text.split("\n\n")
    for idx, line in enumerate(split_text):
        split_text[idx] = line.strip()
    # Remove empty strings
    return [x for x in split_text if x != ""]


def block_to_block_type(block_str: str) -> str:
    match block_str[0]:
        case "#":
            c = 1
            for i in block_str[1:6]:
                if i == "#":
                    c += 1
                    continue
                break
            return f"H{c}"
        case "`":
            c = 1
            for i in block_str[1:3]:
                if i == "`":
                    c += 1
                    continue
                break

            if c == 3:
                return "CODE"
        case ">":
            return "QUOTE"
        case "*" | "-":
            return "UL"

        case _:
            number = ""
            for val in block_str:
                if val.isnumeric():
                    number = number + val
                    continue
                break
            if number:
                return number
    return "NORMAL"


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

        if node.text_type == TextType.IMAGES or not image_nodes:
            new_nodes.append(node)
            continue
        for alt_text, link in image_nodes:
            i_formated = f"![{alt_text}]({link})"
            start_image = node.text.find(i_formated, cursor)
            if start_image > cursor:
                new_nodes.append(
                    TextNode(node.text[cursor:start_image], node.text_type)
                )
            new_nodes.append(TextNode(alt_text, TextType.IMAGES, link))
            cursor = start_image + len(i_formated)
        if len(node.text) > cursor:
            new_nodes.append(TextNode(node.text[cursor:], node.text_type))
    return new_nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        # Skip if it's already an image node
        if node.text_type == TextType.IMAGES:
            new_nodes.append(node)
            continue

        url_nodes = extract_markdown_links(node.text)
        cursor = 0
        for alt_text, link in url_nodes:
            i_formated = f"[{alt_text}]({link})"
            start_link = node.text.find(i_formated, cursor)
            if start_link > cursor:
                new_nodes.append(TextNode(node.text[cursor:start_link], node.text_type))
            new_nodes.append(TextNode(alt_text, TextType.LINKS, link))
            cursor = start_link + len(i_formated)
        if len(node.text) > cursor:
            new_nodes.append(TextNode(node.text[cursor:], node.text_type))
    return new_nodes


def main():
    n3 = """# This is a heading

### This is a 3 heading

######### THIS IS A NORMAL

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
    for i in markdown_to_blocks(n3):
        print(block_to_block_type(i))


main()
