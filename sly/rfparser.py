import re
from sly import Lexer, Parser
from robot.api import TestSuite

class SectionLexer(Lexer):
    tokens = {SETTING_HEADER, TEST_CASE_HEADER, DATA}

    SETTING_HEADER = r'(?i)\*+ ?settings? ?\**'
    TEST_CASE_HEADER = r'(?i)\*+ ?test cases? ?\**'
    DATA = r'.+'

    ignore_newline = r'\n+'

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')


class SectionParser(Parser):
    tokens = SectionLexer.tokens

    @_('sections section')
    def sections(self, p):
        name, data = p.section
        if name in p.sections:
            p.sections[name] += '\n' + data
        else:
            p.sections[name] = data
        return p.sections

    @_('section')
    def sections(self, p):
        name, data = p.section
        return {name: data}

    @_('SETTING_HEADER section_data')
    def section(self, p):
        return ('SETTING', p.section_data)

    @_('TEST_CASE_HEADER section_data')
    def section(self, p):
        return ('TESTCASE', p.section_data)

    @_('section_data DATA')
    def section_data(self, p):
        return p.section_data + '\n' + p.DATA

    @_('DATA')
    def section_data(self, p):
        return p.DATA


class SettingLexer(Lexer):
    parser_tokens = {SETTING_NAME, VALUE}
    tokens = parser_tokens.union({SEPARATOR, CONTINUATION})

    SEPARATOR = r' {2,}'
    SETTING_NAME = r'(?i)Library|Resource'
    CONTINUATION = r'(?m)^\.\.\.'
    VALUE = r'(\S+ )*\S+'

    ignore = '\n'


class SettingParser(Parser):
    tokens = SettingLexer.parser_tokens

    @_('settings')
    def setting_section(self, p):
        return p.settings

    @_('settings setting')
    def settings(self, p):
        return p.settings + [p.setting]

    @_('setting')
    def settings(self, p):
        return [p.setting]

    @_('SETTING_NAME arguments')
    def setting(self, p):
        return (p.SETTING_NAME, p.arguments)

    @_('arguments argument')
    def arguments(self, p):
        return p.arguments + [p.argument]

    @_('argument')
    def arguments(self, p):
        return [p.argument]

    @_('VALUE')
    def argument(self, p):
        return p.VALUE


class TestCaseLexer(Lexer):
    tokens = {NAME, SEPARATOR, KEYWORD, ARGUMENT, CONTINUATION, ASSIGNMENT}

    @_(r'^(\S+ )*\S+')
    def NAME(self, t):
        self._kw_seen = False
        return t

    CONTINUATION = r'(?m)^ {2,}\.\.\.'

    @_(r'(^ {2,})(?!\.\.\.)')
    def first_value(self, t):
        self._kw_seen = False
        t.type = 'SEPARATOR'
        return t

    @_(r'(\S+ )*\S+')
    def value(self, t):
        if self._kw_seen:
            t.type = 'ARGUMENT'
        elif re.match(r'\$\{.+\}( ?=)?', t.value):
            t.type = 'ASSIGNMENT'
        else:
            t.type = 'KEYWORD'
            self._kw_seen = True
        return t

    SEPARATOR = r' {2,}'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)


class TestCaseParser(Parser):
    tokens = {NAME, KEYWORD, ARGUMENT, ASSIGNMENT}

    @_('testcases')
    def testcase_section(self, p):
        return p.testcases

    @_('testcases testcase')
    def testcases(self, p):
        return p.testcases + [p.testcase]

    @_('testcase')
    def testcases(self, p):
        return [p.testcase]

    @_('NAME steps')
    def testcase(self, p):
        return (p.NAME, p.steps)

    @_('steps step')
    def steps(self, p):
        return p.steps + [p.step]

    @_('step')
    def steps(self, p):
        return [p.step]

    @_('KEYWORD')
    def step(self, p):
        return (None, p.KEYWORD, [])

    @_('KEYWORD arguments')
    def step(self, p):
        return (None, p.KEYWORD, p.arguments)

    @_('ASSIGNMENT KEYWORD arguments')
    def step(self, p):
        return (p.ASSIGNMENT, p.KEYWORD, p.arguments)

    @_('arguments argument')
    def arguments(self, p):
        return p.arguments + [p.argument]

    @_('argument')
    def arguments(self, p):
        return [p.argument]

    @_('ARGUMENT')
    def argument(self, p):
        return p.ARGUMENT
