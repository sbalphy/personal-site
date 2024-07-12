import lxml.etree as ET
import lxml.html as HTML
from lxml.html import builder as E
from email.utils import formatdate, parsedate_to_datetime
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
    # TODO: make it print prettier html, check if limiting to 5 works
    page = HTML.parse("../about.html")
    about = page.getroot()
    feedsection = about.get_element_by_id("rss")
    for child in list(feedsection):
        feedsection.remove(child)
    xslt = ET.parse("rss-about-transformer.xsl")
    transform = ET.XSLT(xslt)
    transformed_feed = transform(tree).getroot()[0]
    transformed_feed_HTML = HTML.fromstring(ET.tostring(transformed_feed, pretty_print=True))
    for child in list(transformed_feed_HTML):
        feedsection.append(child)
        for timestamp in child.findall(".//time"):
            timestamp.text = parsedate_to_datetime(timestamp.text).strftime('%I:%M %p, %d %B %Y (%a)')
    output = ET.tostring(page, encoding="UTF-8", pretty_print=True)
    output = output.decode('utf8').replace('&#13;', '\r')
    with open("../about.html", "w") as f:
        f.write(output)
    
if __name__ == "__main__":
    main()