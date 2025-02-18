from typing import Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list["HTMLNode"]] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        self.tag = tag if tag is not None else ""
        self.value = value if value is not None else ""
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

    def to_html(self) -> str:
        raise NotImplementedError("Child classes will override this method")

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return "".join(f' {k}="{v}"' for k, v in self.props.items())


class LeafNode(HTMLNode):
    def __init__(
        self,
        value: str,
        tag: Optional[str] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if self.tag == "":
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        def recursive_to_html(node: HTMLNode) -> str:
            if isinstance(node, LeafNode):
                return node.to_html()
            elif isinstance(node, ParentNode):
                children_html = "".join(
                    recursive_to_html(child) for child in node.children
                )
                return f"<{node.tag}{node.props_to_html()}>{children_html}</{node.tag}>"
            else:
                return ""

        return recursive_to_html(self)
