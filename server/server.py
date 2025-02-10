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

        self._path_to_base_dir: str = os.path.dirname(__file__)
        self._path_to_data_dir: str = os.path.join(self._path_to_base_dir, "data")
        
    
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
        # сохранение данных в папку data
        try:
            self.__save_data(self.__get_data(conn))
        except Exception as ex:
            raise Exception(f"{ex}")


    def __save_data(self, data: list[str]) -> None: 
        for record in data:
            try:
                date, time, key = record.split(":")
            except: continue

            # создание папки data, если ее не существует
            if not os.path.exists(self._path_to_data_dir):
                os.makedirs(self._path_to_data_dir)

            files: list[str] = os.listdir(self._path_to_data_dir)
            
            if date := os.path.join(self._path_to_data_dir, date+".txt") not in files:
                pass
            else: ...


    def __get_data(self, conn: socket.socket) -> tuple[str]: 
        try:
            buffer: bytes = conn.recv(1024)
            data: str = buffer.decode()
            return tuple(data.split("\n"))                
        except Exception as ex:
            raise Exception(f"__get_data. Getting data from client failed: {ex}")


def main() -> None: 
    server: Server = Server()
    server.run()


if __name__ == '__main__':
    main()
