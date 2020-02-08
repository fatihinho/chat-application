from flask import Flask, session, redirect, url_for, escape, request, render_template

NAME_KEY = "name"

app = Flask(__name__)
app.secret_key = b"\x8b[\x06[\xed*\x06\xd7\xbe\x14t\x195\xac_2"


@app.route("/")
@app.route("/home")
def home():
    """if NAME_KEY not in session:
        return redirect(url_for("login"))"""

    # name = session[NAME_KEY]
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop(NAME_KEY, None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
