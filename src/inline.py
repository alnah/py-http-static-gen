import re
from typing import Optional, Callable

from textnode import TextNode, TextType


def get_delimeter_to_text_type() -> dict[str, TextType]:
    return {
        "": TextType.NORMAL,
        "**": TextType.BOLD,
        "*": TextType.ITALIC,
        "_": TextType.ITALIC,
        "`": TextType.CODE,
    }


def split_nodes_delimeter(
    old_nodes: list[TextNode],
    text_type: TextType,
    delimiter: Optional[str] = None,
) -> list[TextNode]:
    delimiter = delimiter if delimiter else ""
    valid_map = get_delimeter_to_text_type()
    if text_type not in valid_map.values():
        raise ValueError(
            f"TextType must be one of {set(valid_map.values())}, got: '{text_type}'"
        )
    if delimiter not in valid_map:
        raise ValueError(
            f"Delimiter must be one of {set(valid_map.keys())}, got: '{delimiter}'"
        )
    want_type = valid_map[delimiter]
    if want_type != text_type:
        raise ValueError(
            f"TextType {text_type!r} doesn't match delimiter {delimiter!r}"
        )
    if not delimiter:
        return old_nodes
    new_nodes = []
    for old_node in old_nodes:
        text = old_node.text
        if delimiter not in text:
            new_nodes.append(old_node)
            continue
        sections = text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid Markdown, unclosed delimiter '{delimiter}'")
        for i, section in enumerate(sections):
            if not section:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(section, old_node.text_type))
            else:
                new_nodes.append(TextNode(section, text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return __split_nodes_helper(old_nodes, extract_markdown_images, TextType.IMAGE)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return __split_nodes_helper(old_nodes, extract_markdown_links, TextType.LINK)


def __split_nodes_helper(
    old_nodes: list[TextNode],
    extract_func: Callable[[str], list[tuple[str, str]]],
    new_text_type: TextType,
) -> list[TextNode]:
    if new_text_type not in (TextType.IMAGE, TextType.LINK):
        raise ValueError("TextType must be: IMAGE, or LINK")
    if extract_func not in (extract_markdown_images, extract_markdown_links):
        raise ValueError(
            "Extract func must be: extract_markdown_images, or extract_markdown_links"
        )
    new_nodes = []
    for old_node in old_nodes:
        old_type = old_node.text_type
        text = old_node.text
        matches = extract_func(text)
        if not matches:
            new_nodes.append(TextNode(text, old_type, old_node.url))
            continue
        for text_helper, elem in matches:
            sep = f"[{text_helper}]({elem})"
            if new_text_type == TextType.IMAGE:
                sep = "!" + sep
            parts = text.split(sep, 1)
            outside = parts[0]
            if outside:
                new_nodes.append(TextNode(outside, old_type, old_node.url))
            new_nodes.append(TextNode(text_helper, new_text_type, elem))
            text = parts[1] if len(parts) > 1 else ""
        if text:
            new_nodes.append(TextNode(text, old_type, old_node.url))
    return new_nodes
