import sys
import tempfile

from robot.api import TestSuite

from rfparser import SectionLexer, SectionParser, TestCaseLexer, TestCaseParser, SettingParser, SettingLexer


def filter_whitespace_tokens(tokens):
    return (t for t in tokens if t.type not in ['SEPARATOR', 'CONTINUATION'])

def parse_sections(data):
    lexer = SectionLexer()
    return SectionParser().parse(lexer.tokenize(data))

def parse_section(section_data, lexer, parser):
    return parser().parse(filter_whitespace_tokens(lexer().tokenize(section_data)))


def build_settings(parsed_settings, suite):
    for name, data in parsed_settings:
        setting = suite.resource.imports.create(type=name, name=data[0])
    return suite

def build_tests(parsed_tests, suite):
    for name, steps in parsed_tests:
        test = suite.tests.create(name=name)
        for assign, name, args in steps:
            if assign is not None:
                assign = [assign]
            else:
                assign = []
            test.keywords.create(name=name, assign=assign, args=args)
    return suite


if __name__ == '__main__':
    data = open(sys.argv[1]).read()
    sections = parse_sections(data)
    parsed_settings = parse_section(sections['SETTING'], SettingLexer, SettingParser)
    parsed_tests = parse_section(sections['TESTCASE'], TestCaseLexer, TestCaseParser)

    suite = build_tests(parsed_tests,
        build_settings(parsed_settings, TestSuite('test suite name'))
    )
    suite.run(outputdir=tempfile.gettempdir())
