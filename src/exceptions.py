class InterpreterException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Undefined : Could not interpret this expression", *args)


class ArithmeticSyntaxError(InterpreterException):
    def __init__(self, *args: object) -> None:
        super().__init__("Something is wrong with syntax of your expression", *args)
