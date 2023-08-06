from os import environ
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path("__file__").resolve().parent
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)

ckip_dir = environ.get("CKIP_DIR")
ckip_path = environ.get("CKIP_PATH")
nlp_model = environ.get("NLP_MODEL")

CKIP_DIR = PROJECT_ROOT / ".ckip" if ckip_dir is None else ckip_dir
CKIP_PATH = CKIP_DIR / "ckip_drivers.pickle" if ckip_path is None else ckip_path
NLP_MODEL = "bert-base" if nlp_model is None else nlp_model
