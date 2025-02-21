import re
from enum import Enum
from typing import Callable

from htmlnode import LeafNode, HTMLNode, ParentNode
from inline import (
    DELIMITER_TO_TEXT_TYPE_MAP,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5


BLOCK_TYPE_TO_REGEX_PATTERN_MAP = {
    BlockType.HEADING: r"^(#{1,6})\s+(.+)$",
    BlockType.CODE: r"^```(?:\s*\w+)?\n([\s\S]*?)\n```$",
    BlockType.QUOTE: r"^(>\s?.+(\n>.*)*)$",
    BlockType.UNORDERED_LIST: r"^([\*\-])\s+(.+)$",
    BlockType.ORDERED_LIST: r"^(1\.)\s+(.+)(\n\d+\.\s+.+)*$",
}


def text_node_to_leaf_node(node: TextNode) -> LeafNode:
    match node.text_type:
        case TextType.NORMAL:
            return LeafNode(node.text)
        case TextType.BOLD:
            return LeafNode(node.text, "b")
        case TextType.ITALIC:
            return LeafNode(node.text, "i")
        case TextType.CODE:
            return LeafNode(node.text, "code")
        case TextType.LINK:
            return LeafNode(node.text, "a", {"href": node.url})
        case TextType.IMAGE:
            return LeafNode("", "img", {"src": node.url, "alt": node.text})


def validate_text(text: str) -> Callable:
    def set_error_message(message: str):
        if text == "":
            raise ValueError(message)

    return set_error_message


def validate_inline_text(text: str) -> None:
    validate_text(text)("Inline text can't be empty")


def validate_block_text(text: str) -> None:
    validate_text(text)("Block text can't be empty")


def validate_markdown_text(text: str) -> None:
    validate_text(text)("Markdown text can't be empty")


def inline_text_to_text_nodes(text: str) -> list[TextNode]:
    validate_block_text(text)
    nodes = [TextNode(text, TextType.NORMAL)]
    for delimiter, text_type in DELIMITER_TO_TEXT_TYPE_MAP.items():
        nodes = split_nodes_delimiter(nodes, text_type, delimiter)
    for split in [split_nodes_image, split_nodes_link]:
        nodes = split(nodes)
    return nodes


def block_text_to_block_type(text: str) -> BlockType:
    validate_block_text(text)
    for block_type, pattern in BLOCK_TYPE_TO_REGEX_PATTERN_MAP.items():
        if re.match(pattern, text, re.MULTILINE):
            return block_type
    return BlockType.PARAGRAPH


def markdown_text_to_blocks(text: str) -> list[str]:
    validate_markdown_text(text)
    return [block.strip("\n").strip() for block in text.split("\n\n") if block]


def get_parent_node_from_text_nodes(
    tag: str,
    text_nodes: list[TextNode],
) -> ParentNode:
    children_nodes = []
    for tn in text_nodes:
        children_nodes.append(text_node_to_leaf_node(tn))
    return ParentNode(tag, children_nodes)


def get_heading_node(block: str) -> ParentNode:
    node = None
    for i in range(6, 0, -1):
        hashes = "#" * i
        if block.startswith(hashes):
            text_nodes = inline_text_to_text_nodes(block.lstrip(hashes + " "))
            node = get_parent_node_from_text_nodes(f"h{i}", text_nodes)
            break
    if not node:
        raise TypeError("Expected heading node to be a ParentNode")
    return node


def get_paragraph_node(block: str) -> ParentNode:
    text_nodes = inline_text_to_text_nodes(block)
    return get_parent_node_from_text_nodes("p", text_nodes)


def get_code_node(block: str) -> ParentNode:
    lines = "\n".join(block.split("\n")[1:-1])
    text_node = LeafNode(lines, "code")
    return ParentNode("pre", [text_node])


def get_quote_node(block: str) -> ParentNode:
    text_nodes = inline_text_to_text_nodes(block.lstrip("> "))
    return get_parent_node_from_text_nodes("blockquote", text_nodes)


def get_unordered_node(block: str) -> ParentNode:
    children_nodes = []
    for ln in block.split("\n"):
        text_nodes = inline_text_to_text_nodes(ln.lstrip("* ").lstrip("- "))
        list_node = get_parent_node_from_text_nodes("li", text_nodes)
        children_nodes.append(list_node)
    return ParentNode("ul", children_nodes)


def get_ordered_node(block: str) -> ParentNode:
    children_nodes = []
    for i, ln in enumerate(block.split("\n"), start=1):
        text_nodes = inline_text_to_text_nodes(ln.lstrip(f"{i}. "))
        list_node = get_parent_node_from_text_nodes("li", text_nodes)
        children_nodes.append(list_node)
    return ParentNode("ol", children_nodes)


def markdown_text_to_html_node(text: str) -> HTMLNode:
    nodes = []
    validate_markdown_text(text)
    blocks = markdown_text_to_blocks(text)
    for b in blocks:
        b_type = block_text_to_block_type(b)
        match b_type:
            case BlockType.HEADING:
                nodes.append(get_heading_node(b))
            case BlockType.PARAGRAPH:
                nodes.append(get_paragraph_node(b))
            case BlockType.CODE:
                nodes.append(get_code_node(b))
            case BlockType.QUOTE:
                nodes.append(get_quote_node(b))
            case BlockType.UNORDERED_LIST:
                nodes.append(get_unordered_node(b))
            case BlockType.ORDERED_LIST:
                nodes.append(get_ordered_node(b))

    return ParentNode("div", nodes)
