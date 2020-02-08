from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import time
from person import Person

# GLOBAL CONSTANTS (Sabitler)
HOST = "localhost"
PORT = 5500
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZE = 512                          # aktarılan data'nın byte sayısı
TIME = time.ctime(time.time())

# GLOBAL VARIABLES (Değişkenler)
persons = []
server = socket(AF_INET, SOCK_STREAM)  # AF_INET -> IPv4 tipinde '100.50.200.5' gibi adresler. # SOCK_STREAM -> Tipi.
server.bind(ADDR)                      # server kurulur


def broadcast(msg, name):
    """
    Tüm kullanıcılara mesaj yollar.
    :param msg: bytes["utf8"]
    :param name: str
    :return: None
    """
    for person in persons:
        client = person.client
        try:
            client.send(bytes(f"{name}", "utf8") + msg)
        except Exception as e:
            print("[HATA]", e)


def client_communication(person):
    """
    Kullanıcılardan gelen mesajları tutar.
    :param person: Person
    :return: None
    """
    client = person.client

    # ilk gelen mesajının, kişinin ismi olmasını sağlıyor
    name = client.recv(BUFSIZE).decode("utf8")
    person.set_name(name)
    msg = bytes(f"{name} katıldı!", "utf8")
    broadcast(msg, "")                                  # katıldı duyurusu | send() edildi

    while True:                                         # kullanıcıdan gelecek mesajı bekler
        msg = client.recv(BUFSIZE)                      # msg -> bytes | client tarafından gelen mesajı tutar

        if msg == bytes("{quit}", "utf8"):              # mesaj 'quit' olduğunda, o kişi sohbet'ten çıkar
            client.close()
            persons.remove(person)
            broadcast(bytes(f"{name} sohbeti terk etti...", "utf8"), "")
            print(f"[TERK] {name} ayrıldı.")
            break
        else:                                           # aksi takdirde, diğer kullanıcılarla sohbet'e devam eder
            broadcast(msg, name+": ")                   # isim: mesaj (client) | send() edildi
            print(f"{name}:", msg.decode("utf8"))       # isim: mesaj (server) | msg -> str


def wait_for_connection():
    """
    Yeni katılacak olan kullanıcıların bağlantılarını bekler.
    :return: None
    """
    while True:                                         # herhangi bir bağlantıyı bekler
        try:
            client, addr = server.accept()              # accept() -> (socket objesi, adres bilgisi)
            person = Person(addr, client)               # bağlantı için yeni bir kişi objesi oluşturur
            persons.append(person)
            print(f"[BAĞLANTI] {person.addr}, server'a bağlandı ({TIME}).")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print("[HATA]", e)
            break

    print("SERVER HATASI")


if __name__ == '__main__':
    server.listen(MAX_CONNECTIONS)                      # bağlantıları dinlemek için server'ı açar
    print("Bağlantılar bekleniyor...")
    server_thread = Thread(target=wait_for_connection)
    server_thread.start()
    server_thread.join()                                # thread terminate edilene kadar bekletilir
    server.close()
