from dataclasses import dataclass

from .base import Cleaner

SegmentedSentences = list[list[tuple[str, str]]]


@dataclass(slots=True)
class TitleCleaner(Cleaner):
    """
    The TitleCleaner object cleans the title data output.
    """

    segmented_sentences: SegmentedSentences

    def clean(self):
        if self.segmented_sentences[0][0][0].startswith("http"):
            return ""

        return self.segmented_sentences[0]


@dataclass(slots=True)
class BodyCleaner(Cleaner):
    """
    The BodyDataCleaner object cleans the body data output.
    """

    segmented_sentences: SegmentedSentences

    def clean(self):
        if not self.segmented_sentences:
            return ""

        return self.segmented_sentences


@dataclass(slots=True)
class CommentsCleaner(Cleaner):
    """
    The CommentsCleaner object cleans the comments data output.
    """

    segmented_sentences: SegmentedSentences

    def clean(self):
        if not self.segmented_sentences:
            return ""

        return self.segmented_sentences
