import unittest

from inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimeter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimeter(unittest.TestCase):
    def test_normal_text(self):
        old_nodes = [TextNode("This is a normal text", TextType.NORMAL)]
        want = old_nodes
        got = split_nodes_delimeter(old_nodes, TextType.NORMAL)
        self.assertListEqual(want, got)

    def test_bold_text(self):
        old_nodes = [TextNode("This is a **bold** text", TextType.NORMAL)]
        want = [
            TextNode("This is a ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ]
        got = split_nodes_delimeter(old_nodes, TextType.BOLD, "**")
        self.assertListEqual(want, got)

    def test_italic_text(self):
        for delimeter in ["*", "_"]:
            old_nodes = [
                TextNode(
                    f"This is an {delimeter}italic{delimeter} text",
                    TextType.NORMAL,
                )
            ]
            want = [
                TextNode("This is an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.NORMAL),
            ]
            got = split_nodes_delimeter(old_nodes, TextType.ITALIC, delimeter)
            self.assertListEqual(want, got)

    def test_code_text(self):
        old_nodes = [TextNode("This is a `code` text", TextType.NORMAL)]
        want = [
            TextNode("This is a ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.NORMAL),
        ]
        got = split_nodes_delimeter(old_nodes, TextType.CODE, "`")
        self.assertListEqual(want, got)

    def test_mixed_text(self):
        old_nodes = [
            TextNode(
                "This is a text, and **bold**, and *italic*, and _italic_, and `code`",
                TextType.NORMAL,
            )
        ]
        want = [
            TextNode("This is a text, and ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(", and ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(", and ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(", and ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
        ]
        bold_nodes = split_nodes_delimeter(old_nodes, TextType.BOLD, "**")
        italic_nodes_1 = split_nodes_delimeter(bold_nodes, TextType.ITALIC, "*")
        italic_nodes_2 = split_nodes_delimeter(italic_nodes_1, TextType.ITALIC, "_")
        code_nodes = split_nodes_delimeter(italic_nodes_2, TextType.CODE, "`")
        got = code_nodes
        self.assertListEqual(want, got)

    def test_invalid_text_type(self):
        old_nodes = [TextNode("This is a normal text", TextType.NORMAL)]
        with self.assertRaises(ValueError):
            split_nodes_delimeter(old_nodes, TextType.LINK)

    def test_invalid_delimeter(self):
        old_nodes = [TextNode("This is a **bold** text", TextType.BOLD)]
        with self.assertRaises(ValueError):
            split_nodes_delimeter(old_nodes, TextType.BOLD, "invalid")

    def test_delimeter_not_match_text_type(self):
        old_nodes = [TextNode("This is a **bold** text", TextType.BOLD)]
        with self.assertRaises(ValueError):
            split_nodes_delimeter(old_nodes, TextType.ITALIC, "code")


class TestExtractLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        want = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        got = extract_markdown_images(text)
        self.assertListEqual(want, got)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to my github](https://github.com/alnah) and [to the repo](https://github.com/alnah/py-http-static-gen)"
        want = [
            ("to my github", "https://github.com/alnah"),
            ("to the repo", "https://github.com/alnah/py-http-static-gen"),
        ]
        got = extract_markdown_links(text)
        self.assertListEqual(want, got)


class TestSplitNodesLink(unittest.TestCase):
    def test_text_with_many_links(self):
        text_node = TextNode(
            text="This is text with a link [to my github](https://github.com/alnah) and [to my repo](https://github.com/alnah/py-http-static-gen)",
            text_type=TextType.NORMAL,
        )
        want = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to my github", TextType.LINK, "https://github.com/alnah"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to my repo",
                TextType.LINK,
                "https://github.com/alnah/py-http-static-gen",
            ),
        ]
        got = split_nodes_link([text_node])
        self.assertListEqual(want, got)

    def test_text_with_many_types_and_links(self):
        text_node = TextNode(
            text="This is a text, and **bold** with a link [to my github](https://github.com/alnah) and [to my repo](https://github.com/alnah/py-http-static-gen)",
            text_type=TextType.NORMAL,
        )
        want = [
            TextNode("This is a text, and ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" with a link ", TextType.NORMAL),
            TextNode("to my github", TextType.LINK, "https://github.com/alnah"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to my repo",
                TextType.LINK,
                "https://github.com/alnah/py-http-static-gen",
            ),
        ]
        with_bold = split_nodes_delimeter([text_node], TextType.BOLD, "**")
        got = split_nodes_link(with_bold)
        self.assertListEqual(want, got)

    def test_text_without_link(self):
        text_node = TextNode(
            text="This is a text without a link",
            text_type=TextType.NORMAL,
        )
        want = [text_node]
        got = split_nodes_link([text_node])
        self.assertListEqual(want, got)

    def test_text_only_with_links(self):
        text_node = TextNode(
            text="[to my github](https://github.com/alnah)[to my repo](https://github.com/alnah/py-http-static-gen)",
            text_type=TextType.NORMAL,
        )
        want = [
            TextNode("to my github", TextType.LINK, "https://github.com/alnah"),
            TextNode(
                "to my repo",
                TextType.LINK,
                "https://github.com/alnah/py-http-static-gen",
            ),
        ]
        got = split_nodes_link([text_node])
        self.assertListEqual(want, got)


class TestSplitNodesImage(unittest.TestCase):
    def test_text_with_many_images(self):
        text_node = TextNode(
            text="This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            text_type=TextType.NORMAL,
        )
        want = [
            TextNode("This is text with an image ", TextType.NORMAL),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        got = split_nodes_image([text_node])
        self.assertListEqual(want, got)

    def test_text_with_many_types_and_images(self):
        text_node = TextNode(
            text="This is a text, and **bold** with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            text_type=TextType.NORMAL,
        )
        want = [
            TextNode("This is a text, and ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" with an image ", TextType.NORMAL),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        with_bold = split_nodes_delimeter([text_node], TextType.BOLD, "**")
        got = split_nodes_image(with_bold)
        self.assertListEqual(want, got)

    def test_text_without_image(self):
        text_node = TextNode(
            text="This is a text without an image",
            text_type=TextType.NORMAL,
        )
        want = [text_node]
        got = split_nodes_image([text_node])
        self.assertListEqual(want, got)

    def test_text_only_with_images(self):
        text_node = TextNode(
            text="![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            text_type=TextType.NORMAL,
        )
        want = [
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        got = split_nodes_image([text_node])
        self.assertListEqual(want, got)


if __name__ == "__main__":
    unittest.main()
