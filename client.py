import socket
from typing import Generator

from constants import EOO, MSG_SIZE, SERVER_PORT


def arithmetic_operations_generator(
    source_file: str = "operations.txt",
) -> Generator[str, None, None]:
    with open(source_file, "r") as f:
        for op in f:
            yield op


def send_with_protocol(client: socket.socket, message: str):
    message = message.strip()
    message = f"{message:<{MSG_SIZE}}"
    client.send(bytes(message, "utf-8"))  # send the length of the message


def client_program():
    # Server that this client will connect to
    server_host = socket.gethostname()
    client_socket = socket.socket()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, SERVER_PORT))  # connecting to the server

        for operation in arithmetic_operations_generator():
            send_with_protocol(client=client_socket, message=operation)
        send_with_protocol(client=client_socket, message=EOO)


if __name__ == "__main__":
    client_program()
