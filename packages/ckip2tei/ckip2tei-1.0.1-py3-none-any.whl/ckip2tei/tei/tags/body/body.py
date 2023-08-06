import asyncio
import xml.etree.ElementTree as ET

from ckip2tei.ckip import segment
from ckip2tei.tei.utils import filter_body

from .taggers import (
    BodyCleaner,
    BodyTagger,
    CommentsCleaner,
    CommentsTagger,
    TitleCleaner,
    TitleTagger,
)

# --------------------------------------------------------------------
# helper functions


async def create_title_task(text_tag: ET.Element, data: str, author: str):
    """The create_title_task function handles the title tag creation."""
    title_tag = ET.SubElement(text_tag, "title", author=author)
    sentence_tag = ET.SubElement(title_tag, "s")
    segmented_data = await segment(data)
    tagger = TitleTagger(sentence_tag, TitleCleaner(segmented_data))
    await tagger.create()


async def create_body_task(text_tag, data, author):
    """The create_body_task function handles the body tag creation."""
    body_tag = ET.SubElement(text_tag, "body", author=author)
    segmented_data = await segment(filter_body(data))
    tagger = BodyTagger(body_tag, BodyCleaner(segmented_data))
    await tagger.create()


async def create_comments_task(text_tag, data):
    """The create_comments_task function handles the comment tags creation."""
    segmented_data = await segment(data)
    tagger = CommentsTagger(text_tag, CommentsCleaner(segmented_data))
    await tagger.create()


# --------------------------------------------------------------------
# public interface


async def create_body_tags(root: ET.Element, content: tuple, author: str):
    title, body, comments = content
    text_tag = ET.SubElement(root, "text")

    title_task = asyncio.create_task(create_title_task(text_tag, title, author))
    body_task = asyncio.create_task(create_body_task(text_tag, body, author))
    comments_task = asyncio.create_task(create_comments_task(text_tag, comments))
    await asyncio.gather(title_task, body_task, comments_task)
