# Manipula ou retorna a árvore salva, de acordo com o comando pedido.
# Não sei muito bem como é a etiqueta de input e output no python. Deve
# ter um jeito de refatorar isso.
from anytree import Node
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter
from anytree.resolver import Resolver
import sys
from tabulate import tabulate
from itertools import zip_longest
from jinja2 import Environment, FileSystemLoader

def addnode(resolve, root, path):
    path_parent, name_child = path.rsplit("/", 1)
    parent = resolve.get(root, path_parent)
    child = Node(name_child, parent=parent)
    return

def removenode(resolve, root, path):
    target = resolve.get(root, path)
    target.parent = None
    return

def createpage(resolve, root, path):
    environment = Environment(loader=FileSystemLoader("templates/"), trim_blocks=True, lstrip_blocks=True)
    template = environment.get_template("template.html")
    target = resolve.get(root, path)
    pathlist = path.split("/")
    filename = f"{target.name}.html"
    table = [[child.name for child in n.children] for n in target.path][1:]
    table = transpose(table)
    content = template.render(
        name = target.name,
        path = path,
        table = table,
        pathlist = pathlist,
        children = [child.name for child in target.children]
    )
    with open(filename, mode="w", encoding="utf-8") as page:
        page.write(content)
        print(f"Page {filename} created.")
    return

def transpose(table):
    return [list(x) for x in zip_longest(*table)]

def main():
    command = sys.argv[1]
    path = sys.argv[2]
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
        else:
            print(f"Unidentified command {command}. Nothing has been updated.")
        fakeroot.children=[]
        f.seek(0)
        f.truncate()
        JsonExporter(sort_keys=True).write(index, f)

if __name__ == "__main__":
    main()