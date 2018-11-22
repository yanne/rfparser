from ply import lex, yacc

from tcukparser import TCUKParser

class KeywordParser(TCUKParser):

    def __init__(self):
       self.lexer = lex.lex(module=self)
       self.parser = yacc.yacc(module=self)

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer)


def parse(data):
    return KeywordParser().parse(data)

