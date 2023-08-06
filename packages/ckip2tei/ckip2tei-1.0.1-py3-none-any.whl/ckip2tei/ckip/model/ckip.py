from dataclasses import (
    dataclass,
    field,
)
from pathlib import Path
import pickle

from ckip2tei.config import (
    CKIP_DIR,
    CKIP_PATH,
    NLP_MODEL,
)


@dataclass(frozen=True, slots=True)
class CKIPClient:
    """
    The CKIPClient object connects to ckip drivers.
    """

    _ckip_path: str = field(init=False, default=CKIP_PATH)
    _nlp_model: str = field(init=False, default=NLP_MODEL)

    def __post_init__(self) -> None:
        self.on_ready()

    def on_ready(self) -> None:
        """The on_ready method initializes and caches the CKIP drivers."""
        has_path = Path(self._ckip_path).exists()

        if not has_path:
            from ckip_transformers.nlp import (
                CkipPosTagger,
                CkipWordSegmenter,
            )

            Path(CKIP_DIR).mkdir(parents=True, exist_ok=True)
            drivers = (
                CkipWordSegmenter(model=self._nlp_model),
                CkipPosTagger(model=self._nlp_model),
            )

            with open(rf"{self._ckip_path}", "wb") as file:
                pickle.dump(drivers, file)

    def connect(self) -> tuple:
        """The connect method connects to the ckip drivers.

        Returns:
            a tuple that contains CkipWordSegmenter and CkipPosTagger.
        """
        with open(self._ckip_path, "rb") as file:
            return pickle.load(file)
