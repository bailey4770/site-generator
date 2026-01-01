import unittest

from textnode import TextType, TextNode
from md_converter import (
    _text_node_to_html_node,
    md_to_html_node,
)


class TestTextToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = _text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = _text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = _text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = _text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("learn backend", TextType.LINK, "boot.dev")
        html_node = _text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "learn backend")
        self.assertEqual(html_node.props, {"href": "boot.dev"})

    def test_image(self):
        node = TextNode("an image", TextType.IMAGE, "content/image.jpeg")
        html_node = _text_node_to_html_node(node)
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
        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"
        self.assertEqual(actual, expected)

    def test_mixed_headings_and_lists(self):
        md = """## Subheading

* first bullet
* second bullet

### Smaller heading

1. numbered one
2. numbered two
3. numbered three"""
        actual = md_to_html_node(md).to_html()
        expected = "<div><h2>Subheading</h2><ul><li>first bullet</li><li>second bullet</li></ul><h3>Smaller heading</h3><ol><li>numbered one</li><li>numbered two</li><li>numbered three</li></ol></div>"
        self.assertEqual(actual, expected)

    def test_quotes_and_code_blocks(self):
        md = """> This is a quoted section
> with multiple lines

```python
def example():
    return True
```

> Another quote after code"""
        actual = md_to_html_node(md).to_html()
        expected = "<div><blockquote>This is a quoted section\nwith multiple lines\n</blockquote><pre><code>def example():\n    return True</code></pre><blockquote>Another quote after code\n</blockquote></div>"
        self.assertEqual(actual, expected)

    def test_empty_and_whitespace_blocks(self):
        md = """# Title


Some text with gaps


- list item"""
        actual = md_to_html_node(md).to_html()
        expected = "<div><h1>Title</h1><p>Some text with gaps</p><ul><li>list item</li></ul></div>"
        self.assertEqual(actual, expected)

    def test_images_in_paragraph(self):
        md = "Here is an ![image](images/test.png)"
        actual = md_to_html_node(md).to_html()
        expected = (
            '<div><p>Here is an <img src="images/test.png" alt="image"></p></div>'
        )
        self.assertEqual(actual, expected)

    def test_links_in_unordered_list(self):
        md = """

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)
"""
        actual = md_to_html_node(md).to_html()
        expected = '<div><h2>Blog posts</h2><ul><li><a href="/blog/glorfindel">Why Glorfindel is More Impressive than Legolas</a></li><li><a href="/blog/tom">Why Tom Bombadil Was a Mistake</a></li><li><a href="/blog/majesty">The Unparalleled Majesty of "The Lord of the Rings"</a></li></ul></div>'
        self.assertEqual(actual, expected)

    def test_links_in_ordered_list(self):
        md = """

## Blog posts

1. [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
2. [Why Tom Bombadil Was a Mistake](/blog/tom)
3. [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)
"""
        actual = md_to_html_node(md).to_html()
        expected = '<div><h2>Blog posts</h2><ol><li><a href="/blog/glorfindel">Why Glorfindel is More Impressive than Legolas</a></li><li><a href="/blog/tom">Why Tom Bombadil Was a Mistake</a></li><li><a href="/blog/majesty">The Unparalleled Majesty of "The Lord of the Rings"</a></li></ol></div>'
        self.assertEqual(actual, expected)

    def test_inline_bold_italic_code_in_lists(self):
        md = """
- this should be **bold**
- and this in _italics_
- `and this in code`

1. this should be **bold**
2. and this in _italics_
3. `and this in code` 
    """
        actual = md_to_html_node(md).to_html()
        expected = "<div><ul><li>this should be <b>bold</b></li><li>and this in <i>italics</i></li><li><code>and this in code</code></li></ul><ol><li>this should be <b>bold</b></li><li>and this in <i>italics</i></li><li><code>and this in code</code></li></ol></div>"
        self.assertEqual(actual, expected)
