import lark
import importlib.resources
from . import error

_data = importlib.resources.files("lexpr").joinpath("data")
GrammarFilename = str(_data.joinpath("lexpr.g"))

class Parser():

  def __init__(self):
    grammar_file = open(GrammarFilename)
    self.parser = lark.Lark(grammar_file)

  def parse(self, text):
    try:
      return self.parser.parse(text)
    except lark.exceptions.UnexpectedCharacters as e:
      errmsg = f"Invalid logic expression: {e}\n"
      errmsg += f"Invalid/unexpected character: {e.char}"
      raise error.LexprParserError(errmsg)
    except lark.exceptions.UnexpectedEOF as e:
      errmsg = f"Invalid logic expression: {e}\n"
      errmsg += "Invalid/unbalanced expression"
      raise error.LexprParserError(errmsg)
