#import xml.etree.ElementTree as ET
import lxml.etree as ET
import lxml.html as HTML
from lxml.html import builder as E
from email.utils import formatdate
import os
# Adds to an existing RSS feed and processes the feed into readable HTML.
# I'll edit this to make it more readable at some point, but it's very 101.

def main():
    feed = "../feed"
    tree = ET.parse(feed)
    modified = input("Name of modified pages (no .html), include path (e.g. wiki/japao): \n").lower()
    if modified != "":
        path = f"../{modified}.html"
        if not os.path.isfile(path):
            print(f"File {path} not found.\n")
            return
        title = ET.Element("title")
        title.text = input("Title of the update: \n")
        link = ET.Element("link")
        link.text = f"https://wiki.cecm.usp.br/~sunny/{modified}.html"
        description = ET.Element("description")
        description.text = input("Description of the update (content of modification): \n")
        pubDate = ET.Element("pubDate")
        pubDate.text = formatdate()

        new_item = ET.Element("item")
        new_item.extend((title, link, description, pubDate))

        root = tree.getroot()
        channel = root.find("./channel")
        channel.append(new_item)
        ET.indent(tree)

        tree.write(feed, encoding="UTF-8", xml_declaration=True)

    # generating html from rss 

    page = HTML.parse("../about.html")
    about = page.getroot()
    feedsection = about.get_element_by_id("rss")
    xslt = ET.parse("rss-about-transformer.xsl")
    transform = ET.XSLT(xslt)
    newdom = transform(tree).getroot()
    feedsection.append(newdom[0])
    page.write("../test.html", encoding="UTF-8", xml_declaration=True)
if __name__ == "__main__":
    main()