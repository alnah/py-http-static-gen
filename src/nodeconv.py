from htmlnode import LeafNode
from inline import (
    get_delimeter_to_text_type,
    split_nodes_delimeter,
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
    for delimeter, text_type in get_delimeter_to_text_type().items():
        nodes = split_nodes_delimeter(nodes, text_type, delimeter)
    for split in [split_nodes_image, split_nodes_link]:
        nodes = split(nodes)
    return nodes
