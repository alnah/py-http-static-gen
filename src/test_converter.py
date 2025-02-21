import unittest

from converter import (
    BlockType,
    block_text_to_block_type,
    inline_text_to_text_nodes,
    markdown_text_to_blocks,
    markdown_text_to_html_node,
    text_node_to_leaf_node,
)
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType


class TestTextNodeToLeafNode(unittest.TestCase):
    def test_normal_text_type(self):
        want = LeafNode(value="normal")
        got = text_node_to_leaf_node(TextNode(text="normal", text_type=TextType.NORMAL))
        self.assertEqual(want, got)

    def test_bold_text_type(self):
        want = LeafNode(value="bold", tag="b")
        got = text_node_to_leaf_node(TextNode(text="bold", text_type=TextType.BOLD))
        self.assertEqual(want, got)

    def test_italic_text_type(self):
        want = LeafNode(value="italic", tag="i")
        got = text_node_to_leaf_node(TextNode(text="italic", text_type=TextType.ITALIC))
        self.assertEqual(want, got)

    def test_code_text_type(self):
        want = LeafNode(value="code", tag="code")
        got = text_node_to_leaf_node(TextNode(text="code", text_type=TextType.CODE))
        self.assertEqual(want, got)

    def test_link_text_type(self):
        want = LeafNode(
            value="link",
            tag="a",
            props={"href": "https://test.com/test"},
        )
        got = text_node_to_leaf_node(
            TextNode(
                text="link",
                text_type=TextType.LINK,
                url="https://test.com/test",
            )
        )
        self.assertEqual(want, got)

    def test_image_text_type(self):
        want = LeafNode(
            value="",
            tag="img",
            props={
                "src": "https://test.com/test",
                "alt": "image",
            },
        )
        got = text_node_to_leaf_node(
            TextNode(
                text="image",
                text_type=TextType.IMAGE,
                url="https://test.com/test",
            )
        )
        self.assertEqual(want, got)


class TestInlineTextToTextNodes(unittest.TestCase):
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
        text = "This is a normal text, and **bold** text, and *italic* text, \
and _italic_ text, and `code block`, and ![image](https://image.jpeg), \
and [link](https://test.com)"
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
                "image",
                TextType.IMAGE,
                "https://image.jpeg",
            ),
            TextNode(", and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://test.com"),
        ]
        got = inline_text_to_text_nodes(text)
        self.assertListEqual(want, got)


class TestMarkdownTextToBlocks(unittest.TestCase):
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
            "This is a paragraph of text. \
It has some **bold** and *italic* words inside of it.",
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
            "This is a paragraph of text. \
It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
   * This is a list item
   * This is another list item""",
        ]
        got = markdown_text_to_blocks(text)
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
            "This is a paragraph of text. \
It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item""",
        ]
        got = markdown_text_to_blocks(text)
        self.assertListEqual(want, got)

    def test_fence_marker(self):
        text = """# This is a heading
This is a paragraph of text.
```python
print("Hello, World!")
```"""
        want = [
            "# This is a heading\n"
            "This is a paragraph of text.\n"
            "```python\n"
            'print("Hello, World!")\n'
            "```"
        ]
        got = markdown_text_to_blocks(text)
        self.assertListEqual(want, got)


class TestBlockTextToBlockType(unittest.TestCase):
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
        text2 = """- unordered list
- unordered list
- unordered list"""
        for t in [text1, text2]:
            self.assertEqual(block_text_to_block_type(t), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        text = """1. ordered list
2. ordered list
3. ordered list"""
        self.assertEqual(block_text_to_block_type(text), BlockType.ORDERED_LIST)


class TestMarkdownTextToHTMLNode(unittest.TestCase):
    def want(self, tag: str, type: str) -> ParentNode:
        if type in ["unordered_list", "ordered_list"]:
            return ParentNode(
                tag,
                [
                    ParentNode(
                        "li",
                        [
                            LeafNode("This is a normal text"),
                        ],
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode("This is a "),
                            LeafNode("bold", "b"),
                            LeafNode(" text"),
                        ],
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode("This is an "),
                            LeafNode("italic", "i"),
                            LeafNode(" text"),
                        ],
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode("This is an "),
                            LeafNode("italic", "i"),
                            LeafNode(" text"),
                        ],
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode("This is a "),
                            LeafNode("code", "code"),
                            LeafNode(" text"),
                        ],
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode("This is an "),
                            LeafNode(
                                "",
                                "img",
                                {"src": "https://image.com", "alt": "image"},
                            ),
                        ],
                    ),
                    ParentNode(
                        "li",
                        [
                            LeafNode("This is a "),
                            LeafNode("link", "a", {"href": "https://link.com"}),
                        ],
                    ),
                ],
            )
        elif type == "code":
            return ParentNode(
                tag,
                [LeafNode('print("Hello, World!")', type)],
            )
        else:
            return ParentNode(
                tag,
                [
                    LeafNode(f"This is a {type}, and "),
                    LeafNode("bold", "b"),
                    LeafNode(", and "),
                    LeafNode("italic", "i"),
                    LeafNode(", and "),
                    LeafNode("italic", "i"),
                    LeafNode(", and "),
                    LeafNode("code", "code"),
                    LeafNode(", and "),
                    LeafNode(
                        "",
                        "img",
                        {"src": "https://image.com", "alt": "image"},
                    ),
                    LeafNode(", and "),
                    LeafNode("link", "a", {"href": "https://link.com"}),
                ],
            )

    def test_empty_text(self):
        text = ""
        with self.assertRaises(ValueError):
            markdown_text_to_html_node(text)

    def test_h1(self):
        text = (
            "# This is a heading, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)"
        )
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", [self.want("h1", "heading")]), got)

    def test_h2(self):
        text = "## This is a heading, and **bold**, and *italic*, and _italic_, \
and `code`, and ![image](https://image.com), and [link](https://link.com)"
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", [self.want("h2", "heading")]), got)

    def test_h3(self):
        text = "### This is a heading, and **bold**, and *italic*, and _italic_, \
and `code`, and ![image](https://image.com), and [link](https://link.com)"
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", [self.want("h3", "heading")]), got)

    def test_h4(self):
        text = "#### This is a heading, and **bold**, and *italic*, and _italic_, \
and `code`, and ![image](https://image.com), and [link](https://link.com)"
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", [self.want("h4", "heading")]), got)

    def test_h5(self):
        text = "##### This is a heading, and **bold**, and *italic*, and _italic_, and \
`code`, and ![image](https://image.com), and [link](https://link.com)"
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", [self.want("h5", "heading")]), got)

    def test_h6(self):
        text = (
            "###### This is a heading, and **bold**, and *italic*, and _italic_, and \
`code`, and ![image](https://image.com), and [link](https://link.com)"
        )
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", [self.want("h6", "heading")]), got)

    def test_paragraph(self):
        text = "This is a paragraph, and **bold**, and *italic*, and _italic_, \
and `code`, and ![image](https://image.com), and [link](https://link.com)"
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", [self.want("p", "paragraph")]), got)

    def test_code(self):
        text = """```python
print("Hello, World!")
```"""
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", [self.want("pre", "code")]), got)

    def test_quote(self):
        text = "> This is a quote, and **bold**, and *italic*, and _italic_, \
and `code`, and ![image](https://image.com), and [link](https://link.com)"
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", [self.want("blockquote", "quote")]), got)

    def test_unordered_list_asterisk(self):
        text = """* This is a normal text
* This is a **bold** text
* This is an *italic* text
* This is an _italic_ text
* This is a `code` text
* This is an ![image](https://image.com)
* This is a [link](https://link.com)"""
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", [self.want("ul", "unordered_list")]), got)

    def test_unordered_list_hyphen(self):
        text = """- This is a normal text
- This is a **bold** text
- This is an *italic* text
- This is an _italic_ text
- This is a `code` text
- This is an ![image](https://image.com)
- This is a [link](https://link.com)"""
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", [self.want("ul", "unordered_list")]), got)

    def test_ordered_list(self):
        text = """1. This is a normal text
2. This is a **bold** text
3. This is an *italic* text
4. This is an _italic_ text
5. This is a `code` text
6. This is an ![image](https://image.com)
7. This is a [link](https://link.com)"""
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", [self.want("ol", "ordered_list")]), got)

    def test_all(self):
        text = '# This is a heading, and **bold**, and *italic*, and _italic_, and \
`code`, and ![image](https://image.com), and [link](https://link.com)\n\n\
## This is a heading, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
### This is a heading, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
#### This is a heading, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
##### This is a heading, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
###### This is a heading, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
This is a paragraph, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
```python\nprint("Hello, World!")\n```\n\n\
> This is a quote, and **bold**, and *italic*, and _italic_, and `code`, \
and ![image](https://image.com), and [link](https://link.com)\n\n\
* This is a normal text\n\
* This is a **bold** text\n\
* This is an *italic* text\n\
* This is an _italic_ text\n\
* This is a `code` text\n\
* This is an ![image](https://image.com)\n\
* This is a [link](https://link.com)\n\n\
- This is a normal text\n\
- This is a **bold** text\n\
- This is an *italic* text\n\
- This is an _italic_ text\n\
- This is a `code` text\n\
- This is an ![image](https://image.com)\n\
- This is a [link](https://link.com)\n\n\
1. This is a normal text\n\
2. This is a **bold** text\n\
3. This is an *italic* text\n\
4. This is an _italic_ text\n\
5. This is a `code` text\n\
6. This is an ![image](https://image.com)\n\
7. This is a [link](https://link.com)'
        want = []
        for i in range(1, 7):
            want.append(self.want(f"h{i}", "heading"))
        for e in [
            self.want("p", "paragraph"),
            self.want("pre", "code"),
            self.want("blockquote", "quote"),
            self.want("ul", "unordered_list"),
            self.want("ul", "unordered_list"),
            self.want("ol", "ordered_list"),
        ]:
            want.append(e)
        got = markdown_text_to_html_node(text)
        self.assertEqual(ParentNode("div", want), got)


if __name__ == "__main__":
    unittest.main()
