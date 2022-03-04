from argparse import ArgumentParser
from pathlib import Path

from hgen._version import __version__

from .utils import cstr


def create_parser():
    prog = "hgen"
    parser = ArgumentParser(
        prog=prog,
        usage=f"{prog} [-hv] -I header.h src [src ...] [-c path]",
        description=cstr("green", "HGEN: Header prototype GENerator"),
    )
    parser.add_argument(
        "sources",
        nargs="+",
        type=Path,
        default=Path(".") / "src",
        help=(
            "list of source files to search for prototypes. "
            "either directory or file works"
        ),
        metavar="",
    )
    parser.add_argument(
        "-I",
        "--includes",
        type=Path,
        default=Path(".") / "includes",
        required=True,
        help="Path to header file",
        metavar="",
    )
    parser.add_argument(
        "-c",
        "--common",
        type=Path,
        default=Path(),
        help="Path shared by both src and dest",
        metavar="",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=__version__
    )

    # parser.add_argument(
    #     "-q",
    #     "--quiet",
    #     type=bool,
    #     default=False,
    #     help="Whether to suppress output (defualt:false)",
    #     metavar="",
    # )
    return parser


if __name__ == "__main__":
    from sys import argv

    argv.append("--version")
    parser = create_parser()
    args = parser.parse_args()
    print(args)
