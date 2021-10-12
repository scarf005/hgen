#!/usr/bin/env python3

from dataclasses import dataclass, field
from pathlib import Path
from re import compile, Pattern, split
from typing import ClassVar, Callable
import re
import colors
from colors import cprint, cstr


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
            [colors.cstr("magenta", self.header_style)]
            + [Proto.color_proto(p) for p in self.prototypes]
            + [""]
        )

    def load_func_protos_from_file(self):
        lines = iter(get_lines_from(self.file))
        colors.cprint("blue", f"reading: {self.filename}")
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
        result = f'{colors.cstr("red", type)} {colors.cstr("magenta", name)}('
        params = iter(paramstr.split())
        for p in params:
            result += colors.cstr("red", p)
            ptr, name = re.split(r"(^\**)", next(params))[1:]
            result += f"{ptr} {colors.cstr('blue', name)} "
        return result[:-1] + ");"


if __name__ == "__main__":
    curr = Proto(Path("../so_long/lib/src/libft/ystrlen.c"))
    # print(repr(curr))
    # print(curr.filename)
    # print(len(curr))
    print(curr)
