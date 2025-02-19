import unittest

from htmlnode import LeafNode
from nodeconv import text_to_leaf_node, text_to_text_nodes
from textnode import TextNode, TextType


class TestTextToLeafNode(unittest.TestCase):
    def test_normal_text_type(self):
        want = LeafNode(value="normal")
        got = text_to_leaf_node(TextNode(text="normal", text_type=TextType.NORMAL))
        self.assertEqual(want, got)

    def test_bold_text_type(self):
        want = LeafNode(value="bold", tag="b")
        got = text_to_leaf_node(TextNode(text="bold", text_type=TextType.BOLD))
        self.assertEqual(want, got)

    def test_italic_text_type(self):
        want = LeafNode(value="italic", tag="i")
        got = text_to_leaf_node(TextNode(text="italic", text_type=TextType.ITALIC))
        self.assertEqual(want, got)

    def test_code_text_type(self):
        want = LeafNode(value="code", tag="code")
        got = text_to_leaf_node(TextNode(text="code", text_type=TextType.CODE))
        self.assertEqual(want, got)

    def test_link_text_type(self):
        want = LeafNode(
            value="link",
            tag="a",
            props={"href": "https://github.com/alnah/py-http-static-gen"},
        )
        got = text_to_leaf_node(
            TextNode(
                text="link",
                text_type=TextType.LINK,
                url="https://github.com/alnah/py-http-static-gen",
            )
        )
        self.assertEqual(want, got)

    def test_image_text_type(self):
        want = LeafNode(
            value="",
            tag="img",
            props={
                "src": "https://github.com/alnah/py-http-static-gen",
                "alt": "image",
            },
        )
        got = text_to_leaf_node(
            TextNode(
                text="image",
                text_type=TextType.IMAGE,
                url="https://github.com/alnah/py-http-static-gen",
            )
        )
        self.assertEqual(want, got)


class TestTextToTextNodes(unittest.TestCase):
    def test_with_no_text(self):
        text = ""
        with self.assertRaises(ValueError):
            text_to_text_nodes(text)

    def test_with_text_only(self):
        text = "This is a normal text"
        want = [TextNode("This is a normal text", TextType.NORMAL)]
        got = text_to_text_nodes(text)
        self.assertEqual(want, got)

    def test_with_all_types(self):
        text = "This is a normal text, and **bold** text, and *italic* text, and _italic_ text, and `code block`, and ![obi wan image](https://https://i.imgur.com/fJRm4Vk.jpeg), and [link](https://github.com/alnah)"
        want = [
            TextNode("This is a normal text, and ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text, and ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text, and ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text, and ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(", and ", TextType.NORMAL),
            TextNode(
                "obi wan image",
                TextType.IMAGE,
                "https://https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            TextNode(", and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://github.com/alnah"),
        ]
        got = text_to_text_nodes(text)
        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
