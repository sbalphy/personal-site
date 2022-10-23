import anytree as Tree
from anytree.exporter import JsonExporter
from anytree.importer import JsonImporter

with open("files.json", "r+") as f:
    index = JsonImporter().read(f)

    # do stuff

    f.seek(0)
    f.truncate()
    JsonExporter(sort_keys=True).write(index, f)