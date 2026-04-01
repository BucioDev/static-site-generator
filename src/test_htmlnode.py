import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_with_props(self):
        node = HTMLNode(
            tag="a",
            props={"href": "https://example.com", "target": "_blank"}
        )
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://example.com" target="_blank"')

    def test_props_to_html_no_props(self):
        node = HTMLNode(tag="p")
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_repr_output(self):
        node = HTMLNode(tag="div", value="Hello", children=None, props=None)
        result = repr(node)
        self.assertEqual(result, "HTMLNode(div, Hello, children: None, None)")


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

class TestParentNode(unittest.TestCase):
    def test_to_html_multiple_children(self):
        node = ParentNode("div", [
            LeafNode("b", "bold"),
            LeafNode("i", "italic"),
        ])
        self.assertEqual(node.to_html(), "<div><b>bold</b><i>italic</i></div>")

    def test_to_html_mixed_children(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold"),
            LeafNode(None, "Normal"),
        ])
        self.assertEqual(node.to_html(), "<p><b>Bold</b>Normal</p>")

    def test_to_html_deep_nesting(self):
        node = ParentNode("div", [
            ParentNode("section", [
                ParentNode("p", [
                    LeafNode("b", "deep")
                ])
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><section><p><b>deep</b></p></section></div>"
        )

    def test_to_html_empty_children(self):
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")
    
    def test_to_html_no_tag_raises(self):
        node = ParentNode(None, [LeafNode("b", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_plain_text_child(self):
        node = ParentNode("p", [LeafNode(None, "hello")])
        self.assertEqual(node.to_html(), "<p>hello</p>")

if __name__ == "__main__":
    unittest.main()

