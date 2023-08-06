import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

from .base import TeiTagger


class TitleTagger(TeiTagger):
    """
    The TitleTagger object creats the tei tags for the post title.
    """

    async def build_tag(self, tag_data: tuple[str, str]) -> None:
        word, pos = tag_data
        ET.SubElement(self.tag, "w", type=pos).text = escape(word)


class BodyTagger(TeiTagger):
    """
    The BodyTagger object creats the tei tags for the post body.
    """

    async def build_tag(self, tag_data: list[tuple[str, str]]) -> None:
        sentence_tag = ET.SubElement(self.tag, "s")
        for word, pos in tag_data:
            ET.SubElement(sentence_tag, "w", type=pos).text = escape(word)


class CommentsTagger(TeiTagger):
    """
    The CommentsTagger object creats the tei tags for the post comments.
    """

    async def build_tag(self, tag_data: dict[str, list[tuple[str, str]]]):
        comments = tag_data.get("content")

        if not comments:
            return None

        author = tag_data.get("author", "匿名")
        comment_type = tag_data.get("type")
        comment_tag = ET.SubElement(
            self.tag, "comment", author=author, c_type=comment_type
        )
        sentence_tag = ET.SubElement(comment_tag, "s")

        for ws_pos_pair in comments[0]:
            word, pos = ws_pos_pair
            ET.SubElement(sentence_tag, "w", type=pos).text = escape(word)
