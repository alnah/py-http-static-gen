from htmlnode import LeafNode
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
