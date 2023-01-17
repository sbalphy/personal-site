# Manipula ou retorna a árvore salva, de acordo com o comando pedido.
# Não sei muito bem como é a etiqueta de input e output no python. Deve
# ter um jeito de refatorar isso.
# Usage: createpage.py command path/to/node (starting from index)
from anytree import Node, Resolver, PreOrderIter, ChildResolverError
from anytree.importer import JsonImporter
from anytree.exporter import JsonExporter
import sys
from itertools import zip_longest
from jinja2 import Environment, FileSystemLoader
import re

def addnode(resolve, root, path):
    path_parent, name_child = path.rsplit("/", 1)
    parent = resolve.get(root, path_parent)
    child = Node(name_child, parent=parent)
    print(f"Created node {child.name}")
    return

def removenode(resolve, root, path):
    target = resolve.get(root, path)
    target.parent = None
    print(f"Removed node {target.name}")
    return

def createpage(resolve, root, path):
    try:
        target = resolve.get(root, path)
    except ChildResolverError:
        print(f"Node {path} does not exist. Adding...")
        addnode(resolve, root, path)
        target = resolve.get(root, path)
    pathlist = path.split("/")
    filename = f"{target.name}.html"
    table = [[child.name for child in n.children] for n in target.path][1:]
    table = transpose(table)
    environment = Environment(loader=FileSystemLoader("templates/"), trim_blocks=True, lstrip_blocks=True)
    template = environment.get_template("template-fresh.html")
    content = template.render(
        name = target.name,
        path = path,
        table = table,
        pathlist = pathlist,
        children = [child.name for child in target.children]
    )
    with open(f"output/{filename}", mode="w", encoding="utf-8") as page:
        page.write(content)
    print(f"Page {filename} created.")
    print("The following pages must be updated:")
    for relative in [child for child in target.parent.children] + [target.parent]:
        print(f"    {relative.name}.html") 
    return


def updatepage(resolve, root, path):
    target = resolve.get(root, path)
    pathlist = path.split("/")
    filename = f"{target.name}.html"
    table = [[child.name for child in n.children] for n in target.path][1:]
    table = transpose(table)
    environment = Environment(loader=FileSystemLoader("templates/"), trim_blocks=True, lstrip_blocks=True)
    template = environment.get_template("template-renew.html")
    originalcontent = fetchcontent(f"../wiki/{filename}")
    content = template.render(
        name = target.name,
        path = path,
        table = table,
        pathlist = pathlist,
        children = [child.name for child in target.children],
        originalcontent = originalcontent
    )
    with open(f"output/{filename}", mode="w", encoding="utf-8") as page:
        page.write(content)
    print(f"Page {filename} updated.")
    return

def transpose(table):
    return [list(x) for x in zip_longest(*table)]

def fetchcontent(path):
    with open(path, mode="r", encoding="utf-8") as page:
        data = page.read() 
        regex = r"<!--content-->((.|\n)*?)<!--content-->"
        return re.search(regex, data).group(1)

def updateall(resolve, root):
    target = resolve.get(root, "index")
    for node in PreOrderIter(target):
        nodepath = "".join([f"{ancestor.name}/" for ancestor in node.ancestors[1:]] + [node.name])
        print(nodepath)
        updatepage(resolve, root, nodepath)
    print(f"Updated all pages.")

def updatedependents(resolve, root, path):
    target = resolve.get(root, path)
    updatepage(resolve, root, path)
    for childpath in [f"{path}/{child.name}" for child in target.children]:
        updatepage(resolve, root, childpath)
    print(f"Updated {path} and all its children.")

def main():
    command = sys.argv[1]
    try:
        path = sys.argv[2]
    except IndexError:
        path = None
        print("No path given. Hopefully you're running update-all.")
    with open("./files.json", "r+") as f:
        index = JsonImporter().read(f)
        resolve = Resolver()
        fakeroot = Node("fakeroot", children=[index])
        if command == "add":
            addnode(resolve, fakeroot, path)
        elif command == "remove":
            removenode(resolve, fakeroot, path)
        elif command == "create":
            createpage(resolve, fakeroot, path)
        elif command == "update":
            updatepage(resolve, fakeroot, path)
        elif command == "update-dependents":
            updatedependents(resolve, fakeroot, path)
        elif command == "update-all":
            updateall(resolve, fakeroot)
        else:
            print(f"Unidentified command {command}. Nothing has been updated.")
        fakeroot.children=[]
        f.seek(0)
        f.truncate()
        JsonExporter(sort_keys=True).write(index, f)

if __name__ == "__main__":
    main()