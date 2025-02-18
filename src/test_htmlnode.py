import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test__init__optional_values(self):
        html_node = HTMLNode()
        self.assertEqual(html_node.tag, "")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {})

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
                "href": "https://github.com/alnah/py-http-static-gen",
                "target": "_blank",
            },
        )
        want = "HTMLNode(tag='a', value='link', children=[HTMLNode(tag='b', value='bold', children=[], props={})], props={'href': 'https://github.com/alnah/py-http-static-gen', 'target': '_blank'})"
        got = repr(html_node)
        self.assertEqual(want, got)

    def test__to_html_placeholder(self):
        html_node = HTMLNode()
        with self.assertRaises(NotImplementedError) as ctx:
            html_node.to_html()
            self.assertEqual(ctx.exception, "Child classes will override this method")

    def test_props_to_html(self):
        html_node = HTMLNode(
            tag="a",
            value="link",
            props={
                "href": "https://github.com/alnah/py-http-static-gen",
                "target": "_blank",
            },
        )
        want = ' href="https://github.com/alnah/py-http-static-gen" target="_blank"'
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
        lead_node = LeafNode(
            tag="a",
            value="test",
            props={
                "href": "https://github.com/alnah/py-http-static-gen",
                "target": "_blank",
            },
        )
        want = '<a href="https://github.com/alnah/py-http-static-gen" target="_blank">test</a>'
        got = lead_node.to_html()
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
