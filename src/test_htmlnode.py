import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    _ = unittest.main()
