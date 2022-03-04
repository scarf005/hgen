from configparser import ConfigParser
from pathlib import Path


def load_version():
    path = Path("setup.cfg")
    if not path.exists():
        path = Path("../setup.cfg")
    file = ConfigParser()
    file.read(path)
    return file["metadata"]["version"]


__version__ = load_version()
