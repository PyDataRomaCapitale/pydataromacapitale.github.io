import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pelicanconf import *  # noqa: E402, F403

SITEURL = "https://pydataroma.python.it"
RELATIVE_URLS = False
