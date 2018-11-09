# Prototypes for parsing Robot Framawork data

There are prototypes implemented using different parsing tools.
The goal is to parse `testdata/test.robot` and create a Robot Framework test suite
object from the parse tree.

For each prototype, there is a main program that shows how the parser can be used to
acheve the goal.

## Parsers

### sly/rfparser.py

Implemented using [Sly](https://github.com/dabeaz/sly)
To run the sly parser from the command line:
  `python sly/test.py testdata/test.robot`
