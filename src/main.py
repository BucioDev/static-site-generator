from textnode import TextNode, TextType
from pathlib import Path
from static_generator import copy_static_to_public, generate_pages_recursive
import sys

dir_path_static = "./static"
dir_path_public = "./docs" #kinda
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def main():
    node = TextNode("This is some anchor text", TextType.LINK,url="https://www.boot.dev")
    print("This text comes form the main")
    print(node)
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_static_to_public()
    
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)
        
main()