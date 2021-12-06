from pathlib import Path

from hgen.utils import RegexRules, cprint, cstr, get_lines_from


def get_flag_span(lines: "list[str]") -> "tuple[int, int]":
    begin = None
    for i, line in enumerate(lines):
        if RegexRules.FLAG_BEGIN.match(line):
            begin = i
        elif begin and any(reg.match(line) for reg in RegexRules.FLAG_END):
            return begin, i
    raise SyntaxError(cstr("red", "function flag header was never found"))


def cut_lines_by_flag_span(lines: "list[str]", span: "tuple[int, int]"):
    return lines[: span[0] + 1], lines[span[1] :]


def try_insert(dest: Path, protos: "list[str]") -> bool:
    lines = get_lines_from(dest)
    try:
        before, after = cut_lines_by_flag_span(lines, get_flag_span(lines))
        dest.write_text("\n".join(before + protos + after))
        return True
        # break
    except SyntaxError:
        return False


def insert_prototypes(dest_path: Path, *, protos: "list[str]") -> None:
    def headererror():
        raise NotImplementedError(
            f"searched {dest_path.absolute()} but could not find "
            "neither header or function definition flags.\n"
            "a header in given directory should contain "
            f"{RegexRules.FLAG_BEGIN}"
        )

    if not dest_path.is_dir():
        oper_ok = try_insert(dest_path, protos)
        if oper_ok:
            return
        else:
            headererror()

    for dest in dest_path.glob("**/*.h"):
        print(dest)
        oper_ok = try_insert(dest, protos)
        if oper_ok:
            break
    else:
        headererror()
