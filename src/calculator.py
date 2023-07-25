from dataclasses import dataclass
from enum import Enum
from typing import Generic, Optional, TypeVar

from exceptions import ArithmeticSyntaxError, InterpreterException


class Type(str, Enum):
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

    def get_priority(self):
        priorities = {
            "+": 1,
            "-": 2,
            "*": 3,
            "/": 3,
        }
        return priorities.get(self.value)


T = TypeVar("T")  # Type variable for the data stored in the node


class BinaryTreeNode(Generic[T]):
    def __init__(self, data: Token):
        self.data: Token = data
        self.left: Optional["BinaryTreeNode[T]"] = None
        self.right: Optional["BinaryTreeNode[T]"] = None


@dataclass
class AbstractSyntaxTree:
    root: BinaryTreeNode


class Interpreter:
    OPERATORS = {Type.DIV, Type.MINUS, Type.PLUS, Type.MULT}

    def __init__(self) -> None:
        # self.expr = arthmetic_expression
        self.result = 0
        self.tokens: list[Token] = []
        self.digits_buffer: list[str] = []

    def __str__(self):
        return f"Arithmetic Expression : ==> {self.expr}\nTokens : ==> {self.tokens}"

    def __consume_digits_buffer(
        self,
    ):
        if self.digits_buffer:
            self.tokens.append(
                Token(value=int("".join(self.digits_buffer)), type=Type.NUMBER)
            )
            self.digits_buffer = []

    def __lexical_analysis(self):
        for character in self.expr:
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
                    raise InterpreterException
        self.__consume_digits_buffer()
        return self.tokens

    def __syntax_analysis(self, tokens: list[Token]) -> BinaryTreeNode:
        if len(self.tokens) % 2 == 0:
            raise ArithmeticSyntaxError
        if len(tokens) == 1:
            return BinaryTreeNode(data=tokens[0])
        lowest_priority = float("inf")
        lowest_priority_index = None
        for i in range(len(tokens) - 1, -1, -1):
            if tokens[i].type in self.OPERATORS:
                priority = tokens[i].get_priority()
                if priority <= lowest_priority:
                    lowest_priority = priority
                    lowest_priority_index = i
        root_node = BinaryTreeNode(tokens[lowest_priority_index])
        root_node.left = self.__syntax_analysis(tokens=tokens[:lowest_priority_index])
        root_node.right = self.__syntax_analysis(
            tokens=tokens[lowest_priority_index + 1 :]
        )

        return root_node

    def tree_walk(self, tree_root: BinaryTreeNode):
        result = 0
        if tree_root.data.type == Type.PLUS:
            result = (
                result
                + self.tree_walk(tree_root=tree_root.left)
                + self.tree_walk(tree_root=tree_root.right)
            )
            return result

        elif tree_root.data.type == Type.MULT:
            result = self.result + self.tree_walk(
                tree_root=tree_root.left
            ) * self.tree_walk(tree_root=tree_root.right)
            return result
        elif tree_root.data.type == Type.DIV:
            result = self.result + self.tree_walk(
                tree_root=tree_root.left
            ) / self.tree_walk(tree_root=tree_root.right)
            return result
        elif tree_root.data.type == Type.MINUS:
            result = (
                self.result
                + self.tree_walk(tree_root=tree_root.left)
                - self.tree_walk(tree_root=tree_root.right)
            )
            return result
        elif tree_root.data.type == Type.NUMBER:
            return tree_root.data.value

    def interpret(self, arithmetic_expression: str):
        self.tokens = []
        self.expr = arithmetic_expression
        tokens = self.__lexical_analysis()
        self.abstract_syntax_tree = AbstractSyntaxTree(
            root=self.__syntax_analysis(tokens=tokens)
        )
        return self.tree_walk(self.abstract_syntax_tree.root)
