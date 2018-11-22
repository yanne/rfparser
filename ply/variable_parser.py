from ply import lex, yacc

from util import accumulate_to_list

tokens = ('VARIABLE_NAME', 'VALUE', 'SEPARATOR', 'CONTINUATION')

t_ignore_SEPARATOR = r'\ {2,}'
t_VARIABLE_NAME = r'(?m)^[$@&]\{.+\}(\ ?=)?'
t_ignore_CONTINUATION = r'(?m)^\.\.\.'
t_VALUE = r'(\S+\ )*\S+'

t_ignore = '\n'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

def p_variables(p):
    '''variables : variable
                | variables variable'''
    accumulate_to_list(p)

def p_setting(p):
    'variable : VARIABLE_NAME values'
    p[0] = (p[1], p[2])

def p_value(p):
    '''values : VALUE
              | values VALUE'''
    accumulate_to_list(p)

def p_error(e):
    print(e)

setting_parser = yacc.yacc()

def parse(data):
    return setting_parser.parse(data, lexer=lexer)
