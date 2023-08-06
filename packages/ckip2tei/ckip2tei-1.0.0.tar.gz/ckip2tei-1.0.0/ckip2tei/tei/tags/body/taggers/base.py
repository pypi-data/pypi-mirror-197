from abc import (
    ABC,
    abstractmethod,
)
import asyncio
from dataclasses import dataclass
import xml.etree.ElementTree as ET

from .cleaners import Cleaner

SegmentedSentences = list[list[tuple[str, str]]]
TagData = tuple[str, str] | list[tuple[str, str]] | dict[str, list[tuple[str, str]]]


@dataclass
class TeiTagger(ABC):
    """
    The TeiTagger object creats the tei tags.
    """

    tag: ET.Element
    data_cleaner: Cleaner

    @abstractmethod
    async def build_tag(self, tag_data: TagData):  # noqa
        pass

    async def build_tags(self, segmented_sentences: SegmentedSentences):
        tasks = []
        for segmented_sentence in segmented_sentences:
            task = asyncio.create_task(self.build_tag(segmented_sentence))
            tasks.append(task)

        return await asyncio.gather(*tasks)

    async def create(self):
        """The create method build TEI tags for each segmented sentence."""
        segmented_sentences = self.data_cleaner.clean()

        if not segmented_sentences:
            return None

        return await self.build_tags(segmented_sentences)
