from flask import Flask,jsonify,request

app = Flask(__name__)

@app.route("/")
def home():
    pass

@app.route("/login")
def login():
    pass

@app.route("register")
def registrar():
    pass

@app.route("/playlist")
def playlist():
    pass

if __name__ == "__main__":
    app.run(debug=True)