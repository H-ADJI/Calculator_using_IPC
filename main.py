# import socket

from calculator import Interpreter


x = Interpreter("85+20 + 5")
x.lexical_parsing()
print(x)