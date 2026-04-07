from textnode import TextNode, TextType
from pathlib import Path
from static_generator import copy_static_to_public, generate_pages_recursive
import sys

dir_path_static = "./static"
dir_path_public = "./docs" #kinda
dir_path_content = "./content"
template_path = "./template.html"

def main():
    node = TextNode("This is some anchor text", TextType.LINK,url="https://www.boot.dev")
    print("This text comes form the main")
    print(node)
    if sys.argv == None:
        basepath = "/"
    else:
        basepath = sys.argv[0]
    copy_static_to_public()
    
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)
        
main()