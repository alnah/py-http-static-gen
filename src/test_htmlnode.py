import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test__init__optional_values(self):
        html_node = HTMLNode()
        self.assertEqual(html_node.tag, "")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {})

    def test__eq__eq_html_node(self):
        html_node1 = HTMLNode(
            tag="div",
            value="test",
            children=[],
            props={"id": "div1"},
        )
        html_node2 = HTMLNode(
            tag="div",
            value="test",
            children=[],
            props={"id": "div1"},
        )
        self.assertEqual(html_node1, html_node2)

    def test__eq__not_eq_tag(self):
        html_node1 = HTMLNode(tag="p", value="test")
        html_node2 = HTMLNode(tag="div", value="test")
        self.assertNotEqual(html_node1, html_node2)

    def test__eq__not_eq_value(self):
        html_node1 = HTMLNode(value="test")
        html_node2 = HTMLNode(value="diff")
        self.assertNotEqual(html_node1, html_node2)

    def test__eq__not_eq_children(self):
        child_html_node = HTMLNode(tag="span")
        html_node1 = HTMLNode(children=[child_html_node])
        html_node2 = HTMLNode(children=[])
        self.assertNotEqual(html_node1, html_node2)

    def test__eq__not_eq_props(self):
        html_node1 = HTMLNode(props={"href": "https://test.com"})
        html_node2 = HTMLNode(props={"src": "test.jpg"})
        self.assertNotEqual(html_node1, html_node2)

    def test__repr__(self):
        html_node = HTMLNode(
            tag="a",
            value="link",
            children=[
                HTMLNode(
                    tag="b",
                    value="bold",
                )
            ],
            props={
                "href": "https://test.com/test",
                "target": "_blank",
            },
        )
        want = "HTMLNode(tag='a', value='link', children=[HTMLNode(tag='b', value='bold', children=[], props={})], props={'href': 'https://test.com/test', 'target': '_blank'})"
        got = repr(html_node)
        self.assertEqual(want, got)

    def test__to_html_placeholder(self):
        html_node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            html_node.to_html()

    def test_props_to_html(self):
        html_node = HTMLNode(
            tag="a",
            value="link",
            props={
                "href": "https://test.com/test",
                "target": "_blank",
            },
        )
        want = ' href="https://test.com/test" target="_blank"'
        got = html_node.props_to_html()
        self.assertEqual(want, got)

    def test_props_to_html_empty_(self):
        html_node = HTMLNode(tag="a", value="link")
        want = ""
        got = html_node.props_to_html()
        self.assertEqual(want, got)


class TestLeafNode(unittest.TestCase):
    def test__init__optional_values(self):
        leaf_node = LeafNode(value="test")
        self.assertEqual(leaf_node.tag, "")
        self.assertEqual(leaf_node.props, {})

    def test__init__ensure_empty_children(self):
        leaf_node = LeafNode(value="test")
        self.assertEqual(leaf_node.children, [])

    def test_to_html_with_tag_and_props(self):
        leaf_node = LeafNode(
            tag="a",
            value="test",
            props={
                "href": "https://test.com/test",
                "target": "_blank",
            },
        )
        want = '<a href="https://test.com/test" target="_blank">test</a>'
        got = leaf_node.to_html()
        self.assertEqual(want, got)

    def test_to_html_with_img_self_enclosing_tag(self):
        leaf_node = LeafNode(
            tag="img",
            value="",
            props={"src": "https://test.com", "alt": "test"},
        )
        want = '<img src="https://test.com" alt="test"/>'
        got = leaf_node.to_html()
        self.assertEqual(want, got)

    def test_to_html_without_tag(self):
        leaf_node = LeafNode(value="test")
        want = "test"
        got = leaf_node.to_html()
        self.assertEqual(want, got)

    def test_to_html_without_props(self):
        leaf_node = LeafNode(tag="p", value="test")
        want = "<p>test</p>"
        got = leaf_node.to_html()
        self.assertEqual(want, got)


class TestParentNode(unittest.TestCase):
    def test__init__optional_values(self):
        parent_node = ParentNode(
            tag="p",
            children=[LeafNode(value="test", tag="b")],
        )
        self.assertEqual(parent_node.props, {})

    def test__init__ensure_empty_value(self):
        parent_node = ParentNode(
            tag="p",
            children=[LeafNode(value="test", tag="b")],
        )
        self.assertEqual(parent_node.value, "")

    def test_to_html_with_children(self):
        parent_node = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="bold"),
                LeafNode(value="normal"),
                LeafNode(tag="i", value="italic"),
                LeafNode(value="normal"),
            ],
            props={"id": "p1"},
        )
        want = '<p id="p1"><b>bold</b>normal<i>italic</i>normal</p>'
        got = parent_node.to_html()
        self.assertEqual(want, got)

    def test_to_html_with_grandchildren(self):
        parent_node = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(tag="b", value="bold"),
                        LeafNode(value="normal"),
                        LeafNode(tag="i", value="italic"),
                        LeafNode(value="normal"),
                    ],
                    props={"id": "p1"},
                ),
            ],
            props={"id": "div1"},
        )

        want = (
            '<div id="div1"><p id="p1"><b>bold</b>normal<i>italic</i>normal</p></div>'
        )
        got = parent_node.to_html()
        self.assertEqual(want, got)


if __name__ == "__main__":
    unittest.main()
