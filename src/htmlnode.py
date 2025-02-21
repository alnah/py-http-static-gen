from typing import Optional


class HTMLNode:
    """Abstract base for HTML nodes."""

    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list["HTMLNode"]] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        """Initialize HTMLNode with tag, value, children, and props."""
        self.tag = tag if tag is not None else ""
        self.value = value if value is not None else ""
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def __eq__(self, other: object) -> bool:
        """Check equality by comparing tag, value, children, and props."""
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self) -> str:
        """Return a reproducible string representation of the node."""
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

    def to_html(self) -> str:
        """Convert node to HTML; must be implemented by subclasses."""
        raise NotImplementedError("Child classes will override this method")

    def props_to_html(self) -> str:
        """Render properties as HTML attributes."""
        if not self.props:
            return ""
        return "".join(f' {k}="{v}"' for k, v in self.props.items())


class LeafNode(HTMLNode):
    """HTML node representing a leaf (no children)."""

    def __init__(
        self,
        value: str,
        tag: Optional[str] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        """Initialize LeafNode with value, optional tag, and props."""
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        """Convert leaf node to HTML string."""
        if self.tag == "":
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}/>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    """HTML node that contains child nodes."""

    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: Optional[dict[str, str]] = None,
    ) -> None:
        """Initialize ParentNode with tag and child nodes."""
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        """Recursively convert node and children to HTML string."""

        def recursive_to_html(node: HTMLNode) -> str:
            if isinstance(node, LeafNode):
                return node.to_html()
            elif isinstance(node, ParentNode):
                children = node.children
                children_html = "".join(recursive_to_html(child) for child in children)
                return f"<{node.tag}{node.props_to_html()}>{children_html}</{node.tag}>"
            else:
                return ""

        return recursive_to_html(self)
