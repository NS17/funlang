from dataclasses import dataclass
from typing import Sequence

from .tokenizer import TokenType, Token
from .errors import ParseError


@dataclass
class AST:
    pass


@dataclass
class General(AST):
    value: Token


@dataclass
class Function(AST):
    name: Token
    args: Sequence[General]
    body: 'Expression'


@dataclass
class FunctionCall(AST):
    name: Token
    args: Sequence


@dataclass
class Declaration(AST):
    letter: General
    declaration: 'Expression'


@dataclass
class Main(AST):
    functions: Sequence[Function]
    expression: 'Expression'


@dataclass
class Expression(AST):
    expression: AST
    declarations: Sequence[Declaration]


@dataclass
class BinOp(AST):
    left: AST
    right: AST
    op: TokenType


@dataclass
class UnaryOp(AST):
    argument: AST
    op: TokenType


@dataclass
class Conditional(AST):
    if_expression: AST
    if_condition: AST
    else_expression: AST


@dataclass
class Constant(AST):
    value: Token


class Parser:
    """
    Class that transforms tokens into AST structure
    """
    def __init__(self, tokens: list):
        self.tokens: Sequence[Token] = tokens
        self.index: int = 0
        self.state: int = 0

    def parse_main(self):
        """
        Entrypoint, parses Main into AST
        :return: AST
        """
        # parse and store functions
        functions = []
        while self.matches(TokenType.Function):
            functions.append(self.parse_function())

        # parse expression
        return Main(functions, self.parse_expression())

    def parse_expression(self):
        left = self.parse_conditional()
        self.state += 1

        # parse declarations
        declarations = []
        while self.matches(TokenType.Line):
            level = len(self.current.value)

            if level == self.state:
                self.advance()
                declarations.append(self.parse_declaration())

            elif level < self.state:
                break

            else:
                raise ParseError('Invalid declarations')

        self.state -= 1
        return Expression(left, declarations)

    def parse_conditional(self):
        expression = self.parse_logic()
        if self.matches(TokenType.If):
            self.advance()
            if_condition = self.parse_logic()
            if self.current.type is not TokenType.Else:
                raise ParseError('If statement without else statement')
            self.advance()
            else_expr = self.parse_logic()
            return Conditional(expression, if_condition, else_expr)

        return expression

    def parse_logic(self):
        return self.parse_standard('parse_arithmetic', TokenType.More, TokenType.Less, TokenType.SuperEqual)

    def parse_arithmetic(self):
        return self.parse_standard('parse_term', TokenType.Plus, TokenType.Minus)

    def parse_term(self):
        return self.parse_standard('parse_signed', TokenType.Multiply, TokenType.Divide)

    def parse_signed(self):
        if self.matches(TokenType.Plus, TokenType.Minus):
            token = self.consume()
            return UnaryOp(self.parse_factor(), token.type)

        return self.parse_factor()

    def parse_factor(self):
        left = self.parse_single()
        if self.matches(TokenType.Pow):
            token = self.consume()
            return BinOp(left, self.parse_signed(), token.type)
        return left

    def parse_single(self):
        token = self.current
        if token.type is TokenType.Number:
            self.advance()
            return Constant(token)

        if token.type is TokenType.Letter:
            # we found function call "func_name(...)"
            if self.next(TokenType.LeftBracket):
                return self.parse_function_call()

            # regular variable
            self.advance()
            return General(token)

        # parse brackets structure
        if token.type is TokenType.LeftBracket:
            self.advance()
            result = self.parse_expression()
            if self.current.type is not TokenType.RightBracket:
                raise ParseError('Invalid brackets')
            self.advance()
            return result
        raise ParseError(f'Invalid expression')

    def parse_function_call(self):
        name = self.consume()
        return FunctionCall(name, self.parse_args())

    def parse_declaration(self):
        letter = self.parse_single()
        if self.current.type is not TokenType.Equal:
            raise ParseError('Equal sign required in declaration')
        self.advance()
        return Declaration(letter, self.parse_expression())

    def parse_function(self):
        self.advance()
        name = self.consume()
        args = self.parse_args()

        if self.current.type is not TokenType.Colon:
            raise ParseError('Invalid function definition')
        self.advance()

        return Function(name, args, self.parse_expression())

    def parse_args(self):
        if self.current.type is not TokenType.LeftBracket:
            raise ParseError('Left bracket required in function definition')

        self.advance()
        args = []
        # parse function args
        while self.matches(TokenType.Letter, TokenType.Number):
            args.append(self.parse_single())

            if self.current.type is not TokenType.Comma:
                break
            self.advance()

        if self.current.type is not TokenType.RightBracket:
            raise ParseError('Right bracket required in function definition')
        self.advance()
        return args

    def parse_standard(self, method_name, *types):
        left = getattr(self, method_name)()
        while self.matches(*types):
            token = self.consume()
            left = BinOp(left, getattr(self, method_name)(), token.type)
        return left

    # utils

    @property
    def current(self):
        return self.tokens[self.index]

    def advance(self):
        self.index += 1

    def consume(self):
        current = self.current
        self.advance()
        return current

    def matches(self, *kind: TokenType):
        return self.index < len(self.tokens) and self.current.type in kind

    def next(self, *kind: TokenType):
        return self.index + 1 < len(self.tokens) and self.tokens[self.index + 1].type in kind
