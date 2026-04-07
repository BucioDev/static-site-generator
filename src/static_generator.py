import os
import shutil
import re
from block_markdown import markdown_to_blocks, markdown_to_html_node, BlockType
from htmlnode import HTMLNode


def copy_static_to_public():
    base_dir = os.path.dirname(__file__)
    
    public_path = os.path.join(base_dir, "..", "docs")
    static_path = os.path.join(base_dir, "..", "static")
    if os.path.exists(public_path) and os.path.exists(static_path):
        print(f"public path {public_path}")
        print(f"static path {static_path}")
        delete_all_on(public_path)
        copy_all_to(static_path, public_path)
    

def delete_all_on(public_path):
    files = os.listdir(path=public_path)
    for file in files:
        file_path = os.path.join(public_path, file)
        if not os.path.isfile(file_path):
            print("found folder")
            delete_all_on(file_path)
    print(f"deleting : {public_path}" )
    shutil.rmtree(public_path)
    print("creating empty public folfer")
    os.mkdir(public_path)


def copy_all_to(origin_path, destiny_path):
    files = os.listdir(origin_path)
    for file in files:
        file_path = os.path.join(origin_path, file)
        if not os.path.isfile(file_path):
            print(f"entering folder {file_path}")
            nested_path = os.path.join(destiny_path, file)
            os.mkdir(nested_path)
            copy_all_to(file_path, nested_path)
        else:
            print(f"copying {file_path} --> {destiny_path}")
            shutil.copy(file_path, destiny_path)



def extract_title(markdown):    
    title = None
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if re.fullmatch(r'#\s+\S.*', block):
            title = block
            break
    if title is None:
        raise Exception("Title is required")
    title = title.replace("#", "")
    return title.strip()



def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()
    
    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()
    
    node = markdown_to_html_node(markdown_content)
    html = node.to_html()
    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)
    
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    files = os.listdir(dir_path_content)
    for file in files:
        file_path = os.path.join(dir_path_content, file)
        if not os.path.isfile(file_path):
            nested_path = os.path.join(dest_dir_path,file)
            os.mkdir(nested_path)
            generate_pages_recursive(file_path, template_path, nested_path, basepath)
        else:
            index_html = os.path.join(dest_dir_path, "index.html")
            generate_page(file_path, template_path, index_html, basepath)

    