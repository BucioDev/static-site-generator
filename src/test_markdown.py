import unittest
from inline_markdown import (
    split_nodes_delimiter,extract_markdown_links, extract_markdown_images, split_nodes_images, split_nodes_link, text_to_textnodes
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestMarkdownExtraction(unittest.TestCase):

    # --------------------
    # Image Tests
    # --------------------

    def test_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_multiple_images(self):
        text = "![one](url1.png) some text ![two](url2.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("one", "url1.png"), ("two", "url2.jpg")],
            matches
        )

    def test_no_images(self):
        matches = extract_markdown_images("Just plain text")
        self.assertListEqual([], matches)

    def test_image_and_link(self):
        text = "![img](img.png) and [link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("img", "img.png")],
            matches
        )

    def test_empty_alt_text(self):
        matches = extract_markdown_images("![](image.png)")
        self.assertListEqual(
            [("", "image.png")],
            matches
        )

    # --------------------
    # Link Tests
    # --------------------

    def test_single_link(self):
        matches = extract_markdown_links(
            "Click [here](https://example.com)"
        )
        self.assertListEqual(
            [("here", "https://example.com")],
            matches
        )

    def test_multiple_links(self):
        text = "[one](url1) and [two](url2)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("one", "url1"), ("two", "url2")],
            matches
        )

    def test_ignore_images(self):
        text = "![img](img.png) and [link](url)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("link", "url")],
            matches
        )

    def test_no_links(self):
        matches = extract_markdown_links("No links here")
        self.assertListEqual([], matches)



class TestImageAndLinkSplitter(unittest.TestCase):

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_images([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "Click [Google](https://google.com) and [OpenAI](https://openai.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("OpenAI", TextType.LINK, "https://openai.com"),
            ],
            new_nodes,
        )

    def test_no_markdown(self):
        node = TextNode("Just plain text", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            new_nodes,
        )

    def test_mixed(self):
        node = TextNode(
            "Start ![img](img.png) middle [link](url.com) end",
            TextType.TEXT,
        )

        nodes = split_nodes_images([node])
        nodes = split_nodes_link(nodes)

        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "img.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
                TextNode(" end", TextType.TEXT),
            ],
            nodes,
        )

class TestTextToTextNodes(unittest.TestCase):
    def test_all_types(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")

        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
        nodes
        )

    def test_no_image(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and a [link](https://boot.dev)")

        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ],
        nodes
        )
    
    def test_only_text(self):
        nodes = text_to_textnodes("This is text with an italic word and a code block and a link https://boot.dev")

        self.assertListEqual([
            TextNode("This is text with an italic word and a code block and a link https://boot.dev", TextType.TEXT),
        ],
        nodes
        )

if __name__ == "__main__":
    unittest.main()