import xml.etree.ElementTree as ET 
from email.utils import formatdate
from jinja2 import Template
import os
# Adds to an existing RSS feed and processes the feed into readable HTML.
# I'll edit this to make it more readable at some point, but it's very 101.
TEMPLATE_STRING = u"""
<h3 class="feed-title"><a href={{titlelink}}feed>{{title}}</a></h3>
<p class="feed-description">{{description}}</p>
{% for item in feed %}
<article class="feed-item">
    <h4>{{item["pubDate"]}}: <a href="{{item["link"]}}" rel="bookmark">{{item["title"]}}</a></h4>
    <p>{{item["description"]}}</p>
</article>
{% endfor %}
"""

def main():
    modified = input("Name of modified pages (no .html), include path (e.g. wiki/japao): \n").lower()
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

    feed = "../feed"
    tree = ET.parse(feed)
    root = tree.getroot()
    channel = root.find("./channel")
    channel.append(new_item)
    ET.indent(tree)

    tree.write(feed, encoding="UTF-8", xml_declaration=True)

    # generating html from rss 

    feed_template = Template(TEMPLATE_STRING)
    feed_info = {}
    feed_info[title] = channel.find("title").text
    feed_info[link] = channel.find("link").text
    feed_info[description] = channel.find("description").text
    feed_info[feed] = [{
        title: item.find("title").text,
        link: item.find("link").text,
        description: item.find("description").text,
        pubDate: parsedate(item.find("pubDate").text)
        }]

if __name__ == "__main__":
    main()