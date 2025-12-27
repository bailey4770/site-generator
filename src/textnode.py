from enum import Enum
import re
from typing import override, Callable


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


def block_to_text_nodes(text: str) -> list[TextNode]:
    """Simply pass MD text as string to be parsed, and list of TextNodes will be returned"""
    removed_nl = " ".join(line.strip() for line in text.splitlines())
    text_node = TextNode(removed_nl, TextType.TEXT)
    debug = False

    if debug:
        print(f"===========FOR INPUT {text}==============")

    # image extraction MUST be run before link extraction, due to markdown syntax
    nodes = _split_nodes([text_node], extractor=_split_node_images, debug=debug)
    nodes = _split_nodes(nodes, extractor=_split_node_links, debug=debug)
    nodes = _split_nodes(nodes, "`", TextType.CODE, debug=debug)
    nodes = _split_nodes(nodes, "_", TextType.ITALIC, debug=debug)
    nodes = _split_nodes(nodes, "**", TextType.BOLD, debug=debug)

    return nodes


def _split_nodes(
    old_nodes: list[TextNode],
    delimiter: str | None = None,
    text_type: TextType | None = None,
    extractor: Callable[[TextNode], list[TextNode]] | None = None,
    debug: bool = False,
) -> list[TextNode]:
    output: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            output.append(old_node)
            continue

        if not extractor:
            if not delimiter or not text_type:
                raise ValueError(
                    "If no extracter is supplied, delimiter and text type must be"
                )
            output.extend(_split_node_delimiter(old_node, delimiter, text_type))

        else:
            output.extend(extractor(old_node))

    if debug:
        print("=====")
        print(delimiter, extractor)
        for node in output:
            print(node)

    return output


def _split_node_delimiter(
    old_node: TextNode, delimiter: str, text_type: TextType
) -> list[TextNode]:
    output: list[TextNode] = []

    parts = old_node.text.split(delimiter)
    if len(parts) % 2 == 0:
        raise ValueError("Invalid input: that is invalid Markdown syntax")

    inside = False
    for part in parts:
        if len(part) == 0:
            inside = not inside
            continue

        if not inside:
            new_node = TextNode(part, old_node.text_type)
        else:
            new_node = TextNode(part, text_type)

        output.append(new_node)
        inside = not inside

    return output


def _split_node_links(old_node: TextNode) -> list[TextNode]:
    links = _extract_markdown_links(old_node.text)
    parts = old_node.text.split("[")
    if not links or len(parts) == 0:
        return [old_node]

    return _split_by_extractables(parts, links, TextType.LINK)


def _split_node_images(old_node: TextNode) -> list[TextNode]:
    images = _extract_markdown_images(old_node.text)
    parts = old_node.text.split("![")
    if not images or len(parts) == 0:
        return [old_node]

    return _split_by_extractables(parts, images, TextType.IMAGE)


def _split_by_extractables(
    parts: list[str], extractables: list[tuple[str, str]], text_type: TextType
) -> list[TextNode]:
    output: list[TextNode] = []
    i = 0

    for part in parts:
        removed_extractable = part.split("](".join(extractables[i]))
        if len(removed_extractable) == 1:
            new_node = TextNode(removed_extractable[0], TextType.TEXT)
            output.append(new_node)
        else:
            link_node = TextNode(extractables[i][0], text_type, extractables[i][1])
            output.append(link_node)

            new_text = removed_extractable[1][1:]
            if new_text == "":
                continue
            new_node = TextNode(new_text, TextType.TEXT)

            output.append(new_node)
            i += 1

    return output


def _extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def _extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
