from abc import (
    ABC,
    abstractmethod,
)


class Cleaner(ABC):
    """
    The Cleaner object cleans the segmented sentences output.
    """

    @abstractmethod
    def clean(self):
        pass
