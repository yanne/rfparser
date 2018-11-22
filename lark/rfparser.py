import os

from lark import Lark
from lark.indenter import Indenter

def parse(data):
    with open(os.path.join(os.path.dirname(__file__), 'robot.lark')) as grammar:
        parser = Lark(grammar.read())

        tree = parser.parse(data)

        print(tree.pretty())
        return tree
