from enum import Enum


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"
    QUOTES = "blockquote"
    UL = "ul"
    OL = "ol"
    CODEBLOCK = "codex"
    HEADER1 = "h1"
    HEADER2 = "h2"
    HEADER3 = "h3"
    HEADER4 = "h4"
    HEADER5 = "h5"
    HEADER6 = "h6"


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


def main():
    pass
