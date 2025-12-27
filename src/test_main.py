import unittest

from textnode import TextType, TextNode
from main import (
    text_node_to_html_node,
    md_to_html_node,
)


class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("learn backend", TextType.LINK, "boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "learn backend")
        self.assertEqual(html_node.props, {"href": "boot.dev"})

    def test_image(self):
        node = TextNode("an image", TextType.IMAGE, "content/image.jpeg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "content/image.jpeg", "alt": "an image"}
        )


class TestMDToHTML(unittest.TestCase):
    def test_blocks_no_inline(self):
        sample_md = """# heading\n\nsome text\n\n- and an\n- unordered\n- list\n\n1. and an\n2. ordered\n3. list\n\n> with a\n> quote\n\nand a\n\n```print(\"code block\")```"""
        actual = md_to_html_node(sample_md).to_html()
        expected = '<div><h1>heading</h1><p>some text</p><ul><li>and an</li><li>unordered</li><li>list</li></ul><ol><li>and an</li><li>ordered</li><li>list</li></ol><blockquote>with a\nquote\n</blockquote><p>and a</p><pre><code>print("code block")</code></pre></div>'
        self.assertEqual(actual, expected)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
        actual = md_to_html_node(md).to_html()
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(actual, expected)

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        actual = md_to_html_node(md).to_html()
        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        self.assertEqual(actual, expected)

    def test_blocks_and_inline(self):

