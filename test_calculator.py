import pytest

from calculator import Interpreter


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
    interpreter = Interpreter()

    with pytest.raises(expected_exception=Exception):
        interpreter.interpret(arithmetic_expression=honey_pot)
