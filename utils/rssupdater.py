import xml.etree.ElementTree as ET 
from email.utils import formatdate
import os
def main():
    modified = input("Name of modified pages (no .html), include path (e.g. wiki/japao): \n").lower()
    path = f"../{modified}.html"
    if not os.path.isfile(path):
        print(f"File {path} not found.\n")
        return
    title = ET.Element("title")
    title.text = input("Title of the update: \n")
    link = ET.Element("link")
    link.text = f"https://wiki.cecm.usp.br/~sunny/wiki/{modified}.html"
    description = ET.Element("description")
    description.text = input("Description of the update (content of modification): \n")
    pubDate = ET.Element("pubDate")
    pubDate.text = formatdate()

    new_item = ET.Element("item")
    new_item.extend((title, link, description, pubDate))

    feed = "../feed"
    tree = ET.parse(feed)
    root = tree.getroot()
    channel = root.find("./channel")
    channel.append(new_item)
    ET.indent(tree)

    tree.write(feed)


if __name__ == "__main__":
    main()