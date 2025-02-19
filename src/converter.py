import re
from enum import Enum

from htmlnode import LeafNode
from inline import (
    get_delimiter_to_text_type,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


def text_to_leaf_node(node: TextNode) -> LeafNode:
    match node.text_type:
        case TextType.NORMAL:
            return LeafNode(value=node.text)
        case TextType.BOLD:
            return LeafNode(value=node.text, tag="b")
        case TextType.ITALIC:
            return LeafNode(value=node.text, tag="i")
        case TextType.CODE:
            return LeafNode(value=node.text, tag="code")
        case TextType.LINK:
            return LeafNode(
                value=node.text,
                tag="a",
                props={"href": node.url},
            )
        case TextType.IMAGE:
            return LeafNode(
                value="",
                tag="img",
                props={
                    "src": node.url,
                    "alt": node.text,
                },
            )


def text_to_text_nodes(text: str) -> list[TextNode]:
    if text == "":
        raise ValueError("Text can't be empty")
    nodes = [TextNode(text, TextType.NORMAL)]
    for delimiter, text_type in get_delimiter_to_text_type().items():
        nodes = split_nodes_delimiter(nodes, text_type, delimiter)
    for split in [split_nodes_image, split_nodes_link]:
        nodes = split(nodes)
    return nodes


def markdown_to_blocks(text: str) -> list[str]:
    if text == "":
        raise ValueError("Text can't be empty")
    blocks = text.split("\n\n")
    fmt_blocks = []
    for b in blocks:
        if not b:
            continue
        else:
            fmt_blocks.append(b.strip("\n").strip(" "))
    return fmt_blocks


class BlockType(Enum):
    PARAGRAPH = 0
    HEADING = 1
    CODE = 2
    QUOTE = 3
    UNORDERED_LIST = 4
    ORDERED_LIST = 5


def block_to_block_type(text: str) -> BlockType:
    if text == "":
        raise ValueError("Text can't be empty")
    block_type_to_pattern_map = {
        BlockType.HEADING: r"^(#{1,6})\s+(.+)$",
        BlockType.CODE: r"^```(?:\s*\w+)?\n([\s\S]*?)\n```$",
        BlockType.QUOTE: r"^(>\s?.+(\n>.*)*)$",
        BlockType.UNORDERED_LIST: r"^([\*\-])\s+(.+)$",
        BlockType.ORDERED_LIST: r"^(1\.)\s+(.+)(\n\d+\.\s+.+)*$",
    }
    for block_type, pattern in block_type_to_pattern_map.items():
        if re.match(pattern, text, re.MULTILINE):
            return block_type
    return BlockType.PARAGRAPH
