import enum
import operator
from typing import NamedTuple

from .errors import TokenizationError


class TokenType(enum.Enum):
    """
    Class that contains possible types of the tokens
    """
    Number = enum.auto()
    Plus = '+', operator.add, operator.pos
    Minus = '-', operator.sub, operator.neg
    Multiply = '*', operator.mul
    Divide = '/', operator.truediv
    Pow = '**', operator.pow

    LeftBracket = '(',
    RightBracket = ')',

    Letter = enum.auto()
    Line = enum.auto()

    Equal = '=',
    Less = '<', operator.le
    More = '>', operator.gt
    SuperEqual = '==', operator.eq
    If = 'if',
    Else = 'else',
    Function = 'fun',
    Colon = ':',
    Comma = ',',


class Token(NamedTuple):
    type: TokenType
    value: str


types_unq_dict = {x.value[0]: Token(x, x.value) for x in TokenType if
                  x not in [TokenType.Number, TokenType.Letter, TokenType.Line]}


def parse_string(s: str):
    """
    Transforms string into tokens
    :param s: input string
    :return: tokens
    """
    s = list(s)

    while s:
        element = s.pop(0)

        if element.isdigit():
            yield from read_continuous(element, s, lambda x: x.isdigit(), TokenType.Number)

        elif element.isalpha():
            yield from read_continuous(element, s, lambda x: x.isalpha(), TokenType.Letter)

        elif element == '|':
            yield from read_continuous(element, s, lambda x: x == '|', TokenType.Line)

        elif element == '*' and s and s[0] == '*':
            s.pop(0)
            yield types_unq_dict['**']

        elif element == '=' and s and s[0] == '=':
            s.pop(0)
            yield types_unq_dict['==']

        elif element in types_unq_dict:
            yield types_unq_dict[element]

        elif element in [' ', '\n']:
            continue

        else:
            raise TokenizationError(f'Unknown symbol {element}')


def read_continuous(element, s, compare, token_type):
    last = [element]

    while s and compare(s[0]):
        last.append(s.pop(0))

    element = ''.join(last)

    if element in types_unq_dict:
        yield types_unq_dict[element]
        return

    yield Token(token_type, element)
