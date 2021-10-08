import os

from fashionscrapper.default_logger.defaultLogger import defaultLogger
from fashionscrapper.brand import parser_settings

CATEGORIES = [
    {"name": "schuhe", "includes": ["sneaker", "schuhe"], "excludes": ["edits/sneakers"]},
    {"name": "hose", "includes": ["short", "jeans", "rocke", "hose"], "excludes": []},
    {"name": "shirt", "includes": ["shirt", "hemd", "blazer"], "excludes": []},
    {"name": "pullover", "includes": ["pullover"], "excludes": []},
    {"name": "jacke", "includes": ["jacke", "mantel"], "excludes": []},
    {"name": "kleid", "includes": ["kleid"], "excludes": ["kleidung"]},
    {"name": "anzug", "includes": ["anzug", "overalls"], "excludes": []}
]

view_blacklist = ["Detail des Artikels 0",
                    "Detail des Artikels 6",
                    "Detail des Artikels 7",
                    "Detail des Artikels 8",
                    "Detail des Artikels 9",]

BASE_PATH = os.path.join(parser_settings.BASE_PATH, "mango")
THREADS = parser_settings.THREADS

FORCE_RESCAN = True
logger = defaultLogger("Mango")
