import re
from typing import Callable, Optional

from textnode import TextNode, TextType

DELIMITER_TO_TEXT_TYPE_MAP = {
    "": TextType.NORMAL,
    "**": TextType.BOLD,
    "*": TextType.ITALIC,
    "_": TextType.ITALIC,
    "`": TextType.CODE,
}


def validate_text_type(text_type: TextType) -> None:
    valid_text_types = set(DELIMITER_TO_TEXT_TYPE_MAP.values())
    if text_type not in valid_text_types:
        raise ValueError(f"TextType must be one of {valid_text_types} not {text_type}")


def validate_delimiter(delimiter: str) -> None:
    valid_delimiters = set(DELIMITER_TO_TEXT_TYPE_MAP.keys())
    if delimiter not in valid_delimiters:
        raise ValueError(f"Delimiter must be one of {valid_delimiters} not {delimiter}")


def validate_delimiter_match_text_type(delimiter: str, text_type: TextType) -> None:
    want_text_type = DELIMITER_TO_TEXT_TYPE_MAP[delimiter]
    if want_text_type != text_type:
        raise ValueError(f"TextType {text_type!r} doesn't match {delimiter}")


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    text_type: TextType,
    delimiter: Optional[str] = None,
) -> list[TextNode]:
    delimiter = delimiter if delimiter else ""

    validate_text_type(text_type)
    validate_delimiter(delimiter)
    validate_delimiter_match_text_type(delimiter, text_type)

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


def get_separator(text_type: TextType, text_ref: str, ref: str) -> str:
    base_separator = f"[{text_ref}]({ref})"
    return "!" + base_separator if text_type == TextType.IMAGE else base_separator


def validate_image_or_link_text_type(text_type: TextType) -> None:
    valid_text_types = {TextType.IMAGE, TextType.LINK}
    if text_type not in valid_text_types:
        raise ValueError(f"TextType must be one of {valid_text_types} not {text_type}")


def validate_extractor(extractor: Callable) -> None:
    valid_extractors = {extract_markdown_images, extract_markdown_links}
    if extractor not in valid_extractors:
        raise ValueError(f"Extractor must be one of {valid_extractors} not {extractor}")


def split_nodes_reference(
    old_nodes: list[TextNode],
    extractor: Callable[[str], list[tuple[str, str]]],
    new_text_type: TextType,
) -> list[TextNode]:
    validate_image_or_link_text_type(new_text_type)
    validate_extractor(extractor)

    new_nodes = []
    for old_node in old_nodes:
        _text_type, text = old_node.text_type, old_node.text
        matches = extractor(text)
        if not matches:
            new_nodes.append(TextNode(text, _text_type, old_node.url))
            continue
        for text_ref, ref in matches:
            separator = get_separator(new_text_type, text_ref, ref)
            parts = text.split(separator, 1)
            outside, inside = parts[0], parts[1]
            if outside:
                new_nodes.append(TextNode(outside, _text_type, old_node.url))
            new_nodes.append(TextNode(text_ref, new_text_type, ref))
            text = inside if len(parts) > 1 else ""
        if text:
            new_nodes.append(TextNode(text, _text_type, old_node.url))
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_reference(old_nodes, extract_markdown_images, TextType.IMAGE)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_reference(old_nodes, extract_markdown_links, TextType.LINK)
