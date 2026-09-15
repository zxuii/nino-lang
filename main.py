from dataclasses import dataclass
from enum import Enum, auto
from pprint import pprint
import sys

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

  # special
  EOF = auto()          # end of file

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

    self.tokens.append(Token(TokenType.EOF, "end of file"))

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
    if ident == "let":
      self.tokens.append(Token(TokenType.LET, "let"))      
    elif ident == "fun":
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


# EXPRESSION

@dataclass
class Node:
  pass

@dataclass
class Program(Node):
  block: Node

@dataclass
class UnaryOp(Node):
  op: Token
  value: Node

@dataclass
class BinOp(Node):
  left: Node
  op: Token
  right: Node

@dataclass
class IntLit(Node):
  value: int

@dataclass
class StringLit(Node):
  value: str

class Parser():
  def __init__(self, tokens):
    self.tokens = tokens
    self.ct = None
    self.pos = 0

    self.advance()

  def is_at_end(self):
    return self.ct and self.ct.ttype == TokenType.EOF

  def consume(self, ty):
    if self.ct and self.ct.ttype == ty:
      self.advance()
    else:
      print("eror pokoknya")

  def advance(self):
    if not self.is_at_end():
      self.ct = self.tokens[self.pos]
      self.pos += 1
    else:
      self.ct = None

  def parse_expr(self):
    return self.parse_additive()

  def parse_additive(self):
    expr = self.parse_term()

    if self.ct.ttype == TokenType.PLUS:
      self.consume(TokenType.PLUS)
      return BinOp(expr, self.ct.ttype, self.parse_term())
    elif self.ct.ttype == TokenType.MINUS:
      self.consume(TokenType.MINUS)
      return BinOp(expr, self.ct.ttype, self.parse_term())

    return expr
    
  def parse_term(self):
    expr = self.parse_factor()
    # print(node)
    while self.ct and self.ct.ttype in [TokenType.MUL, TokenType.DIV]:
      tok = self.ct
      if tok.ttype == TokenType.MUL:
          self.consume(TokenType.MUL)
      elif tok.ttype == TokenType.DIV:
          self.consume(TokenType.DIV)

      expr = BinOp(expr, tok, self.parse_factor())
    return expr

  def parse_factor(self):
    expr = self.parse_primary()
    # print(node)
    while self.ct and self.ct.ttype in [TokenType.PLUS, TokenType.MINUS]:
        tok = self.ct
        if tok.ttype == TokenType.PLUS:
            self.consume(TokenType.PLUS)
        elif tok.ttype == TokenType.MINUS:
            self.consume(TokenType.MINUS)

        expr = BinOp(expr, tok, self.parse_primary())
    return expr

  def parse_primary(self):
    tok = self.ct
    if tok.ttype == TokenType.LPAREN:
      self.consume(TokenType.LPAREN)
      node = self.parse_expr()
      self.consume(TokenType.RPAREN)
      return node
    elif tok.ttype == TokenType.INT:
      self.consume(TokenType.INT)
      return IntLit(tok)
    elif tok.ttype == TokenType.STRING:
      self.consume(TokenType.STRING)
      return StringLit(tok)
    else:
      raise SyntaxError(f"unexpected token {tok}")

def run():
  if len(sys.argv) > 1:
    f = open(sys.argv[1], "r")
    code = f.read()
    lexer = Lexer(code)
    lexer.tokenize()
    parser = Parser(lexer.tokens)
    return parser.parse_expr()
  else:
    print("Usage: nino <file.nino>")

def main():
  tokens = run()
  pprint(tokens)

if __name__ == "__main__":
  main()
