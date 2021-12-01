#!/usr/bin/env python3

from itertools import chain
from pathlib import Path

from hgen.utils import cprint, cstr

from .protos import Protos


def _crawl_prototypes(src_path: Path) -> "list[Protos]":
    results: list[Protos] = []
    cprint("magenta", f">> from {src_path}")
    for src in src_path.glob("**/*.c"):
        status, res = "green", ""
        try:
            target = Protos(src)
            results.append(target)
            res = f"(x{len(target)})"
        except ValueError:
            status, res = "yellow", "none"
        finally:
            print(f"{cstr(status, f'{res} in')} {cstr('blue', src.name)}")
    if not len(results):
        raise ValueError(
            cstr(
                "red",
                f"no function prototypes found in {src_path}",
            )
        )
    return results


def _align_protos_indentation(protolist: "list[Protos]"):
    def before_len(proto):
        return len(proto.split("\t")[0])

    def get_longest_prototype_len():
        result = 0
        for container in protolist:
            for proto in container:
                result = max(result, before_len(proto))

        return result + 4  # tabs

    longest = get_longest_prototype_len()

    for container in protolist:
        results = []
        for proto in container:
            to_pad = longest // 4 - before_len(proto) // 4 + 1
            types, name_params = proto.split("\t")
            results.append(types + "\t" * to_pad + name_params)

        container.prototypes = results


def _protolist_to_strlist(protolist: "list[Protos]") -> "list[str]":
    return [repr(s) for s in chain(protolist)]


def get_prototypes(src_path: Path) -> "list[str]":
    protolist = _crawl_prototypes(src_path)
    _align_protos_indentation(protolist)
    return _protolist_to_strlist(protolist)


if __name__ == "__main__":
    try:
        results = get_prototypes(Path("../so_long/src"))
    except ValueError as e:
        print(e, "\n====")
        print(get_prototypes(Path("../so_long/lib/src")))
