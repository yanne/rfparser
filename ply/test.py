import sys
import tempfile

from robot.api import TestSuite

import section_parser
import setting_parser
import variable_parser
import testcase_parser
import keyword_parser

def parse_sections(data):
    return section_parser.parse(data)

def build_settings(parsed_settings, suite):
    for name, data in parsed_settings:
        suite.resource.imports.create(type=name, name=data[0])
    return suite

def build_variables(parsed_variables, suite):
    for name, data in parsed_variables:
        suite.resource.variables.create(name, data)
    return suite

def build_tests(parsed_tests, suite):
    for name, settings, steps in parsed_tests:
        test = suite.tests.create(name=name)
        for name, value in settings:
            if name == 'tags':
                test.tags = value
        for assign, name, args in steps:
            if assign is not None:
                assign = [assign]
            else:
                assign = []
            test.keywords.create(name=name, assign=assign, args=args)
    return suite

def build_keywords(parsed_keywords, suite):
    for name, settings, steps in parsed_keywords:
        kw = suite.keywords.create(name=name)
        for name, value in settings:
            pass
        for assign, name, args in steps:
            if assign is not None:
                assign = [assign]
            else:
                assign = []
            kw.keywords.create(name=name, assign=assign, args=args)
    return suite


if __name__ == '__main__':
    data = open(sys.argv[1]).read()
    sections = parse_sections(data)
    parsed_settings = setting_parser.parse(sections['SETTING'])
    parsed_variables = variable_parser.parse(sections['VARIABLE'])
    parsed_tests = testcase_parser.parse(sections['TESTCASE'])
    parsed_kws = keyword_parser.parse(sections['KEYWORD'])
    print(parsed_kws)

    suite = TestSuite('test suite name')
    suite = build_settings(parsed_settings, suite)
    suite = build_variables(parsed_variables, suite)
    suite = build_tests(parsed_tests, suite)
    suite = build_keywords(parsed_kws, suite)
    suite.run(outputdir=tempfile.gettempdir(), log='log.html')
