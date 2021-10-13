#!/usr/bin/env python3

from dataclasses import dataclass, field
from pathlib import Path
import re
from colors import cprint, cstr
from utils import get_lines_from
from regexrules import RegexRules


@dataclass
class Proto:
    """container for c function prototypes defined inside source code."""

    file: Path
    header_style: str = field(init=False)

    prototypes: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.load_func_protos_from_file()
        assert len(self.prototypes), (
            f"{cstr('yellow', self.filename)} "
            f"{cstr('red',f'never had any BSD-style C function prototypes')}"
        )

        self.align_protos_indentation()
        self.prototypes.sort(key=len)

        self.header_style = f"// < {self.filename} >"

    def __len__(self) -> int:
        return len(self.prototypes)

    def __repr__(self) -> str:
        print(self.prototypes)
        return "\n".join([self.header_style, *self.prototypes, ""])

    def __str__(self) -> str:
        return "\n".join(
            [cstr("magenta", self.header_style)]
            + [Proto.color_proto(p) for p in self.prototypes]
            + [""]
        )

    def load_func_protos_from_file(self):
        lines = iter(get_lines_from(self.file))
        for line in lines:
            if (
                not any(banned in line for banned in ["static", "main"])
                and RegexRules.FUNCTION.match(line)
                and next(lines) == "{"
            ):
                for incode in lines:
                    if incode == "}":
                        self.prototypes.append(f"{line};")
                        break

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
        self.prototypes = results

    @property
    def filename(self) -> str:
        return self.file.name

    @staticmethod  # TODO: colors from clsmethod
    def color_proto(prototype: str):
        type, name, paramstr = re.split(r"\t+|\(", prototype[:-2])
        result = f'{cstr("red", type)} {cstr("magenta", name)}('
        params = iter(paramstr.split())
        for p in params:
            result += cstr("red", p)
            ptr, name = re.split(r"(^\**)", next(params))[1:]
            result += f"{ptr} {cstr('blue', name)} "
        return result[:-1] + ");"


if __name__ == "__main__":
    curr = Proto(Path("../so_long/lib/src/libft/ystrlen.c"))
    # print(repr(curr))
    # print(curr.filename)
    # print(len(curr))
    print(curr)
