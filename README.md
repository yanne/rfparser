# Prototypes for parsing Robot Framawork data

There are prototypes implemented using different parsing tools.
The goal is to parse `testdata/test.robot` and create a Robot Framework test suite
object from the parse tree.

For each prototype, there is a main program that shows how the parser can be used to
acheve the goal.

## Parsers

### ply/rfparser.py

Implemented using [Ply](https://github.com/dabeaz/ply)
To run the ply parser from the command line:
  `python ply/test.py testdata/test.robot`

### sly/rfparser.py

Implemented using [Sly](https://github.com/dabeaz/sly)
To run the sly parser from the command line:
  `python sly/test.py testdata/test.robot`

### lark/rfparser.py

Implemented using [Lark](https://github.com/lark-parser/lark)
To run the lark parser from the command line:
  `python lark/test.py testdata/test.robot`
