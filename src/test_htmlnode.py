import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_prop_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)

        expected_string = ' href="https://www.google.com" target="_blank"'
        actual_string = node.props_to_html()

        self.assertEqual(expected_string, actual_string)

    def test_to_html(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)

        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node1 = HTMLNode("tag", "text")
        node2 = HTMLNode("tag bold", "bold text")
        node3 = HTMLNode("tag parent", "parent text", [node1, node2])

        print(node3)


class TestLeadNode(unittest.TestCase):
    def test_leaf_to_html1(self):
        node = LeafNode("p", "Hello, world!")
        expected = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html3(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = LeafNode("a", "Click me!", props)
        expected = '<a href="https://www.google.com" target="_blank">Click me!</a>'
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    _ = unittest.main()
