import servidor
import threading
from servidor.operacoes import somar
import json

class ProcessaCliente(threading.Thread):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address
        self.sum = somar.Somar()

#----------interaction with sockets ---------------
    def receive_int(self, n_bytes: int) -> int:
        """
        :param n_bytes: The number of bytes to read from the current connection
        :return: The next integer read from the current connection
        """
        data = self.connection.recv(n_bytes)
        return int.from_bytes(data, byteorder='big', signed=True)

    def send_int(self, value: int, n_bytes: int) -> None:
        """
        :param value: The integer value to be sent to the current connection
        :param n_bytes: The number of bytes to send
        """
        self.connection.send(int(value).to_bytes(n_bytes, byteorder="big", signed=True))

    def receive_str(self, n_bytes: int) -> str:
        """
        :param n_bytes: The number of bytes to read from the current connection
        :return: The next string read from the current connection
        """
        data = self.connection.recv(n_bytes)
        return data.decode()

    def send_str(self, value: str) -> None:
        """
        :param value: The string value to send to the current connection
        """
        self.connection.send(value.encode())

    def send_object(self, obj):
        """1º: envia tamanho, 2º: envia dados."""
        data = json.dumps(obj).encode('utf-8')
        size = len(data)
        self.connection.send_int(self.connection, size, servidor.INT_SIZE) # Envio do tamanho
        self.connection.send(data)# Envio do objeto

    def receive_object(self):
        """1º: lê tamanho, 2º: lê dados."""
        size = self.connection.receive_int(self.connection, servidor.INT_SIZE) #   Recebe o tamanho
        data = self.connection.recv(size)  # Recebe o objeto
        return json.loads(data.decode('utf-8'))

    #--------
    def run(self):
        print(self.address, "Thread iniciada")
        last_request = False
        while not last_request:
            request_type = self.receive_str(servidor.COMMAND_SIZE)
            if request_type == servidor.ADD_OP:
                x = self.receive_int(servidor.INT_SIZE)
                y = self.receive_int(servidor.INT_SIZE)
                print(f"[{self.address}] Somar: {x} + {y}")
                result = self.sum.execute(x, y)
                self.send_int(result, servidor.INT_SIZE)
            elif request_type == servidor.SUB_OP:
                pass
            elif request_type == servidor.END_OP:
                last_request = True
                print(self.address,"Thread terminada")
                self.connection.close()