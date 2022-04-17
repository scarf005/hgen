from pathlib import Path

import tatsu
from tatsu.util import asjson

code = """\
int foo(struct stat * c, int a[][], char b[MACRO]) { }

void bar(){}
int baz(struct stat *st) { return 0;}

"""

grammar = Path("grammar.ebnf").read_text()

parser = tatsu.compile(grammar)

scope = """{aaa {aaa} aaa {a{a}a} aaa}"""

ast = parser.parse(code)
# ast = parser.parse(scope)
from pprint import pprint

pprint(asjson(ast))
