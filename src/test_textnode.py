import unittest

from textnode import TextType, TextNode


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
            TextType.PLAIN,
        )
        node2 = TextNode("...to the text here", TextType.PLAIN)
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    _ = unittest.main()
