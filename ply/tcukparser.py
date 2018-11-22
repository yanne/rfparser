import re

from util import accumulate_to_list


class TCUKParser(object):
    tokens = ('NAME', 'SEPARATOR', 'KEYWORD', 'ARGUMENT', 'CONTINUATION', 'ASSIGNMENT', 'SETTING', 'SETTING_VALUE')
    t_ignore = '\n'

    def t_NAME(self, t):
        r'^(\S+\ )*\S+'
        self._kw_seen = False
        self._setting_seen = False
        return t

    t_ignore_CONTINUATION = r'(?m)^\ {2,}\.\.\.'

    def t_SETTING(self, t):
        r'\[Tags\]'
        self._setting_seen = True
        t.value = t.value[1:-1].lower()
        return t

    def t_first_value(self, t):
        r'(^\ {2,})(?!\.\.\.)'
        self._kw_seen = False
        self._setting_seen = False

    def t_value(self, t):
        r'(\S+\ )*\S+'
        if self._setting_seen:
            t.type = 'SETTING_VALUE'
            return t
        if self._kw_seen:
            t.type = 'ARGUMENT'
        elif re.match(r'\$\{.+\}( ?=)?', t.value):
            t.type = 'ASSIGNMENT'
        else:
            t.type = 'KEYWORD'
            self._kw_seen = True
        return t

    t_ignore_SEPARATOR = r'\ {2,}'

    def p_testcases(self, p):
        '''testcases : testcase
                    | testcases testcase'''
        accumulate_to_list(p)

    def p_testcase(self, p):
        '''testcase : NAME settings steps
                    | NAME steps'''
        if len(p) == 4:
            p[0] = (p[1], p[2], p[3])
        else:
            p[0] = (p[1], [], p[2])

    def p_settings(self, p):
        '''settings : setting
                    | settings setting'''
        accumulate_to_list(p)

    def p_setting(self, p):
        '''setting : SETTING setting_values'''
        p[0] = (p[1], p[2])

    def p_setting_values(self, p):
        '''setting_values : SETTING_VALUE
                          | setting_values SETTING_VALUE'''
        accumulate_to_list(p)

    def p_steps(self, p):
        '''steps : step
                 | steps step'''
        accumulate_to_list(p)

    def p_step(self, p):
        '''step : KEYWORD
                | KEYWORD arguments
                | ASSIGNMENT KEYWORD arguments'''
        if len(p) == 2:
            p[0] = (None, p[1], [])
        elif len(p) == 3:
            p[0] = (None, p[1], p[2])
        else:
            p[0] = (p[1], p[2], p[3])

    def p_arguments(self, p):
        '''arguments : ARGUMENT
                     | arguments ARGUMENT'''
        accumulate_to_list(p)


