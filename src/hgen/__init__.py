#!/usr/bin/env python3

from pathlib import Path
from sys import argv, stderr

from hgen.injector import insert_prototypes
from hgen.proto import get_prototypes
from hgen.utils import create_parser, visualize


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
    parser = create_parser()
    if len(argv) == 1:
        parser.print_usage(stderr)
        exit()

    args = parser.parse_args()

    dest_path = args.common / args.includes

    for src in args.sources:
        src_path = args.common / src
        visualize(dest_path, src_path)
        update_header_prototypes(dest_path, src_path)
