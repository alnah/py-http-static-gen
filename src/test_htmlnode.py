import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test__init__empty_values(self):
        html_node = HTMLNode()
        self.assertEqual(html_node.tag, "")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {})

    def test__repr(self):
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
        want = "href='https://github.com/alnah/py-http-static-gen' target='_blank'"
        got = html_node.props_to_html()
        self.assertEqual(want, got)

    def test_props_to_html_empty_(self):
        html_node = HTMLNode(tag="a", value="link")
        want = ""
        got = html_node.props_to_html()
        self.assertEqual(want, got)
