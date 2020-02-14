from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
from client import Client
from threading import Thread
import time

NAME_KEY = "name"
client = None
messages = []

app = Flask(__name__)
app.secret_key = b"\x8b[\x06[\xed*\x06\xd7\xbe\x14t\x195\xac_2"


@app.route("/")
@app.route("/home")
def home():
    """
    Eğer giriş yapılmışsa anasayfa'yı gösterir.
    :return: None
    """
    global client
    if NAME_KEY not in session:
        return redirect(url_for("login"))
    client = Client(session[NAME_KEY])
    return render_template("index.html", **{"session": session})


def disconnect():
    """
    Kullanıcı, server'dan ayrılmadan önce çağırılır.
    :return: None
    """
    global client
    if client:
        client.disconnect()


@app.route("/login", methods=["POST", "GET"])
def login():
    """
    Giriş yapma ekranını yükler ve session'a kullanıcının ismini kaydeder.
    :exception POST
    :return: None
    """
    if request.method == "POST":
        session[NAME_KEY] = request.form["inputName"]
        return redirect(url_for("home"))
    return render_template("login.html", **{"login": True, "session": session})


@app.route("/logout")
def logout():
    """
    Session'dan çıkış yapan kullanıcıların ismini siler.
    :return: None
    """
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))


@app.route("/send_message")
def send_message():
    """
    JQuery'den gönderilecek mesajları çağırır.
    :return: None
    """
    global client
    msg = request.args.get("val")
    if client is not None:
        client.send_message(msg)
    return "none"


@app.route("/get_messages")
def get_messages():
    return jsonify({"messages": messages})


def update_messages():
    """
    Mesaj listesini update eder.
    :return: None
    """
    global client
    global messages
    run = True
    while run:
        time.sleep(0.1)  # her 1 salisede update eder
        if not client:
            continue
        new_messages = client.get_messages()  # client'tan yeni mesajı tutar
        messages.extend(new_messages)  # yeni mesajları local bir liste'de tutar
        for msg in new_messages:  # yeni mesajları görüntüler
            print(msg)
            if msg == "{quit}":
                disconnect()
                run = False
                break


if __name__ == "__main__":
    Thread(target=update_messages).start()
    app.run(debug=True)
