import unittest

from textnode import TextType, TextNode
from main import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
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


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_italic(self):
        node = TextNode("This test has an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This test has an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_already_parsed(self):
        node = TextNode("italic text", TextType.ITALIC)
        new_node = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual([node], new_node)

    def test_list_input(self):
        nodes = [
            TextNode("**Bold Text**", TextType.TEXT),
            TextNode("some plain text", TextType.TEXT),
            TextNode("then some _italic text_", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)

        expected = [
            TextNode("Bold Text", TextType.BOLD),
            TextNode("some plain text", TextType.TEXT),
            TextNode("then some ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_fake_delimiter(self):
        node = TextNode("This text has no comma", TextType.TEXT)
        new_node = split_nodes_delimiter([node], ",", TextType.ITALIC)
        self.assertListEqual([node], new_node)

    def test_input_error(self):
        node = TextNode("This text is **invalid", TextType.TEXT)
        with self.assertRaises(ValueError):
            _ = split_nodes_delimiter([node], "**", TextType.BOLD)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(actual, expected)

    def test_not_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_images(text)
        expected = None
        self.assertNotEqual(actual, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_Links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(actual, expected)

    def test_not_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = extract_markdown_links(text)
        expected = None
        self.assertNotEqual(actual, expected)
