#!/usr/bin/env python3

import re
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path

from hgen.utils import RegexRules, cstr, get_lines_from
from termcolor import cprint

_NAME_HEADER = "/*\n** < {filename} > */"
_COLOR_HEADER = "magenta"
_COLOR_TYPE = "red"
_COLOR_VAR = "blue"


@dataclass
class Protos:
    """container for c function prototypes defined inside given source code."""

    file: Path
    prototypes: "list[str]" = field(default_factory=list)

    def __post_init__(self):
        self.load_func_protos_from_file()
        if not len(self.prototypes):
            raise ValueError(
                f"{cstr('yellow', self.file.name)} "
                f"{cstr('red',f'never had any BSD-style C function prototypes')}"
            )

    def is_line_func(self, line: str) -> bool:
        return (
            not any(line.startswith(char) for char in "#{")
            and not any(banned in line for banned in ["static", "main"])
            and RegexRules.FUNCTION.match(line) is not None
        )

    def load_func_protos_from_file(self):
        lines = iter(get_lines_from(self.file))
        for line in lines:
            if not self.is_line_func(line):
                continue
            if line.endswith("{"):
                collected = line.replace("{", "").strip().lstrip()
            else:
                collected = line
                for inparam in lines:
                    if inparam == "{":
                        break
                    elif "{" in inparam:
                        collected += inparam.replace("{", "").strip()
                        break
                    else:
                        collected += inparam.lstrip("\t")
            for inside_code in lines:
                if inside_code == "}":
                    break

            self.prototypes.append(f"{collected};")

    def __len__(self) -> int:
        return len(self.prototypes)

    def __repr__(self) -> str:
        return "\n".join([self.header, "", *self.prototypes])

    def __str__(self) -> str:
        return "\n".join(
            [cstr(_COLOR_HEADER, self.header)]
            + [p for p in self.prototypes]
            # + [Protos.colored_prototype(p) for p in self.prototypes]
            + [""]
        )

    def __getitem__(self, item):
        return self.prototypes[item]

    @cached_property
    def header(self):
        return _NAME_HEADER.format(filename=self.file.name)

    @staticmethod
    def colored_prototype(prototype: str):
        type, name, paramstr = re.split(r"\t+|\(", prototype[:-2])
        result = f'{cstr(_COLOR_TYPE, type)} {cstr("magenta", name)}('
        params = iter(paramstr.split())
        for param in params:
            result += cstr(_COLOR_TYPE, param)
            ptr, name = re.split(r"(^\**)", next(params))[1:]
            result += f" {ptr}{cstr(_COLOR_VAR, name)} "
        return result[:-1] + ");"
