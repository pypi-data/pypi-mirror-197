import asyncio
import xml.etree.ElementTree as ET


async def create_metadata_tag(name: str, value: str, tei_header: ET.Element) -> None:
    """The create_metadata_tag function adds a new metadata tag to the given `tei_header`.

    Args:
        name (str): the name of the metadata tag to add
        value (str): the value of the metadata tag to add
        tei_header (xml.etree.ElementTree.Element): a tei header
    """
    ET.SubElement(tei_header, "metadata", name=name).text = value


async def create_header_tag(root: ET.Element, meta_data: dict[str, str]) -> None:
    """The create_header_tag function creates a set of metadata tags and adds
    them to the `tei_header`.

    Args:
        root (xml.etree.ElementTree.Element): the root element
        meta_data (dict): the metadata of a post
    """
    tei_header = ET.SubElement(root, "teiHeader")
    tasks = []

    for name, value in meta_data.items():
        task = asyncio.create_task(create_metadata_tag(name, value, tei_header))
        tasks.append(task)

    await asyncio.gather(*tasks)
