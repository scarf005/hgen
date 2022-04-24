#!/usr/bin/env python3

import re
from itertools import chain
from pathlib import Path

from hgen.proto import Protos
from hgen.utils import TAB, cprint, cstr
from hgen.utils.regexrules import RegexRules


def crawl_prototypes(src_path: Path) -> "list[Protos]":
    def crawl_file(src: Path):
        status, res = "green", ""
        try:
            target = Protos(src)
            res = f"(x{len(target)})"
            # return target
            results.append(target)
        except ValueError:
            status, res = "yellow", "none"
        finally:
            print(f"{cstr(status, f'{res} in')} {cstr('blue', src.name)}")

    def checked(results: "list[Protos]"):
        if not len(results):
            raise ValueError(
                cstr(
                    "red",
                    f"no function prototypes found in {src_path}",
                )
            )
        return results

    results: list[Protos] = []
    cprint("magenta", f">> from {src_path}")

    if not src_path.is_dir():
        crawl_file(src_path)
        return checked(results)

    for src in sorted(src_path.glob("*.c")):
        crawl_file(src)

    return checked(results)


# this is the dirtiest loop i've ever laid my hands on.
# but it works.
def align_protos_indentation(protolist: "list[Protos]"):
    def get_types_and_params(proto: str) -> "tuple[str, str]":
        types, funcname_params = re.findall(RegexRules.FUNCTION_SPLIT, proto)[
            0
        ]
        return types.strip(" \t"), funcname_params

    def get_funcname_and_params(
        funcname_params: str,
    ) -> "tuple[str, list[str]]":
        try:
            funcname, param = funcname_params.split("(")
            params = [p.strip() for p in param.split(",")]

            return funcname, params
        except ValueError as e:
            raise ValueError(
                cstr("red", f'{e} while splitting "{funcname_params}"')
            )

    def before_len(proto: str) -> int:
        types = get_types_and_params(proto)[0]
        return len(types)
        # return len(proto.split(TAB)[0])

    def get_longest_prototype_len(protolist: "list[Protos]"):
        result = 0
        for container in protolist:
            for proto in container:
                result = max(result, before_len(proto))
        return result + 4  # tabs

    def in_loop():
        types, funcname_params = get_types_and_params(proto)
        funcname, params = get_funcname_and_params(funcname_params)
        # print(f"{types = }, {funcname_params = }")
        # print(f"{funcname = }, {param = }")
        # print(f"{longest = }")
        to_pad = longest // 4 - before_len(proto) // 4
        nl_tabs = TAB * (1 + before_len(proto) // 4 + to_pad)
        # print(before_len(proto), nl_tabs)
        result = [f"{types}{TAB * to_pad}{funcname}("]
        # print(result)
        i = 0
        while i < 100:
            is_first = True
            while (
                len(params)
                and len(result[i].replace(TAB, "....") + params[0]) < 79
            ):
                if is_first:
                    is_first = False
                else:
                    result[i] += " "
                result[i] += params.pop(0)
                if len(params):
                    result[i] += ","
            i += 1
            if len(params):
                result.append(nl_tabs)
            else:
                break
        else:
            raise ValueError(
                cstr(
                    "red",
                    f"{len(params)} params left after {i} iterations",
                )
            )
        return result

    cprint("red", "start")
    longest = get_longest_prototype_len(protolist)

    for container in protolist:
        # print(container)
        results = []
        for proto in container:
            result = in_loop()
            results.append("\n".join(result))

        container.prototypes = results


def protolist_to_strlist(protolist: "list[Protos]") -> "list[str]":
    return [repr(s) for s in chain(protolist)]


def get_prototypes(src_path: Path) -> "list[str]":
    protolist = crawl_prototypes(src_path)
    align_protos_indentation(protolist)
    return protolist_to_strlist(protolist)


if __name__ == "__main__":
    try:
        results = get_prototypes(Path("../so_long/src"))
    except ValueError as e:
        print(e, "\n====")
        print(get_prototypes(Path("../so_long/lib/src")))
