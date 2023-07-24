from dataclasses import dataclass
from enum import Enum


class Type(str, Enum):
    EOL = "EOL"
    NUMBER = "NUMBER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULT = "MULT"
    DIV = "DIV"
    WSPACE = "WSPACE"

    @classmethod
    def detect_type(cls, character: str):
        if character.isdigit():
            return cls.NUMBER
        elif character.isspace():
            return cls.WSPACE
        elif character == "+":
            return cls.PLUS
        elif character == "-":
            return cls.MINUS
        elif character == "*":
            return cls.MULT
        elif character == "/":
            return cls.DIV


@dataclass
class Token:
    value: str
    type: Type


class Interpreter:
    def __init__(self, arthmetic_expression: str) -> None:
        self.expr = arthmetic_expression
        self.tokens: list[Token] = []
        self.current_character: str = None
        self.position: int = 0
        self.current_token: Token = None
        self.digits_buffer: list[str] = []

    def __consume_digits_buffer(
        self,
    ):
        if self.digits_buffer:
            self.tokens.append(
                Token(value="".join(self.digits_buffer), type=Type.NUMBER)
            )
            self.digits_buffer = []

    def lexical_parsing(self):
        for position, character in enumerate(self.expr):
            match Type.detect_type(character):
                case Type.WSPACE:
                    self.__consume_digits_buffer()
                    continue
                case Type.NUMBER:
                    self.digits_buffer.append(character)
                case Type.DIV:
                    self.__consume_digits_buffer()
                    self.tokens.append(Token(value=character, type=Type.DIV))
                case Type.MULT:
                    self.__consume_digits_buffer()
                    self.tokens.append(Token(value=character, type=Type.MULT))
                case Type.MINUS:
                    self.__consume_digits_buffer()
                    self.tokens.append(Token(value=character, type=Type.MINUS))
                case Type.PLUS:
                    self.__consume_digits_buffer()
                    self.tokens.append(Token(value=character, type=Type.PLUS))
                case _:
                    self.__consume_digits_buffer()
                    raise Exception("unsuported case")

    def __str__(self):
        return f"Arithmetic Expression : ==> {self.expr}\nTokens : ==> {self.tokens}"
