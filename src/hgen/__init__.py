#!/usr/bin/env python3



from argparse import Namespace
from pathlib import Path
from sys import argv, stderr

from hgen.injector import create_header_prototypes, insert_prototypes
from hgen.utils import create_parser, visualize

def main():
    parser = create_parser()
    if len(argv) == 1:
        parser.print_usage(stderr)
        exit()

    args = parser.parse_args()
    dest_path = args.common / args.includes
    common_path = args.common

    prototypes: "list[str]" = create_header_prototypes(
        args.sources, common_path, dest_path
    )
    insert_prototypes(dest_path, protos=prototypes)
