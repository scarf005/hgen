#!/usr/bin/env python3

from dataclasses import dataclass, field
from pathlib import Path
from re import compile, Pattern, split
from typing import ClassVar, Callable
import re


@dataclass(frozen=True)
class Color:
    red = "\033[91m"
    green = "\033[92m"
    blue = "\033[94m"
    cyan = "\033[96m"
    white = "\033[97m"
    yellow = "\033[93m"
    magenta = "\033[95m"
    grey = "\033[90m"
    black = "\033[90m"
    default = "\033[99m"
    end = "\033[0m"

    @classmethod
    def cstr(cls, color: str, string: str):
        return f"{getattr(cls, color)}{string}{Color.end}"

    @classmethod
    def cprint(cls, color: str, string: str):
        print(cls.cstr(color, string))


def get_lines_from(file: Path) -> list[str]:
    return file.read_text().splitlines(keepends=False)


@dataclass
class Proto:
    file: Path
    func_def: ClassVar[Pattern] = compile(r"^(\w* ?)+\t(\w*)(?!main)\(.*\)$")
    header_style: str = field(init=False)

    prototypes: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.load_func_protos_from_file()
        self.header_style = f"// < {self.filename} >"

    def __len__(self) -> int:
        return len(self.prototypes)

    def __repr__(self) -> str:
        print(self.prototypes)
        return "\n".join([self.header_style, *self.prototypes, ""])

    def __str__(self) -> str:
        return "\n".join(
            [Color.cstr("magenta", self.header_style)]
            + [Proto.color_proto(p) for p in self.prototypes]
            + [""]
        )

    def load_func_protos_from_file(self):
        lines = iter(get_lines_from(self.file))
        Color.cprint("blue", f"reading: {self.filename}")
        for line in lines:
            if Proto.func_def.match(line) and next(lines) == "{":
                for incode in lines:
                    if incode == "}":
                        self.prototypes.append(f"{line};")
                        break

        self.prototypes = self.align_protos_indentation()
        self.prototypes.sort(key=len)

    def align_protos_indentation(self):
        def before_len(proto: str):
            return len(proto.split("\t")[0])

        longest = max(before_len(proto) for proto in self.prototypes)
        results = []
        for proto in self.prototypes:
            # print(before_len(proto), end=", ")
            to_pad = longest // 4 - before_len(proto) // 4 + 1
            types, name_params = proto.split("\t")
            results.append(types + "\t" * to_pad + name_params)
        # print(results)
        return results

    @property
    def filename(self) -> str:
        return self.file.name

    @staticmethod  # TODO: colors from clsmethod
    def color_proto(prototype: str):
        type, name, paramstr = re.split(r"\t+|\(", prototype[:-2])
        result = f'{Color.cstr("red", type)} {Color.cstr("magenta", name)}('
        params = iter(paramstr.split())
        for p in params:
            result += Color.cstr("red", p)
            ptr, name = re.split(r"(^\**)", next(params))[1:]
            result += f"{ptr} {Color.cstr('blue', name)} "
        return result[:-1] + ");"


curr = Proto(Path("lib/src/libft/ystrlen.c"))
print(repr(curr))
# print(curr.filename)
# print(len(curr))
# print(curr)
