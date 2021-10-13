#!/usr/bin/env python3

from pathlib import Path
from utils import get_lines_from
from sys import argv
from regexrules import RegexRules
from prototypes import Proto
from colors import cstr, cprint


def get_func_span(lines: list[str]) -> tuple[int, int]:
    begin = None
    for i, line in enumerate(lines):
        if RegexRules.FLAG_BEGIN.match(line):
            begin = i
        elif begin and any(reg.match(line) for reg in RegexRules.FLAG_END):
            return begin, i
    raise SyntaxError(cstr("red", "function flag header was never found"))


def insert_protos(dest_dir: Path, *, protos: list[str]) -> None:
    for dest in dest_dir.glob("**/*.h"):
        lines = get_lines_from(dest)
        try:
            span = get_func_span(lines)
            before, after = lines[: span[0] + 1], lines[span[1] :]
            dest.write_text("\n".join(before + protos + after))
            break
        except SyntaxError:
            pass
    else:
        raise NotImplementedError(
            'could not find either header or function definition flags'
            )
#
# ===== Sources =====

def crawl_prototypes(src_dir: Path):
    results: list[Proto] = []
    cprint('magenta', f'>> from {src_dir}')
    for src in src_dir.glob("**/*.c"):
        try:
            target = Proto(src)
            results.append(target)
            status, num = 'green', f'x{len(target)}'
        except:
            status, num = 'yellow', ''
        finally:
            print(f"{cstr(status, 'read')} {cstr('blue', src.name)} ({num})")
    assert len(results), cstr('red', f"no function prototypes found in this subdirectory(or file)")
    print(results)
    return results

def update_header_prototypes(dest_dir: Path, src_dir: Path):
    """find and update c function prototypes with comment flags.

    Args:
        dest_dir (Path): directory(or file) to search for headers recursively
        src_dir (Path): directory(or file) to search for prototypes recursively
    """
    ...
    prototypes = crawl_prototypes(src_dir)
    # insert_protos(dest_dir, protos = protos)


if __name__ == "__main__":
    match argv[1:]:
        case [dest, src_dir]:
            com = ""
        case [dest, src_dir, common]:
            com = argv[3]
        case _:
            # FIXME only for development
            update_header_prototypes(
                Path('../so_long/includes/lib'),
                Path('../so_long/lib/src'),
            )
            exit()
            # FIXME end fixme
            print("to use: ./protogen.py HEADER.h SRC DIRECTORY [Common]")
            exit()

    dest_dir, src_dir = (Path(com) / Path(argv[i]) for i in range(1, 3))
    update_header_prototypes(dest_dir, src_dir)