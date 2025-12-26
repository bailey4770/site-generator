import re

from textnode import TextType, TextNode
from htmlnode import LeafNode


def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str):
    return re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    output: list[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            output.append(old_node)
            continue

        text = old_node.text
        parts = text.split(delimiter)

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


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url:
                return LeafNode("a", text_node.text, {"href": text_node.url})
            else:
                raise ValueError("no link provided")
        case TextType.IMAGE:
            if text_node.url:
                return LeafNode(
                    "img", "", {"src": text_node.url, "alt": text_node.text}
                )
            else:
                raise ValueError("no link provided")


def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

    print(node)


if __name__ == "__main__":
    main()
