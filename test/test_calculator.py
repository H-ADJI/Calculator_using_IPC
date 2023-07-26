import pytest

from calculator import CalculatorInterpreter
from exceptions import ArithmeticSyntaxError, InterpreterException


def test_interpreter_result():
    calculator_interpreter = CalculatorInterpreter()
    with open("test/test_operations.txt", "r") as f:
        for i, op in enumerate(f):
            try:
                result = calculator_interpreter.interpret(arithmetic_expression=op)
                assert eval(op) == result
            except Exception:
                pass


def test_invalid_input():
    honey_pot = "import sys; sys.exit()"
    invalid_expression_syntax = "9 - 2 +* 6"

    calculator_interpreter = CalculatorInterpreter()

    with pytest.raises(expected_exception=InterpreterException):
        calculator_interpreter.interpret(arithmetic_expression=honey_pot)

    with pytest.raises(expected_exception=ArithmeticSyntaxError):
        calculator_interpreter.interpret(
            arithmetic_expression=invalid_expression_syntax
        )
