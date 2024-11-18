from textnode import TextNode, TextType
from htmlnode import HTMLnode, LeafNode, ParentNode
from extract import extract_markdown_images, extract_markdown_links


# Calisify strings in textnodes.
def markdown_to_nodes(text: str) -> list[TextNode]:
    node = [TextNode(text, TextType.NORMAL)]

    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "*", TextType.ITALIC)
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    node = split_nodes_images(node)
    node = split_nodes_links(node)
    return node


# Splits a text by paragraphs
def markdown_to_blocks(text: str) -> list[str]:
    split_text = text.split("\n\n")
    for idx, line in enumerate(split_text):
        split_text[idx] = line.strip(" ")
    # Remove empty strings
    return [x for x in split_text if x != ""]


# Classify paragraphs
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
                return "codeblock"
        case ">":
            return "blockquote"
        case "*" | "-":
            return "ul"

    return "p"


def blocktype_to_type(blocktype: str) -> TextType:
    match blocktype:
        case "blockquote":
            return TextType.QUOTES
        case "ul":
            return TextType.UL
        case "ol":
            return TextType.OL
        case "codeblock":
            return TextType.CODEBLOCK
        case "H1":
            return TextType.HEADER1
        case "H2":
            return TextType.HEADER2
        case "H3":
            return TextType.HEADER3
        case "H4":
            return TextType.HEADER4
        case "H5":
            return TextType.HEADER5
        case "H6":
            return TextType.HEADER6
    return TextType.NORMAL


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
        case TextType.QUOTES:
            text = node.text.split("\n")
            for index, line in enumerate(text):
                text[index] = line.strip(" ")[2:]
            return LeafNode("blockquote", LeafNode("p", "\n".join(text)).to_html())
        case TextType.UL | TextType.OL:
            return LeafNode("ul", node.text)
        case TextType.CODEBLOCK:
            text = node.text.split("\n")
            for index, line in enumerate(text):
                text[index] = line.strip(" ")
            last_dance = "\n".join(text)
            return LeafNode("codeblock", last_dance.strip("\n`"))
        case TextType.HEADER1:
            return LeafNode("h1", node.text.strip(" ")[2:])
        case TextType.HEADER2:
            return LeafNode("h2", node.text.strip(" ")[3:])
        case TextType.HEADER3:
            return LeafNode("h3", node.text.strip(" ")[4:])
        case TextType.HEADER4:
            return LeafNode("h4", node.text.strip(" ")[5:])
        case TextType.HEADER5:
            return LeafNode("h5", node.text.strip(" ")[6:])
        case TextType.HEADER6:
            return LeafNode("h6", node.text.strip(" ")[7:])


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


def list_to_html(ul: str) -> str:
    splitted_ul = ul.split("\n")
    formated_ul = map(lambda x: "<li>" + x.strip(" ")[1:] + "</li>", splitted_ul)

    return "\n".join(formated_ul)


def markdown_to_html_node(md_text: str) -> list[TextNode]:
    html_nodes = []
    blocks = markdown_to_blocks(md_text)
    for block in blocks:
        block_type = block_to_block_type(block.strip("\n "))
        match block_type:
            case "p":
                html_nodes.extend(markdown_to_nodes(block))
            case "ul" | "ol":
                html_nodes.extend(
                    [TextNode(list_to_html(block), blocktype_to_type(block_type))]
                )
            case _:
                html_nodes.extend([TextNode(block, blocktype_to_type(block_type))])

    # Textnode to htmlnode
    return html_nodes


def html_nodes_finito(nodes: list[TextNode]) -> str:
    html_template = []
    current_childs = []
    count = 0
    normal_in_a_row = False
    while len(nodes) > count:
        if normal_in_a_row and nodes[count].text_type == TextType.NORMAL:
            previous_parent = ParentNode(
                "p", [text_node_to_html_node(x) for x in current_childs]
            )
            html_template.append(previous_parent.to_html())
            current_childs = []

        if nodes[count].text_type in [
            TextType.NORMAL,
            TextType.BOLD,
            TextType.ITALIC,
            TextType.IMAGES,
            TextType.LINKS,
            TextType.CODE,
        ]:
            if nodes[count].text_type == TextType.NORMAL:
                normal_in_a_row = True
            else:
                normal_in_a_row = False
            current_childs.append(nodes[count])
            count += 1
            continue
        else:
            normal_in_a_row = False
            if current_childs:
                previous_parent = ParentNode(
                    "p", [text_node_to_html_node(x) for x in current_childs]
                )
                html_template.append(previous_parent.to_html().strip(" "))
                current_childs = []
            current_node = text_node_to_html_node(nodes[count])
            html_template.append(current_node.to_html())
            count += 1
    if current_childs:
        previous_parent = ParentNode(
            "p", [text_node_to_html_node(x) for x in current_childs]
        )
        html_template.append(previous_parent.to_html())

    return "<div>" + "\n".join(html_template) + "</div>"
