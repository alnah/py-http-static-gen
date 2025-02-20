import re
from enum import Enum

from htmlnode import LeafNode
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


def text_node_to_html_node(node: TextNode) -> LeafNode:
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


def inline_text_to_text_nodes(text: str) -> list[TextNode]:
    if text == "":
        raise ValueError("Inline text can't be empty")

    nodes = [TextNode(text, TextType.NORMAL)]
    for delimiter, text_type in DELIMITER_TO_TEXT_TYPE_MAP.items():
        nodes = split_nodes_delimiter(nodes, text_type, delimiter)
    for split in [split_nodes_image, split_nodes_link]:
        nodes = split(nodes)
    return nodes


def block_text_to_block_type(text: str) -> BlockType:
    if text == "":
        raise ValueError("Block text can't be empty")

    for block_type, pattern in BLOCK_TYPE_TO_REGEX_PATTERN_MAP.items():
        if re.match(pattern, text, re.MULTILINE):
            return block_type
    return BlockType.PARAGRAPH


def markdown_text_to_blocks(text: str) -> list[str]:
    if text == "":
        raise ValueError("Markdown text can't be empty")
    return [b.strip("\n").strip() for b in text.split("\n\n") if b]
