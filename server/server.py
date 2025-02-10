import socket 
import os
import sys


'''
РАБОТА СЕРВЕРА

1. Слушанье входящих соединений
2. Принятие клиентского сокета
3. Получение данных от клиента
4. Обработка данных: 

'''


class Server:
    def __init__(self, host: str = socket.gethostname(), port: int = 12345) -> None: 
        self._host: str = host
        self._port: int = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)


    
    def run(self) -> None: 
        try: 
            self.server.bind((self._host, self._port))
            self.server.listen()
            print("listening...")
            while 1: 
                conn, addr = self.server.accept()
                print(f"[+] new connection by: {addr}")
                try:
                    self.serve_client(conn)
                except Exception as ex:
                    print(f"[ERROR]: {ex}")
        finally:
            self.server.close()

    
    def serve_client(self, conn: socket.socket) -> None: 
        data: str = self.__get_data(conn)
        print(data)

    
    def __get_data(self, conn: socket.socket) -> str: 
        try:
            buffer: bytes = conn.recv(1024)
            data: str = buffer.decode()
            return data                
        except Exception as ex:
            raise Exception(f"__get_data. Getting data from client failed: {ex}")


def main() -> None: 
    server: Server = Server()
    server.run()


if __name__ == '__main__':
    main()
