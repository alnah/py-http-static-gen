import unittest
from enum import Enum
from typing import Optional


class TextType(Enum):
    NORMAL = 0
    BOLD = 1
    ITALIC = 2
    CODE = 3
    LINK = 4
    IMAGE = 5


class TextNode:
    def __init__(
        self,
        text: str,
        text_type: TextType,
        url: Optional[str] = None,
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url if url is not None else ""

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text,
            self.text_type,
            self.url,
        ) == (
            other.text,
            other.text_type,
            other.url,
        )

    def __repr__(self):
        return f"TextNode(text={self.text!r}, text_type={self.text_type!r}, url={self.url!r})"


if __name__ == "__main__":
    unittest.main()
