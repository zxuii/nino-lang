from dataclasses import dataclass
from enum import Enum, auto
from pprint import pprint

class TokenType(Enum):
  # keyword
  LET = auto()          # let
  FUN = auto()          # fun
  PLUS = auto()         # +
  MINUS = auto()        # -
  MUL = auto()          # *
  DIV = auto()          # /
  EQUAL = auto()        # =
  LPAREN = auto()       # (
  RPAREN = auto()       # )
  LBRACE = auto()       # {
  RBRACE = auto()       # }

  IDENTIFIER = auto()   # ..

  # tipe data
  INT = auto()          # 1..9
  STRING = auto()       # ".."

@dataclass
class Token():
  ttype: TokenType
  value: str

  def __repr__(self):
    return f"Token({self.ttype}: '{self.value}')"

class Lexer():
  def __init__(self, code_str: str):
    self.code_str = code_str
    self.pos = 0
    self.ch = ''
    self.tokens = []

    self.advance()

  def advance(self):
    if (self.pos < len(self.code_str)):
      self.ch = self.code_str[self.pos]
      self.pos += 1
    else:
      self.ch = ''

  def clear_whitespace(self):
    while self.ch == ' ' or self.ch == '\n' or self.ch == '\t' or self.ch == '\r':
      self.advance()


  def tokenize(self):
    while self.ch != '':
      self.scan()

  def is_int(self) -> bool:
    return '0' <= self.ch <= '9'

  def parse_int(self):
    num = ''
    while self.is_int():
      num += self.ch
      self.advance()
    self.tokens.append(Token(TokenType.INT, num))

  def is_alpha(self) -> bool:
    return 'a' <= self.ch <= 'z' or 'A' <= self.ch <= 'Z' or self.ch == '_' 

  def get_ident(self):
    ident = ''
    while self.is_alpha():
      ident += self.ch
      self.advance()
    return ident

  def parse_keyword_or_ident(self):
    ident = self.get_ident()
    if self.ch == "let":
      self.tokens.append(Token(TokenType.LET, "let"))      
    if self.ch == "fun":
      self.tokens.append(Token(TokenType.FUN, "fun"))
    else:
      self.tokens.append(Token(TokenType.IDENTIFIER, ident))     
    self.advance()


  def scan(self):
    self.clear_whitespace()

    if self.ch == '+':
      self.tokens.append(Token(TokenType.PLUS, '+'))
      self.advance()
    elif self.ch == '-':
      self.tokens.append(Token(TokenType.MINUS, '-'))
      self.advance()
    elif self.ch == '*':
      self.tokens.append(Token(TokenType.MUL, '*'))
      self.advance()
    elif self.ch == '/':
      self.tokens.append(Token(TokenType.DIV, '/'))
      self.advance()
    elif self.ch == '=':
      self.tokens.append(Token(TokenType.EQUAL, '='))
      self.advance()
    elif self.ch == '(':
      self.tokens.append(Token(TokenType.LPAREN, '('))
      self.advance()
    elif self.ch == ')':
      self.tokens.append(Token(TokenType.RPAREN, ')'))
      self.advance()
    elif self.ch == '{':
      self.tokens.append(Token(TokenType.LBRACE, '{'))
      self.advance()
    elif self.ch == '}':
      self.tokens.append(Token(TokenType.RBRACE, '}'))
      self.advance()
    elif self.is_int():
      self.parse_int()
    elif self.ch == '"':
      str_ = ''
      self.advance()
      while self.ch != '"':
        str_ += self.ch
        self.advance()
      self.tokens.append(Token(TokenType.STRING, str_))
      self.advance()
    else:
      self.parse_keyword_or_ident()

def main():
  tokens = Lexer('let x = "test string if it work"')
  tokens.tokenize()
  pprint(tokens.tokens)

if __name__ == "__main__":
  main()
