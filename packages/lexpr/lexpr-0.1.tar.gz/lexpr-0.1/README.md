# Lexpr: A simple logical expressions parser

Lexpr is a simple package containing a
logical expressions parser developed using a Lark grammar.

The expressions may contain:
- entity identifiers
- the binary operators ``|`` (or), ``&`` (and)
- the unary operator ``!`` (not).
- balanced pairs of round parentheses

## Installation

The package can be installed using ``pip install lexpr``.

## Usage

A parser is created and used for parsing the text, as in the
following example:
```
import lexpr
lp = lexpr.Parser()
lp.parse("(G1 & G2) | !G3")
#
# output:
#
#  Tree(
#    Token('RULE', 'start'),
#    [Tree(Token('RULE', 'entity'),
#      [Tree(Token('RULE', 'or_expr'),
#        [Tree(Token('RULE', 'entity'),
#          [Tree(Token('RULE', 'enclosed_expr'),
#            [Tree(Token('RULE', 'entity'),
#              [Tree(Token('RULE', 'and_expr'),
#                [Tree(Token('RULE', 'entity'), [Token('IDENTIFIER', 'G1')]),
#                 Tree(Token('RULE', 'entity'), [Token('IDENTIFIER', 'G2')])])]
#            )]
#          )]
#        ), Tree(Token('RULE', 'entity'),
#             [Tree(Token('RULE', 'not_expr'),
#               [Tree(Token('RULE', 'entity'), [Token('IDENTIFIER', 'G3')])]
#             )]
#           )]
#      )]
#    )]
#  )

```

In case of an invalid string is passed to the parser, an
exception is raised:
```
import lexpr
lp = lexpr.Parser()
lp.parse("G1 &")
# raises LexprParserError, unbalanced expression
lp.parse("G1 & G$")
# raises LexprParserError, invalid character in identifier
```

## Implementation

The grammar is contained in the file ``lexpr/data/lexpr.g``.
The parser is in the module ``lexpr/parser.py``.
Errors raised by the module are defined in ``lexpr/error.py``
and are instances of the class ``LexprError`` or its
subclasses.

## History

The package has been developed to support the parsing of the EGC format, for
expressing expectations about the contents of prokaryotic genomes. In this
format, groups of organisms can be combined using logical expressions of the
form parsed by this package. The main implementation of the format is based on
TextFormats, which, however does not support non-regular, indefinetly nested
expressions, such as the logical expressions parsed here. Thus the parsing of
this expressions has been developed separately in this package.

## Acknowledgements

This package has been created in context of the DFG project GO 3192/1-1
“Automated characterization of microbial genomes and metagenomes by collection
and verification of association rules”. The funders had no role in study
design, data collection and analysis.

