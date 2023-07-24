import pytest

from src.calculator import Interpreter
from src.exceptions import InterpreterException,ArithmeticSyntaxError

def test_interpreter_result():
    interpreter = Interpreter()
    with open("operations.txt", "r") as f:
        for i, op in enumerate(f):
            try:
                result = interpreter.interpret(arithmetic_expression=op)
                assert eval(op) == result
            except Exception:
                pass


def test_invalid_input():
    honey_pot = "import sys; sys.exit()"
    invalid_expression_syntax = "9 - 2 +* 6"

    interpreter = Interpreter()

    with pytest.raises(expected_exception=InterpreterException):
        interpreter.interpret(arithmetic_expression=honey_pot)

    with pytest.raises(expected_exception=ArithmeticSyntaxError):
        interpreter.interpret(arithmetic_expression=invalid_expression_syntax)
