from ply import lex, yacc

from tcukparser import TCUKParser

class TestCaseLexer(TCUKParser):

    def __init__(self):
       self.lexer = lex.lex(module=self)
       self.parser = yacc.yacc(module=self)

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer)


def parse(data):
    t = TestCaseLexer()
    return t.parse(data)
