from pathlib import Path 
import yaml
import xml.etree.ElementTree as ET

base_dir = Path(__file__).resolve().parent 

with (base_dir / "feed.yaml").open("r", encoding="utf-8") as file:
    yaml_data = yaml.safe_load(file) 

link_prefix = yaml_data["link"].rstrip("/")

rss = ET.Element(
    "rss",
    {
        "version":"2.0",
        "xmlns:itunes":"http://www.itunes.com/dtds/podcast-1.0.dtd", 
        "xmlns:content":"http://purl.org/rss/1.0/modules/content/",
    },
)

channel = ET.SubElement(rss, "channel")

ET.SubElement(channel, "title").text = yaml_data["title"]
ET.SubElement(channel, "link").text = link_prefix
ET.SubElement(channel, "description").text = yaml_data["description"]
ET.SubElement(channel, "language").text = yaml_data["language"]
ET.SubElement(channel, "itunes:author").text = yaml_data["author"]
ET.SubElement(channel, "itunes:subtitle").text = yaml_data["subtitle"]
ET.SubElement(channel, "itunes:image", {"href": link_prefix + yaml_data["image"]})
ET.SubElement(channel, "itunes:category", {"text":yaml_data["category"]})

for item in yaml_data.get("item", []): 
    item_element = ET.SubElement(channel, "item")
    ET.SubElement(item_element, "title").text = item["title"]
    ET.SubElement(item_element, "itunes:author").text = yaml_data["author"]
    ET.SubElement(item_element, "description").text = item["description"]
    ET.SubElement(item_element, "itunes:duration").text = item["duration"]
    ET.SubElement(item_element, "pubDate").text = item["published"] 

    ET.SubElement(
        item_element, 
        "enclosure", 
        {
            "url": link_prefix + item["file"],
            "type": "audio/mpeg",
            "length": item["length"]
        }, 
    )

tree = ET.ElementTree(rss)
tree.write(base_dir / "podcast.xml", encoding="UTF-8", xml_declaration=True) 
