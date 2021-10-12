#!/usr/bin/env python3

from pathlib import Path
from sys import argv
from re import compile, IGNORECASE
from dataclasses import dataclass

# ===== Terminal Output =====


@dataclass(frozen=True)
class Clr:
    M = "\033[95m"
    B = "\033[94m"
    C = "\033[96m"
    G = "\033[92m"
    Y = "\033[93m"
    R = "\033[91m"
    B = "\033[1m"
    U = "\033[4m"
    END = "\033[0m"

    @classmethod
    def color_str(cls, color, string):
        return f"{getattr(cls, color)}{string}{Clr.END}"

    @classmethod
    def cprint(cls, color, string):
        print(cls.color_str(color, string))

# ===== Regexes =====


def formatted_comment(which):
    return compile(fr"[/][/*] *={{5,}} *{which} *={{5,}}", IGNORECASE)


@dataclass(frozen=True)
class Regex:
    func_begin = formatted_comment(r"functions?")
    func_end = [compile("#endif"), formatted_comment(r".*")]
    func_def = compile(r"(\w*)\t(\w*)(?!main)\(.*\)")


# ===== Utils & Prototype Dataclass =====


def get_lines_from(file: Path) -> list[str]:
    return file.read_text().splitlines(keepends=False)

@dataclass
class Protos:

    ...

# ===== Headers =====


def get_func_span(lines: list[str]) -> tuple[int, int]:
    begin = None
    for i, line in enumerate(lines):
        if Regex.func_begin.match(line):
            begin = i
        elif begin and any(reg.match(line) for reg in Regex.func_end):
            return begin, i
    raise SyntaxError(
        Clr.color_str("R", "// ===== Functions ===== flag were never found")
    )


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


# ===== Sources =====


def get_func_protos_in_file(file: Path) -> list[str]:
    results, lines = [], iter(get_lines_from(file))
    print(f"reading: {file.name}")
    for line in lines:
        if Regex.func_def.match(line) and next(lines) == "{":
            for inside in lines:
                if inside == "}":
                    results.append(f"{line};")
                    break
    return results

def create_protos(src_dir: Path) -> list[str]:
    results = []
    counter = {'sources': 0, 'prototypes': 0}
    for src in src_dir.glob("**/*.c"):
        file_protos = [f'\n// {src.name}']
        file_protos.extend(sorted(get_func_protos_in_file(src)))
        if len(file_protos):
            counter['sources'] += 1
            counter['prototypes'] += len(file_protos) - 1
            results.extend(file_protos)
    results.append('')

    if counter['prototypes'] > 0:
        Clr.cprint(
            "G",
            f"found {counter['prototypes']} prototypes "
            f"in {counter['sources']} sources"
        )
    else:
        Clr.cprint("Y", f"no prototypes found in {counter['sources']} sources")
    return results


# ===== Main =====


def main(dest_dir: Path, src_dir: Path):
    protos = create_protos(src_dir)

    insert_protos(dest_dir, protos = protos)


if __name__ == "__main__":
    match argv[1:]:
        case [dest, src_dir]:
            com = ""
        case [dest, src_dir, common]:
            com = argv[3]
        case _:
            print("to use: ./protogen.py HEADER.h SRC DIRECTORY [Common]")
            exit()

    dest, src_dir = (Path(com) / Path(argv[i]) for i in range(1, 3))
    main(dest, src_dir)
