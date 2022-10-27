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
from html import escape

def main():
    command = sys.argv[1]
    path = sys.argv[2]
    with open("./files.json", "r+") as f:
        index = JsonImporter().read(f)
        r = Resolver()
        fakeroot = Node("fakeroot", children=[index])
        if command == "add":
            path_parent, name_child = path.rsplit("/", 1)
            parent = r.get(fakeroot, path_parent)
            child = Node(name_child, parent=parent)
        elif command == "remove":
            target = r.get(fakeroot, path)
            target.parent = None
        elif command == "table":
            target = r.get(fakeroot, path)
            table = [[f"<a href=\"./{child.name}.html\">{child.name}</a>" for child in n.children] for n in target.path][1:]
            table = [list(x) for x in zip_longest(*table)]
            print("/".join([n.name for n in target.path[1:]]))
            print(tabulate(table, tablefmt="unsafehtml", colalign=None))
        else:
            print(f"Unidentified command {command}. Nothing has been updated.")
        fakeroot.children=[]
        f.seek(0)
        f.truncate()
        JsonExporter(sort_keys=True).write(index, f)

if __name__ == "__main__":
    main()