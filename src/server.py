import socket
from multiprocessing import connection, get_context

from calculator import Interpreter

HEADER_SIZE = 64


def read_client_data(
    client_connection: socket.socket, remote_address, write_conn: connection.Connection
):
    while True:
        data_length = client_connection.recv(HEADER_SIZE).decode()
        if data_length:
            data = client_connection.recv(int(data_length)).decode()
            print("from connected client: " + data)
            if data == "END_OF_OPERATIONS":
                print(f"[DONE] reading operations from client : {str(remote_address)}")
                write_conn.send(data)
                break
            write_conn.send(data)


def save_results(read_conn: connection.Connection):
    with open("results.csv", "a") as f:
        while read_conn.poll(timeout=1):
            result = read_conn.recv()
            f.write(result + "\n")


def calculation(read_conn: connection.Connection, write_conn: connection.Connection):
    interpreter = Interpreter()  # our calculator
    while True:
        expression = read_conn.recv()
        if expression == "END_OF_OPERATIONS":
            break
        try:
            result = interpreter.interpret(arithmetic_expression=expression)
        except Exception:
            result = None
        write_conn.send(f"{expression} , {result}")


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5555
    Interpreter()  # our calculator
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print("[LISTENING] ...")
        multiprocessing_context = get_context(method="fork")

        read_operations_conn, write_operations_conn = multiprocessing_context.Pipe()
        read_results_conn, write_results_conn = multiprocessing_context.Pipe()

        while True:
            calc_process = multiprocessing_context.Process(
                target=calculation, args=(read_operations_conn, write_results_conn)
            )
            new_connection, address = server_socket.accept()
            print("OPENNING Connection from: " + str(address))

            calc_process.start()
            read_client_data(
                client_connection=new_connection,
                remote_address=address,
                write_conn=write_operations_conn,
            )
            save_results(read_conn=read_results_conn)
            calc_process.join()
            print("CLOSING Connection from: " + str(address))
            new_connection.close()


if __name__ == "__main__":
    server_program()
