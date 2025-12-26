from enum import Enum
from typing import override


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    @override
    def __eq__(self, node2: object):
        if not isinstance(node2, TextNode):
            return False

        if (
            self.text == node2.text
            and self.text_type == node2.text_type
            and self.url == node2.url
        ):
            return True

        return False

    @override
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
