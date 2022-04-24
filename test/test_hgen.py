from pathlib import Path

from hgen.injector import create_header_prototypes, insert_prototypes
from hgen.proto import Protos, get_prototypes

from termcolor import cprint


def test_protos():
    generated = repr(Protos(Path("test/given/01.c")))
    expected = Path("test/expected/01.c").read_text()

    print(generated)
    cprint(f"{generated=}", "yellow")
    cprint(f"{expected =}", "green")
    assert expected == generated


# def test_conversion():
#     generated = Path("test/given/02.h").read_text()
#     expected = Path("test/expected/02.h").read_text()
#     result = create_header_prototypes(
#         sources=[Path("02.c")],
#         common=Path("test/given"),
#         dest=Path("02.h"),
#     )
#     print(result)
#     assert expected == generated


# if __name__ == "__main__":
#     test_conversion()
