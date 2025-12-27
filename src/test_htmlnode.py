import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
            _ = node.to_html()


class TestLeafNode(unittest.TestCase):
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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_for_index(self):
        title = LeafNode("title", "Why Frontend Development Sucks")
        head = ParentNode("head", [title])

        heading = LeafNode("h1", "Front-end Development is the Worst")

        para1 = LeafNode(
            "p",
            "Look, front-end development is for script kiddies and soydevs who can't handle the real programming. I mean, it's just a bunch of divs and spans, right? And css??? It's like, \"Oh, I want this to be red, but not thaaaaat red.\" What a joke.",
        )

        para2_block1 = LeafNode(
            None,
            "Real programmers code, not silly markup languages. They code on Arch Linux, not macOS, and certainly not Windows. They use Vim, not VS Code. They use C, not HTML. Come to the ",
        )
        para2_link1 = LeafNode("a", "backend", {"href": "https://www.boot.dev"})
        para2_block2 = LeafNode(None, ", where the real programming happens.")
        para2 = ParentNode("p", [para2_block1, para2_link1, para2_block2])

        body = ParentNode("body", [heading, para1, para2])

        html = ParentNode("html", [head, body])

        actual_html = html.to_html()
        expected_html = '<html><head><title>Why Frontend Development Sucks</title></head><body><h1>Front-end Development is the Worst</h1><p>Look, front-end development is for script kiddies and soydevs who can\'t handle the real programming. I mean, it\'s just a bunch of divs and spans, right? And css??? It\'s like, "Oh, I want this to be red, but not thaaaaat red." What a joke.</p><p>Real programmers code, not silly markup languages. They code on Arch Linux, not macOS, and certainly not Windows. They use Vim, not VS Code. They use C, not HTML. Come to the <a href="https://www.boot.dev">backend</a>, where the real programming happens.</p></body></html>'

        self.maxDiff = None
        self.assertEqual(actual_html, expected_html)


if __name__ == "__main__":
    _ = unittest.main()
