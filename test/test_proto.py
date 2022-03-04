from pathlib import Path

from hgen.proto import Protos
from termcolor import cprint


def test_protos():
    generated = repr(Protos(Path("test/given/01.c")))
    expected = Path("test/expected/01.c").read_text()

    print(generated)
    cprint(f"{generated=}", "yellow")
    cprint(f"{expected =}", "green")
    assert expected == generated
