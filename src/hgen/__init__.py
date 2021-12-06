#!/usr/bin/env python3

from pathlib import Path
from sys import argv

from hgen.injector import insert_prototypes
from hgen.proto import get_prototypes
from hgen.utils import cstr, visualize


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


def main():
    args = argv[1:]
    if len(args) != 3:
        print("Usage: hgen <common_path> <dest_path> <src_path>")
    common = Path(args[0])
    dest_path, src_path = common / args[1], common / args[2]

    visualize(dest_path, src_path)
    update_header_prototypes(dest_path, src_path)
