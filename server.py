import socket
from itertools import cycle
from multiprocessing import Pipe, Process, connection
from threading import Event, Thread

from loguru import logger

from calculator import CalculatorInterpreter
from constants import EOO, MSG_SIZE, SERVER_PORT


class CalculationWorker(Process):
    def __init__(
        self, read_conn: connection.Connection, write_conn: connection.Connection
    ) -> None:
        super().__init__()
        self.read_conn = read_conn
        self.write_conn = write_conn

    def run(self) -> None:
        calculator = CalculatorInterpreter()  # our calculator
        while True:
            expression = self.read_conn.recv()
            if expression == EOO:
                break
            try:
                result = calculator.interpret(arithmetic_expression=expression)
            except Exception:
                result = None
            self.write_conn.send(f"{expression} = {result}")


class CalculationServer:
    def __init__(self, worker_count: int = 1) -> None:
        self.operations_pipes = [Pipe() for _ in range(worker_count)]
        self.results_pipes = [Pipe() for _ in range(worker_count)]
        self.worker_count = worker_count

    def launch_workers(self):
        self.workers = [
            CalculationWorker(
                read_conn=self.operations_pipes[i][0],
                write_conn=self.results_pipes[i][1],
            )
            for i in range(self.worker_count)
        ]
        for worker in self.workers:
            worker.start()

    def read_client_data(
        self,
        client_connection: socket.socket,
        remote_address,
    ):
        logger.info("[Reading data]")
        for round_robin in cycle(range(self.worker_count)):
            data = client_connection.recv(MSG_SIZE)
            data = data.decode().strip()
            if data == EOO:
                for conn in self.operations_pipes:
                    conn[1].send(data)
                logger.info(
                    f"[DONE] reading operations from client : {str(remote_address)}"
                )
                break
            if data:
                self.operations_pipes[round_robin][1].send(data)

    def handle_connection(self, server_socket: socket.socket, event: Event):
        new_connection, address = server_socket.accept()
        logger.info("OPENNING Connection from: " + str(address))
        self.launch_workers()
        event.set()
        self.read_client_data(
            client_connection=new_connection,
            remote_address=address,
        )

    def log_results(self, event: Event):
        event.wait()
        logger.debug("STARTING LOGGING")
        for rounb_robin in cycle(range(self.worker_count)):
            if not (
                self.results_pipes[rounb_robin][0].poll(timeout=1)
                or self.results_pipes[rounb_robin - 1][0].poll(timeout=1)
            ):
                break
            result = self.results_pipes[rounb_robin][0].recv()
            logger.info(result)
        for worker in self.workers:
            worker.join()

    def run_server(self):
        HOST = socket.gethostname()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, SERVER_PORT))
            server_socket.listen()
            while True:
                logger.info("[LISTENING] ...")
                consume_trigger = Event()
                thread = Thread(target=self.log_results, args=(consume_trigger,))
                thread.start()
                self.handle_connection(
                    server_socket=server_socket, event=consume_trigger
                )
                thread.join()
                logger.debug("[DONE]")


if __name__ == "__main__":
    calc_server = CalculationServer(worker_count=3)
    calc_server.run_server()
