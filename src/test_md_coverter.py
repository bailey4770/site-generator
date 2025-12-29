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
        expected = "<div><h2>Subheading</h2><ul><li>first bullet</li><li>second bullet</li></ul><h3>Smaller</h3><ol><li>numbered one</li><li>numbered two</li><li>numbered three</li></ol></div>"
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

    def test_tolkien_fan_club(self):
        md = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)

## Reasons I like Tolkien

- You can spend years studying the legendarium and still not understand its depths
- It can be enjoyed by children and adults alike
- Disney _didn't ruin it_ (okay, but Amazon might have)
- It created an entirely new genre of fantasy

## My favorite characters (in order)

1. Gandalf
2. Bilbo
3. Sam
4. Glorfindel
5. Galadriel
6. Elrond
7. Thorin
8. Sauron
9. Aragorn

Here's what `elflang` looks like (the perfect coding language):

```
func main(){
    fmt.Println("Aiya, Ambar!")
}
```

Want to get in touch? [Contact me here](/contact).

This site was generated with a custom-built [static site generator](https://www.boot.dev/courses/build-static-site-generator-python) from the course on [Boot.dev](https://www.boot.dev)."""
        actual = md_to_html_node(md).to_html()
        expected = '<div><h1>Tolkien Fan Club</h1><p><img src="/images/tolkien.png" alt="JRR Tolkien sitting"></p><p>Here&#39;s the deal, <strong>I like Tolkien</strong>.</p><blockquote><p>&quot;I am in fact a Hobbit in all but size.&quot;</p><p>-- J.R.R. Tolkien</p></blockquote><h2>Blog posts</h2><ul><li><a href="/blog/glorfindel">Why Glorfindel is More Impressive than Legolas</a></li><li><a href="/blog/tom">Why Tom Bombadil Was a Mistake</a></li><li><a href="/blog/majesty">The Unparalleled Majesty of &quot;The Lord of the Rings&quot;</a></li></ul><h2>Reasons I like Tolkien</h2><ul><li>You can spend years studying the legendarium and still not understand its depths</li><li>It can be enjoyed by children and adults alike</li><li>Disney <em>didn&#39;t ruin it</em> (okay, but Amazon might have)</li><li>It created an entirely new genre of fantasy</li></ul><h2>My favorite characters (in order)</h2><ol><li>Gandalf</li><li>Bilbo</li><li>Sam</li><li>Glorfindel</li><li>Galadriel</li><li>Elrond</li><li>Thorin</li><li>Sauron</li><li>Aragorn</li></ol><p>Here&#39;s what <code>elflang</code> looks like (the perfect coding language):</p><pre><code>func main(){fmt.Println(&quot;Aiya, Ambar!&quot;)}</code></pre><p>Want to get in touch? <a href="/contact">Contact me here</a>.</p><p>This site was generated with a custom-built <a href="https://www.boot.dev/courses/build-static-site-generator-python">static site generator</a> from the course on <a href="https://www.boot.dev">Boot.dev</a>.</p></div>'
        self.maxDiff = None
        self.assertEqual(actual, expected)
