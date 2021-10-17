#!/usr/bin/env python3

from pathlib import Path
from sys import argv

from sources import get_prototypes
from headers import insert_prototypes


def update_header_prototypes(dest_path: Path, src_path: Path):
    """find and update c function prototypes with comment flags.

    Args:
        dest_path (Path): path to search for headers recursively
        src_path (Path): path to search for prototypes recursively
    """
    prototypes = get_prototypes(src_path)
    insert_prototypes(dest_path, protos=prototypes)


def main(dest_path=Path("includes"), src_path=Path("src"), common=None):
    if common:
        dest_path, src_path = Path(common) / dest_path, Path(common) / src_path
    update_header_prototypes(dest_path, src_path)


if __name__ == "__main__":
    main(*argv[1:])
