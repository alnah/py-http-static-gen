import unittest

from htmlnode import LeafNode
from nodeconv import text_to_leaf_node
from textnode import TextNode, TextType


class TestNodeConv(unittest.TestCase):
    def test_normal_text_type(self):
        want = LeafNode(value="normal")
        got = text_to_leaf_node(TextNode(text="normal", text_type=TextType.NORMAL))
        self.assertEqual(repr(want), repr(got))

    def test_bold_text_type(self):
        want = LeafNode(value="bold", tag="b")
        got = text_to_leaf_node(TextNode(text="bold", text_type=TextType.BOLD))
        self.assertEqual(repr(want), repr(got))

    def test_italic_text_type(self):
        want = LeafNode(value="italic", tag="i")
        got = text_to_leaf_node(TextNode(text="italic", text_type=TextType.ITALIC))
        self.assertEqual(repr(want), repr(got))

    def test_code_text_type(self):
        want = LeafNode(value="code", tag="code")
        got = text_to_leaf_node(TextNode(text="code", text_type=TextType.CODE))
        self.assertEqual(repr(want), repr(got))

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
        self.assertEqual(repr(want), repr(got))

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
        self.assertEqual(repr(want), repr(got))


if __name__ == "__main__":
    unittest.main()
