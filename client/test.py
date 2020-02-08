from client import Client
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
    run = True
    msgs = []
    while run:
        time.sleep(0.1)
        new_messages = c1.get_messages()
        msgs.extend(new_messages)
        for msg in new_messages:
            print(msg)
            if msg == "{quit}":
                run = False
                break


Thread(target=update_messages).start()

test()
