from blocks import BlockType, get_block_type, markdown_to_blocks
from textnode import TextType, TextNode, block_to_text_nodes
from htmlnode import HTMLNode, LeafNode, ParentNode
import config as cfg


def md_to_html_node(markdown: str) -> HTMLNode:
    def _remove_marks_lines(block: str) -> str:
        space_idx = block.find(" ")
        return "".join(line[space_idx + 1 :] + "\n" for line in block.splitlines())

    children: list[HTMLNode] = []
    blocks: list[str] = markdown_to_blocks(markdown)

    for block in blocks:
        if not block:
            continue
        node: HTMLNode = HTMLNode()

        match get_block_type(block):
            case BlockType.PARAGRAPH:
                text_nodes = block_to_text_nodes(block)
                node = text_nodes_to_parent(text_nodes)
            case BlockType.HEADING:
                parts = block.split()
                heading_number = "h" + str(len(parts[0]))
                node = LeafNode(heading_number, parts[1])
            case BlockType.CODE:
                backticks_removed = block.strip()[3:-3]
                # also remove leading new lines and empty space
                backticks_removed = backticks_removed.strip()

                language = backticks_removed.splitlines()[0]
                if language.lower() in cfg.get_languages():
                    code_node = LeafNode("code", backticks_removed[len(language) + 1 :])
                else:
                    code_node = LeafNode("code", backticks_removed)

                node = ParentNode("pre", [code_node])
            case BlockType.QUOTE:
                quotemark_removed = _remove_marks_lines(block)
                node = LeafNode("blockquote", quotemark_removed)
            case BlockType.UNORDERED_LIST:
                bullets_removed = _remove_marks_lines(block)
                unordered_list_nodes: list[HTMLNode] = [
                    LeafNode("li", line) for line in bullets_removed.split("\n") if line
                ]
                node = ParentNode("ul", unordered_list_nodes)
            case BlockType.ORDERED_LIST:
                numbers_removed = _remove_marks_lines(block)
                ordered_list_nodes: list[HTMLNode] = [
                    LeafNode("li", line) for line in numbers_removed.split("\n") if line
                ]
                node = ParentNode("ol", ordered_list_nodes)

        children.append(node)

    final_parent = ParentNode("div", children)
    return final_parent


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


def text_nodes_to_parent(text_nodes: list[TextNode]) -> ParentNode:
    children: list[HTMLNode] = []
    for node in text_nodes:
        leaf = text_node_to_html_node(node)
        children.append(leaf)

    return ParentNode("p", children)


def main():
    blocks = [
        "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n    ```\n    "
    ]
    print(get_block_type(blocks[0]))


if __name__ == "__main__":
    main()
