import socket
from typing import Generator


def arithmetic_operations_generator(
    source_file: str = "operations.txt",
) -> Generator[str, None, None]:
    with open(source_file, "r") as f:
        for op in f:
            yield op


HEADER_SIZE = 64


def send_with_protocol(client: socket.socket, message: str):
    message = message.strip().encode()
    message_length = len(message)
    length_header = str(message_length).encode()
    client.send(
        length_header + b" " * (HEADER_SIZE - len(length_header))
    )  # send the length of the message
    client.send(message)  # send the message


def client_program():
    # Server that this client will connect to
    server_host = socket.gethostname()
    server_port = 5555
    client_socket = socket.socket()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, server_port))  # connecting to the server

        for operation in arithmetic_operations_generator(source_file="test_op.txt"):
            send_with_protocol(client=client_socket, message=operation)

        send_with_protocol(client=client_socket, message="END_OF_OPERATIONS")


if __name__ == "__main__":
    client_program()
