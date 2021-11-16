#!/usr/bin/env python3

from pathlib import Path
from sys import argv
from protogen import get_prototypes, insert_prototypes


def update_header_prototypes(dest_path: Path, src_path: Path):
    """find and update c function prototypes with comment flags.

    Args:
        dest_path (Path): path to search for headers recursively
        src_path (Path): path to search for prototypes recursively
    """
    try:
        prototypes = get_prototypes(src_path)
        insert_prototypes(dest_path, protos=prototypes)
    except ValueError as e:
        print(e)


def main(common="", dest="includes", src="src"):
    if common:
        dest_path, src_path = Path(common) / dest, Path(common) / src
    else:
        dest_path, src_path = Path(dest), Path(src)

    print(f"{src_path.resolve()} -> {dest_path.resolve()}")
    update_header_prototypes(dest_path, src_path)


if __name__ == "__main__":
    main(*argv[1:])
