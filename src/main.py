from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
from inline_markdown import split_nodes_delimiter, split_nodes_link, split_nodes_images

def main():
    node = TextNode("This is some anchor text", TextType.LINK,url="https://www.boot.dev")
    print("This text comes form the main")
    print(node)

def text_node_to_html_node(text_node):
    text = text_node.text
    url = text_node.url
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None,text)
        case TextType.BOLD:
            return LeafNode("b",text)
        case TextType.ITALIC:
            return LeafNode("i",text)
        case TextType.CODE:
            return LeafNode("code",text)
        case TextType.LINK:
            return LeafNode("a",text,{"href":url})
        case TextType.IMAGE:
            return LeafNode("img",None,{
                "src":url,
                "alt":text
            })
        case _:
            raise Exception("text node requires Text Type")
        
def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = []
    nodes = split_nodes_delimiter([node],  "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,  "_", TextType.ITALIC) 
    nodes = split_nodes_delimiter(nodes,  "`", TextType.CODE)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

main()