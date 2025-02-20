import unittest

from converter import (
    BlockType,
    block_text_to_block_type,
    inline_text_to_text_nodes,
    markdown_text_to_blocks,
    text_node_to_html_node,
)
from htmlnode import LeafNode
from textnode import TextNode, TextType


class TestTextToLeafNode(unittest.TestCase):
    def test_normal_text_type(self):
        want = LeafNode(value="normal")
        got = text_node_to_html_node(TextNode(text="normal", text_type=TextType.NORMAL))
        self.assertEqual(want, got)

    def test_bold_text_type(self):
        want = LeafNode(value="bold", tag="b")
        got = text_node_to_html_node(TextNode(text="bold", text_type=TextType.BOLD))
        self.assertEqual(want, got)

    def test_italic_text_type(self):
        want = LeafNode(value="italic", tag="i")
        got = text_node_to_html_node(TextNode(text="italic", text_type=TextType.ITALIC))
        self.assertEqual(want, got)

    def test_code_text_type(self):
        want = LeafNode(value="code", tag="code")
        got = text_node_to_html_node(TextNode(text="code", text_type=TextType.CODE))
        self.assertEqual(want, got)

    def test_link_text_type(self):
        want = LeafNode(
            value="link",
            tag="a",
            props={"href": "https://github.com/alnah/py-http-static-gen"},
        )
        got = text_node_to_html_node(
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
        got = text_node_to_html_node(
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
            inline_text_to_text_nodes(text)

    def test_with_text_only(self):
        text = "This is a normal text"
        want = [TextNode("This is a normal text", TextType.NORMAL)]
        got = inline_text_to_text_nodes(text)
        self.assertListEqual(want, got)

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
        got = inline_text_to_text_nodes(text)
        self.assertListEqual(want, got)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_empty_text(self):
        text = ""
        with self.assertRaises(ValueError):
            markdown_text_to_blocks(text)

    def test_nice_formatted_text(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        want = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item""",
        ]
        got = markdown_text_to_blocks(text)
        self.assertListEqual(want, got)

    def test_remove_block_trailing_whitespaces(self):
        text = """   # This is a heading

   This is a paragraph of text. It has some **bold** and *italic* words inside of it.     

   * This is the first list item in a list block
   * This is a list item
   * This is another list item   """
        want = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
   * This is a list item
   * This is another list item""",
        ]
        got = markdown_text_to_blocks(text)
        self.maxDiff = None
        self.assertListEqual(want, got)

    def test_remove_excessive_newlines(self):
        text = """# This is a heading


This is a paragraph of text. It has some **bold** and *italic* words inside of it.     




* This is the first list item in a list block
* This is a list item
* This is another list item



"""
        want = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item""",
        ]
        got = markdown_text_to_blocks(text)
        self.maxDiff = None
        self.assertListEqual(want, got)


class TestBlockToBlockType(unittest.TestCase):
    def test_empty_text(self):
        text = ""
        with self.assertRaises(ValueError):
            block_text_to_block_type(text)

    def test_paragraph(self):
        text = "This is a paragraph"
        self.assertEqual(block_text_to_block_type(text), BlockType.PARAGRAPH)

    def test_h1(self):
        text = "# Heading 1"
        self.assertEqual(block_text_to_block_type(text), BlockType.HEADING)

    def test_h2(self):
        text = "## Heading 2"
        self.assertEqual(block_text_to_block_type(text), BlockType.HEADING)

    def test_h3(self):
        text = "### Heading 3"
        self.assertEqual(block_text_to_block_type(text), BlockType.HEADING)

    def test_h4(self):
        text = "#### Heading 4"
        self.assertEqual(block_text_to_block_type(text), BlockType.HEADING)

    def test_h5(self):
        text = "##### Heading 5"
        self.assertEqual(block_text_to_block_type(text), BlockType.HEADING)

    def test_h6(self):
        text = "###### Heading 6"
        self.assertEqual(block_text_to_block_type(text), BlockType.HEADING)

    def test_code(self):
        text = """```python
print("Hello, World!")
```"""
        self.assertEqual(block_text_to_block_type(text), BlockType.CODE)

    def test_quote(self):
        text = "> quote"
        self.assertEqual(block_text_to_block_type(text), BlockType.QUOTE)

    def test_unordered_list(self):
        text1 = """* unordered list
* unordered list
* unordered list"""
        text2 = """* unordered list
* unordered list
* unordered list"""
        for t in [text1, text2]:
            self.assertEqual(block_text_to_block_type(t), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        text = """1. ordered list
2. ordered list
3. ordered list"""
        self.assertEqual(block_text_to_block_type(text), BlockType.ORDERED_LIST)


if __name__ == "__main__":
    unittest.main()
