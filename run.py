#!/usr/bin/env python3

from pathlib import Path
from sys import argv

from hgen import get_prototypes, insert_prototypes
from hgen.utils import cprint, cstr


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


def visualize(dest_path: Path, src_path: Path):
    cols = {"d": "", "s": ""}
    for n, path in (("d", dest_path), ("s", src_path)):
        p = path.resolve()
        cols[n] += (
            cstr("cyan", f"{p.parent.parent.name}/")
            + cstr("yellow", f"{p.parent.name}/")
            + cstr("red", p.name)
        )
    print(f"{cols['s']} -> {cols['d']}")


def main(common="", dest="includes", src="src"):
    if common:
        dest_path, src_path = Path(common) / dest, Path(common) / src
    else:
        dest_path, src_path = Path(dest), Path(src)

    visualize(dest_path, src_path)
    update_header_prototypes(dest_path, src_path)


if __name__ == "__main__":
    main(*argv[1:])
