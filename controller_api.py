import json
from socket import socket, AF_INET, SOCK_STREAM

from config import CONTROLLER_SOCKET


class ControllerAPI:
    instance: 'ControllerAPI'

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ControllerAPI, cls).__new__(cls)
        return cls.instance

    def __init__(self, addr: tuple[str, int]):
        self.addr = addr
        self.__controller_socket = socket(AF_INET, SOCK_STREAM)
        self.__connect()

    def __del__(self):
        self.__close()

    def __request(self, text: str) -> str:
        self.__controller_socket.send(bytes(text, 'utf-8'))
        data = self.__controller_socket.recv(1024)
        if data == b'ERROR':
            raise Exception('Failed to set value')
        return data.decode('utf-8')

    def __connect(self):
        self.__controller_socket.connect(self.addr)

    def __close(self):
        self.__controller_socket.send(b'bye')
        self.__controller_socket.close()

    def set_out(self, gpio: str, value: int):
        self.__request(f'SET_VAL {gpio} {value}')

    def get_out(self, gpio: str) -> int:
        data = self.__request(f'GET_VAL {gpio}')
        return int(data)

    def get_devices(self) -> dict:
        data = self.__request('GET_DEVICES')
        return json.loads(data)


controller = ControllerAPI(CONTROLLER_SOCKET)
