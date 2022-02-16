#!/usr/bin/env python3

from re import IGNORECASE, compile


def _make_flagged_comment_regex(which):
    COMMENT_BEGIN = r"[/][/*].*"
    return compile(fr"{COMMENT_BEGIN}{which}", IGNORECASE)


class RegexRules:
    """Regex Rules to parse *.c and *.h files."""

    FUNCTION = compile(
        r"\b(?P<type>(\w* ?)+)\t(?P<name>[\w\*]*)(?P<param>\(.*\))"
    )
    FLAG_BEGIN = _make_flagged_comment_regex(r"@(func|functions?)\b")
    FLAG_END = [
        compile("#endif"),
        _make_flagged_comment_regex(r"=+.*=+"),
        _make_flagged_comment_regex(r"@end"),
    ]


if __name__ == "__main__":
    print(RegexRules.FUNCTION)
    print(RegexRules.FLAG_BEGIN)
