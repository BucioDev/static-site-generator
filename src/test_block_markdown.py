import unittest
from block_markdown import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node

class TestBlockMarkdown(unittest.TestCase):
    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    
    
    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
        
    def test_only_whitespace(self):
        md = "   \n\n   \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
        
    def test_single_block(self):
        md = "This is just one block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is just one block"])
    
    def test_leading_trailing_newlines(self):
        md = "\n\nThis is a block\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a block"])
    
    def test_multiple_empty_blocks(self):
        md = "Block one\n\n\n\nBlock two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block one", "Block two"])
    
    def test_preserves_internal_newlines(self):
        md = "Line one\nLine two\n\nLine three"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Line one\nLine two", "Line three"]
        )
    
    def test_mixed_markdown(self):
        md = """
    # Heading

    Paragraph text here

    - Item 1
    - Item 2

    Another paragraph
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph text here",
                "- Item 1\n    - Item 2",
                "Another paragraph",
            ],
        )
        
        ## TEST FOR BLOCK TYPE
        
    def test_blocktype_heading(self):
        text = "# Heading 1"
        blocktype = block_to_block_type(text)
        
        self.assertEqual(blocktype, BlockType.HEADING)
        
    def test_blocktype_heading6(self):
        text = "###### Heading 6"
        blocktype = block_to_block_type(text)
        
        self.assertEqual(blocktype, BlockType.HEADING)
    
    def test_blocktype_not_heading(self):
        text = "######### Heading 6"
        blocktype = block_to_block_type(text)
        
        self.assertEqual(blocktype, BlockType.PARAGRAPH)
    
    def test_blocktype_quote(self):
        text = "> line 1\n> line 2"
        blocktype = block_to_block_type(text)
        
        self.assertEqual(blocktype, BlockType.QUOTE)
    
    def test_blocktype_code_block(self):
        text = "```\nprint('hi')\n```"
        blocktype = block_to_block_type(text)
        
        self.assertEqual(blocktype, BlockType.CODE)
        
    def test_blocktype_unordered_list(self):
        text = "- item 1\n- item 2"
        blocktype = block_to_block_type(text)
        
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)
    
    def test_blocktype_ordered_list(self):
        text = "1. one\n2. two\n3. three"
        blocktype = block_to_block_type(text)
        
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )






if __name__ == "__main__":
    unittest.main()