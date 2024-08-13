from flask import Flask, request, render_template, jsonify,redirect,url_for, session

app = Flask(__name__)

@app.route("/")
def home():
    pass

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def registrar():
    return render_template("register.html")

@app.route("/playlist")
def playlist():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=8000)