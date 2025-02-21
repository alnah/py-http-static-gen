import re
from enum import Enum
from typing import Callable

from htmlnode import HTMLNode, LeafNode, ParentNode
from inline import (
    DELIMITER_TO_TEXT_TYPE_MAP,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class BlockType(Enum):
    """Enum representing markdown block types."""

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
    """Convert a TextNode to an HTML LeafNode."""
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
    """Return a validator that raises error if text is empty."""

    def set_error_message(message: str):
        if text == "":
            raise ValueError(message)

    return set_error_message


def validate_inline_text(text: str) -> None:
    """Ensure inline text is not empty."""
    validate_text(text)("Inline text can't be empty")


def validate_block_text(text: str) -> None:
    """Ensure block text is not empty."""
    validate_text(text)("Block text can't be empty")


def validate_markdown_text(text: str) -> None:
    """Ensure markdown text is not empty."""
    validate_text(text)("Markdown text can't be empty")


def inline_text_to_text_nodes(text: str) -> list[TextNode]:
    """Convert inline markdown text into a list of TextNodes."""
    validate_block_text(text)
    nodes = [TextNode(text, TextType.NORMAL)]
    for split in [split_nodes_image, split_nodes_link]:
        nodes = split(nodes)
    for delimiter, text_type in DELIMITER_TO_TEXT_TYPE_MAP.items():
        nodes = split_nodes_delimiter(nodes, text_type, delimiter)
    return nodes


def block_text_to_block_type(text: str) -> BlockType:
    """Identify markdown block type using regex patterns."""
    validate_block_text(text)
    for block_type, pattern in BLOCK_TYPE_TO_REGEX_PATTERN_MAP.items():
        if re.match(pattern, text, re.MULTILINE):
            return block_type
    return BlockType.PARAGRAPH


def markdown_text_to_blocks(text: str) -> list[str]:
    """Split markdown text into block segments."""
    validate_markdown_text(text)
    blocks, current_block, inside = [], [], False
    current_block = []

    for line in text.split("\n"):
        if line.startswith("```"):
            current_block.append(line)
            inside = not inside
        elif line.strip() == "" and not inside:
            if current_block:
                blocks.append("\n".join(current_block).strip())
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block).strip())
    return blocks


def wrap_into_parent_node(
    tag: str,
    text_nodes: list[TextNode],
) -> ParentNode:
    """Wrap TextNodes in a ParentNode with the given tag."""
    children_nodes = []
    for tn in text_nodes:
        children_nodes.append(text_node_to_leaf_node(tn))
    return ParentNode(tag, children_nodes)


def heading_block_to_html_node(block: str) -> ParentNode:
    """Convert a markdown heading block to an HTML heading node."""
    node = None
    for i in range(6, 0, -1):
        hashes = "#" * i
        if block.startswith(hashes):
            text_nodes = inline_text_to_text_nodes(block.lstrip(hashes + " "))
            node = wrap_into_parent_node(f"h{i}", text_nodes)
            break
    if not node:
        raise TypeError("Expected heading node to be a ParentNode")
    return node


def paragraph_block_to_html_node(block: str) -> ParentNode:
    """Convert a markdown paragraph block to an HTML paragraph node."""
    text_nodes = inline_text_to_text_nodes(block)
    return wrap_into_parent_node("p", text_nodes)


def code_block_to_html_node(block: str) -> ParentNode:
    """Convert a markdown code block to an HTML code element."""
    lines = "\n".join(block.split("\n")[1:-1])
    text_node = LeafNode(lines, "code")
    return ParentNode("pre", [text_node])


def quote_block_to_html_node(block: str) -> ParentNode:
    """Convert a markdown quote block to an HTML blockquote node."""
    text_nodes = inline_text_to_text_nodes(block.lstrip("> "))
    return wrap_into_parent_node("blockquote", text_nodes)


def unordered_block_to_html_node(block: str) -> ParentNode:
    """Convert markdown unordered list to an HTML ul with li items."""
    children_nodes = []
    for ln in block.split("\n"):
        text_nodes = inline_text_to_text_nodes(ln.lstrip("* ").lstrip("- "))
        list_node = wrap_into_parent_node("li", text_nodes)
        children_nodes.append(list_node)
    return ParentNode("ul", children_nodes)


def ordered_block_to_html_node(block: str) -> ParentNode:
    """Convert markdown ordered list to an HTML ol with li items."""
    children_nodes = []
    for i, ln in enumerate(block.split("\n"), start=1):
        text_nodes = inline_text_to_text_nodes(ln.lstrip(f"{i}. "))
        list_node = wrap_into_parent_node("li", text_nodes)
        children_nodes.append(list_node)
    return ParentNode("ol", children_nodes)


def markdown_text_to_html_node(text: str) -> HTMLNode:
    """Convert markdown text to an HTMLNode tree."""
    nodes = []
    validate_markdown_text(text)
    blocks = markdown_text_to_blocks(text)
    for b in blocks:
        b_type = block_text_to_block_type(b)
        match b_type:
            case BlockType.HEADING:
                nodes.append(heading_block_to_html_node(b))
            case BlockType.PARAGRAPH:
                nodes.append(paragraph_block_to_html_node(b))
            case BlockType.CODE:
                nodes.append(code_block_to_html_node(b))
            case BlockType.QUOTE:
                nodes.append(quote_block_to_html_node(b))
            case BlockType.UNORDERED_LIST:
                nodes.append(unordered_block_to_html_node(b))
            case BlockType.ORDERED_LIST:
                nodes.append(ordered_block_to_html_node(b))

    return ParentNode("div", nodes)
