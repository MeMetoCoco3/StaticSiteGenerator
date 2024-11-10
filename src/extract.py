import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # No nested parentesis....YET
    return re.findall(r"!\[([^\]]*)\]\(([https]?:?\/?\/?[^\)]*[^\)])\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^)]*)\]\((https?:\/\/[^)]*\)?)\)", text)
