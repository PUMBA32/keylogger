import socket as sock
import os
import sys
import logging


from typing import Optional, List


class Client:
    def __init__(self, host: str = sock.gethostname(), port: int = 12345) -> None: 
        self._host: str = host
        self._port: str = port

        self.client: sock.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

        try:
            self.client.connect((self._host, self._port))
        except sock.error as err:
            self.client.close()
            logging.critical(f"Client connecting to server failed: {err}")
        else:
            logging.info("connected.")


    def __str__(self) -> str:
        return f"host: {self._host}; port: {self._port}"
    

    def __cls(self) -> None: 
        os.system("cls" if sys.platform == 'win32' else "clear")


    def send(self, data: str | List[str]) -> Optional[str]: 
        self.__cls()

        if type(data) == list:
            data = "".join(data)

        try:
            self.client.send(data.encode())
        except sock.error as err:
            self.client.close()
            logging.warning(f"Sending data failed: {err}")
            raise Exception(f"Sending data failed: {err}")

        
    def close(self) -> None:
        self.client.close()