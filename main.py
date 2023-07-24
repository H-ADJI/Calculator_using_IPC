# import socket

from src.calculator import Interpreter


def main():
    interpreter = Interpreter()
    with open("operations.txt", "r") as f:
        for op in f:
            try:
                interpreter.interpret(arithmetic_expression=op)
            except Exception:
                print(f"invalid input {op}")


if __name__ == "__main__":
    main()
