from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread, Lock
import time


class Client:
    """
    Server ile iletişimi sağlar.
    """
    # GLOBAL CONSTANTS
    HOST = "localhost"
    PORT = 5500
    BUFSIZE = 512
    ADDR = (HOST, PORT)

    def __init__(self, name):
        """
        Objeleri tanımlar ve name parametresinin mesajını server'a yollar.
        :param name: str
        """
        self.messages = []
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        client_thread = Thread(target=self.receive_message)
        client_thread.start()
        self.send_message(name)
        self.lock = Lock()

    def receive_message(self):
        """
        Server'dan gelen mesajı alır.
        :return: None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZE).decode("utf8")
                self.lock.acquire()  # kilitler
                self.messages.append(msg)
                self.lock.release()  # kilidi açar
            except Exception as e:
                print("[HATA]", e)
                break

    def send_message(self, msg):
        """
        Kullanıcının mesajını server'a iletir.
        :param msg: str
        :return: None
        """
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            self.client_socket.close()

    def get_messages(self):
        """
        :returns str tipinde mesajların bulunduğu list döndürür.
        :return: list[str]
        """
        messages_copy = self.messages[:]  # kopyalar
        # hafızanın mesajlara erişiminin güvenliğini sağlar
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy

    def disconnect(self):
        self.send_message("{quit}")
