import os
import importlib.metadata
from dotenv import load_dotenv

load_dotenv()

__version__ = importlib.metadata.version("kaptik")

DATA_SERVER_HOST = os.getenv("KAPTIK_SERVER_HOST", "localhost")
DATA_SERVER_PORT = os.getenv("KAPTIK_SERVER_PORT", 8822)