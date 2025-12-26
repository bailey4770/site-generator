import unittest

from textnode import (
    TextType,
    TextNode,
    _extract_markdown_images,
    _extract_markdown_links,
    _split_nodes,
    _split_node_links,
    _split_node_images,
    blocks_to_text_nodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node1 = TextNode("This is bold text", TextType.BOLD)
        node2 = TextNode("This is bold text", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_eq2(self):
        node1 = TextNode("This is a link node", TextType.BOLD, "boot.dev")
        node2 = TextNode("This is a link node", TextType.BOLD, "boot.dev")
        self.assertEqual(node1, node2)

    def test_eq3(self):
        node1 = TextNode("This is an image node", TextType.BOLD, "./content/img1.jpeg")
        node2 = TextNode("This is an image node", TextType.BOLD, "./content/img1.jpeg")
        self.assertEqual(node1, node2)

    def test_not_eq1(self):
        node1 = TextNode(
            "One is missing a link",
            TextType.LINK,
            "boot.dev",
        )
        node2 = TextNode("One is missing a link", TextType.LINK)
        self.assertNotEqual(node1, node2)

    def test_not_eq2(self):
        node1 = TextNode("One is bold and the other italic", TextType.BOLD)
        node2 = TextNode(
            "One is bold and the other italic",
            TextType.ITALIC,
        )
        self.assertNotEqual(node1, node2)

    def test_not_eq3(self):
        node1 = TextNode(
            "Links don't match",
            TextType.LINK,
            "boot.dev",
        )
        node2 = TextNode("Links don't match", TextType.LINK, "archlinx.org")
        self.assertNotEqual(node1, node2)

    def test_not_eq4(self):
        node1 = TextNode(
            "The text here is...",
            TextType.TEXT,
        )
        node2 = TextNode("...to the text here", TextType.TEXT)
        self.assertNotEqual(node1, node2)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_Links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = _extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(actual, expected)

    def test_not_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = _extract_markdown_links(text)
        expected = None
        self.assertNotEqual(actual, expected)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual = _extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(actual, expected)

    def test_not_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual = _extract_markdown_images(text)
        expected = None
        self.assertNotEqual(actual, expected)


class TextSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = _split_nodes([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_italic(self):
        node = TextNode("This test has an _italic_ word", TextType.TEXT)
        new_nodes = _split_nodes([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This test has an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_already_parsed(self):
        node = TextNode("italic text", TextType.ITALIC)
        new_node = _split_nodes([node], "_", TextType.ITALIC)
        self.assertListEqual([node], new_node)

    def test_list_input(self):
        nodes = [
            TextNode("**Bold Text**", TextType.TEXT),
            TextNode("some plain text", TextType.TEXT),
            TextNode("then some _italic text_", TextType.TEXT),
        ]

        new_nodes = _split_nodes(nodes, "**", TextType.BOLD)
        new_nodes = _split_nodes(new_nodes, "_", TextType.ITALIC)

        expected = [
            TextNode("Bold Text", TextType.BOLD),
            TextNode("some plain text", TextType.TEXT),
            TextNode("then some ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_fake_delimiter(self):
        node = TextNode("This text has no comma", TextType.TEXT)
        new_node = _split_nodes([node], ",", TextType.ITALIC)
        self.assertListEqual([node], new_node)

    def test_input_error(self):
        node = TextNode("This text is **invalid", TextType.TEXT)
        with self.assertRaises(ValueError):
            _ = _split_nodes([node], "**", TextType.BOLD)


class TestSplitNodesLinks(unittest.TestCase):
    def test_2links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        actual = _split_nodes([node], extractor=_split_node_links)
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(actual, expected)

    def test_1link(self):
        node = TextNode(
            "This text [to boot dev](https://www.boot.dev) contains 1 link",
            TextType.TEXT,
        )
        actual = _split_nodes([node], extractor=_split_node_links)
        expected = [
            TextNode("This text ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" contains 1 link", TextType.TEXT),
        ]
        self.assertListEqual(actual, expected)

    def test_no_link(self):
        node = TextNode("This contains no link", TextType.TEXT)
        actual = _split_nodes([node], extractor=_split_node_links)
        self.assertListEqual(actual, [node])

    def test_invalid_syntax(self):
        node = TextNode("This contains an [invalid (image.png)", TextType.TEXT)
        actual = _split_nodes([node], extractor=_split_node_links)
        self.assertListEqual(actual, [node])

    def test_link_and_image_to_link_func(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)! and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        actual = _split_nodes([node], extractor=_split_node_links)
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode("! and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertListEqual(actual, expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        actual = _split_nodes([node], extractor=_split_node_images)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(actual, expected)

    def test_no_image(self):
        node = TextNode("This contains no image", TextType.TEXT)
        actual = _split_nodes([node], extractor=_split_node_images)
        self.assertListEqual(actual, [node])

    def test_invalid_syntax(self):
        node = TextNode("This contains an ![invalid (image.png)", TextType.TEXT)
        actual = _split_nodes([node], extractor=_split_node_images)
        self.assertListEqual(actual, [node])

    def test_invalid_syntax2(self):
        node = TextNode("This contains an [invalid](image.png)", TextType.TEXT)
        actual = _split_nodes([node], extractor=_split_node_images)
        self.assertListEqual(actual, [node])


class TestSplitNodes(unittest.TestCase):
    def test_list(self):
        nodes = [
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                TextType.TEXT,
            ),
            TextNode(
                "This text [to boot dev](https://www.boot.dev) contains 1 link",
                TextType.TEXT,
            ),
        ]
        actual = _split_nodes(nodes, extractor=_split_node_links)
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode("This text ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" contains 1 link", TextType.TEXT),
        ]
        self.assertListEqual(actual, expected)


class TestTextToTextNodes(unittest.TestCase):
    def test_1_of_each(self):
        sample_md = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        actual = blocks_to_text_nodes(sample_md)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(actual, expected)

    def test_2(self):
        sample_md = "**Heading** welome to this _test_. Here is a [link](www.archlinux.org) and another [link](www.boot.dev). See this image ![test](test.png) too **end of page**"
        actual = blocks_to_text_nodes(sample_md)
        expected = [
            TextNode("Heading", TextType.BOLD),
            TextNode(" welome to this ", TextType.TEXT),
            TextNode("test", TextType.ITALIC),
            TextNode(". Here is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "www.archlinux.org"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("link", TextType.LINK, "www.boot.dev"),
            TextNode(". See this image ", TextType.TEXT),
            TextNode("test", TextType.IMAGE, "test.png"),
            TextNode(" too ", TextType.TEXT),
            TextNode("end of page", TextType.BOLD),
        ]
        self.assertListEqual(actual, expected)

    def test_invalid_syntax_heading(self):
        sample_md = "**incomplete heading*"
        with self.assertRaises(ValueError):
            _ = blocks_to_text_nodes(sample_md)

    def test_invalid_syntax_nested_links(self):
        sample_md = "Here is an ![image (test.png) but [with a link](link.com)"
        actual = blocks_to_text_nodes(sample_md)
        expected = [
            TextNode("Here is an !", TextType.TEXT),
            TextNode("image (test.png) but ", TextType.TEXT),
            TextNode("with a link", TextType.LINK, "link.com"),
        ]
        self.assertListEqual(actual, expected)


if __name__ == "__main__":
    _ = unittest.main()
