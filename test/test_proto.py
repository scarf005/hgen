from pathlib import Path

from hgen.proto import Protos
from termcolor import cprint


def test_protos():
    generated = repr(Protos(Path("test/c/test.c")))
    expected = Path("test/c/expected.c").read_text()

    print(generated)
    cprint(f"{generated=}", "yellow")
    cprint(f"{expected =}", "green")
    assert expected == generated
