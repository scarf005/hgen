#!/usr/bin/env python3

from argparse import Namespace
from pathlib import Path
from sys import argv, stderr

from hgen.injector import insert_prototypes
from hgen.proto import get_prototypes
from hgen.utils import create_parser, visualize


def update_header_prototypes(args: Namespace):
    prototypes: list[str] = []

    dest_path = args.common / args.includes

    for src in args.sources:
        try:
            src_path = args.common / src
            visualize(dest_path, src_path)
            prototypes.extend(get_prototypes(src_path))
        except:
            pass
    insert_prototypes(dest_path, protos=prototypes)


def main():
    parser = create_parser()
    if len(argv) == 1:
        parser.print_usage(stderr)
        exit()

    args = parser.parse_args()
    update_header_prototypes(args)
