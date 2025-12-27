import unittest
from blocks import BlockType, markdown_to_blocks, find_block_type


class TestMarkdownToBlocks(unittest.TestCase):
    def test_1(self):
        sample_md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        actual = markdown_to_blocks(sample_md)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
        ]
        self.assertListEqual(actual, expected)

    def test_2(self):
        sample_md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        actual = markdown_to_blocks(sample_md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertListEqual(actual, expected)

    def test_3(self):
        sample_md = """# Weird spacing


    Here is a _list_:

    - first
      - second"""
        actual = markdown_to_blocks(sample_md)
        expected = ["# Weird spacing", "Here is a _list_:", "- first\n- second"]
        self.assertListEqual(actual, expected)


class TestBlockToBlock(unittest.TestCase):
    def test_ordered_list(self):
        block = "1. One\n2. second\n3. again"
        actual = find_block_type(block)
        expected = BlockType.ORDERED_LIST
        self.assertEqual(actual, expected)

    def test_false_ordered_list(self):
        block = "1. hey\n3. skipped\n4. okay"
        actual = find_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(actual, expected)

    def test_unordered_list(self):
        block = "- help\n- me"
        actual = find_block_type(block)
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(actual, expected)

    def test_heading(self):
        block = "## heading"
        actual = find_block_type(block)
        expected = BlockType.HEADING
        self.assertEqual(actual, expected)

    def test_false_heading(self):
        block = "####### too many hashes"
        actual = find_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(actual, expected)

    def test_code(self):
        block = '```\nprint("hello world!")\n```'
        actual = find_block_type(block)
        expected = BlockType.CODE
        self.assertEqual(actual, expected)

    def test_false_code(self):
        block = "``x = 1\n"
        actual = find_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(actual, expected)

    def test_quote(self):
        block = "> I am\n> highly skilled\n> as Prime Minister\n> increased GDP"
        actual = find_block_type(block)
        expected = BlockType.QUOTE
        self.assertEqual(actual, expected)

    def test_false_quote(self):
        block = "> This is\n a false\n> quote"
        actual = find_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(actual, expected)

    def test_paragraph(self):
        block = "normal block\nof text\nin a\nparagraph"
        actual = find_block_type(block)
        expected = BlockType.PARAGRAPH
        self.assertEqual(actual, expected)
