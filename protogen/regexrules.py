# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    regexrules.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: youkim < youkim@student.42seoul.kr>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/10/13 11:05:46 by youkim            #+#    #+#              #
#    Updated: 2021/11/26 13:07:23 by youkim           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/usr/bin/env python3

from functools import cached_property
from re import IGNORECASE, compile
from typing import Pattern


def _make_flagged_comment_regex(which):
    COMMENT_BEGIN = r"[/][/*][\t ]*={5,} *"
    COMMENT_END = r" *={5,}"
    return compile(fr"{COMMENT_BEGIN}{which}{COMMENT_END}", IGNORECASE)


class RegexRules:
    """Regex Rules to parse *.c and *.h files."""

    FUNCTION = compile(
        r"\b(?P<type>(\w* ?)+)\t(?P<name>[\w\*]*)(?P<param>\(.*\))"
    )
    FLAG_BEGIN = _make_flagged_comment_regex(r"@functions?")
    FLAG_END = [
        compile("#endif"),
        _make_flagged_comment_regex(r".*"),
    ]


if __name__ == "__main__":
    print(RegexRules.FUNCTION)
    print(RegexRules.FLAG_BEGIN)
