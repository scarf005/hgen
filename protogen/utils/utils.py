#!/usr/bin/env python3

from pathlib import Path


def get_lines_from(file: Path) -> 'list[str]':
    return file.read_text().splitlines(keepends=False)
