from .client import Client
from threading import Thread
import time

c1 = Client("Fatih")
c2 = Client("Çınar")


def test():
    c1.send_message("selam")
    time.sleep(2)
    c2.send_message("selam")
    time.sleep(2)
    c1.send_message("naber")
    time.sleep(2)
    c2.send_message("iyiyim, teşekkürler")
    time.sleep(2)

    c1.disconnect()
    time.sleep(2)
    c2.disconnect()


def update_messages():
    """
    Mesaj listesini update eder.
    :return: None
    """
    run = True
    msgs = []
    while run:
        time.sleep(0.1)                     # her 1 salisede update eder
        new_messages = c1.get_messages()    # client'tan yeni mesajı tutar
        msgs.extend(new_messages)           # yeni mesajları local bir liste'de tutar
        for msg in new_messages:            # yeni mesajları görüntüler
            print(msg)
            if msg == "{quit}":
                run = False
                break


Thread(target=update_messages).start()

test()
