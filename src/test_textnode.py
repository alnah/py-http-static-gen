import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test__init__optional_url(self):
        text_node = TextNode(
            text="test",
            text_type=TextType.NORMAL,
        )
        self.assertEqual(text_node.url, "")

    def test__eq__eq_node(self):
        text_node = TextNode(
            text="test",
            text_type=TextType.NORMAL,
            url="https://test.com",
        )
        other_text_node = TextNode(
            text="test",
            text_type=TextType.NORMAL,
            url="https://test.com",
        )
        self.assertEqual(text_node, other_text_node)

    def test__eq__not_eq_text(self):
        text_node = TextNode(
            text="test",
            text_type=TextType.NORMAL,
            url="https://test.com",
        )
        other_text_node = TextNode(
            text="diff",
            text_type=TextType.NORMAL,
            url="https://test.com",
        )
        self.assertNotEqual(text_node, other_text_node)

    def test__eq__not_eq_type(self):
        text_node = TextNode(
            text="test",
            text_type=TextType.NORMAL,
            url="https://test.com",
        )
        other_text_node = TextNode(
            text="test",
            text_type=TextType.BOLD,  # diff text type
            url="https://test.com",
        )
        self.assertNotEqual(text_node, other_text_node)

    def test__eq__not_eq_url(self):
        text_node = TextNode(
            text="test",
            text_type=TextType.NORMAL,
            url="https://test.com",
        )
        other_text_node = TextNode(
            text="test",
            text_type=TextType.NORMAL,
            url="https://diff.com",
        )
        self.assertNotEqual(text_node, other_text_node)

    def test__repr__with_url(self):
        text_node = TextNode(
            text="test",
            text_type=TextType.NORMAL,
            url="https://test.com",
        )
        want = "TextNode(text='test', text_type=<TextType.NORMAL: 0>, url='https://test.com')"
        got = repr(text_node)
        self.assertEqual(want, got)

    def test__repr__without_url(self):
        text_node = TextNode(
            text="test",
            text_type=TextType.NORMAL,
        )
        want = "TextNode(text='test', text_type=<TextType.NORMAL: 0>, url='')"
        got = repr(text_node)
        self.assertEqual(want, got)
