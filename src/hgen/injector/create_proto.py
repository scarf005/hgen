from pathlib import Path

from hgen.proto import get_prototypes
from hgen.utils import visualize


def create_header_prototypes(
    sources: "list[Path]", common: Path, dest: Path
) -> "list[str]":
    prototypes: list[str] = []

    for src in sources:
        src_path = common / src
        try:
            # FIXME: single responsibility not satisfied
            visualize(dest, src_path)
            prototypes.extend(get_prototypes(src_path))
        except:
            pass

    return prototypes
