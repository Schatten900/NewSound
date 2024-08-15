from flask import Flask, request, render_template, jsonify,redirect,url_for, session
from servicos.modContas import CntrlSConta

app = Flask(__name__)

@app.route("/")
def home():
    pass

@app.route("/login", methods=["GET","POST"])
def login():
    #Pegar os dados do usuario e checar
    if request.method == "POST":
        email = request.form['loginEmail']
        senha = request.form['loginPassword']
        controladora = CntrlSConta()
        user = controladora.logar(email,senha)
        if user:
            return jsonify({"message":"login concluido","status":"success","redirect":url_for('home')}),200
        else:
            return jsonify({"message":"falha ao logar","status":"fail"}),401
    
    #Mostrar a tela de registro
    elif request.method == "GET":
        return render_template("login.html")
    
    #Caso aconteça algo inesperado
    else:
        return jsonify({"message":"Ação invalida","status":"fail"}),401
    

@app.route("/register", methods=["GET","POST"])
def registrar():
    #Pegar os dados do usuario e checar
    if request.method == "POST":
        nome = request.form['registerNome']
        email = request.form['registerEmail']
        senha = request.form['registerPassword']
        confirm = request.form['registerConfirm']
        controladora = CntrlSConta()
        user = controladora.cadastrar(nome,email,senha,confirm)
        if user:
            return jsonify({"message":"sucesso ao registrar","status":"success","redirect":url_for('home')}),200
        else:
            return jsonify({"message":"falha ao registrar usuario","status":"fail"}),401
    
    #Mostrar a tela de registro
    elif request.method == "GET":
        return render_template("register.html")
    #Caso aconteça algo inesperado
    else:
        return jsonify({"message":"Acao invalida","status":"fail"}),401


@app.route("/playlist")
def playlist():
    music = ("Camisado")
    title = "Rock"
    return render_template("playlist.html",Musics=music,Title=title)

if __name__ == "__main__":
    app.run(debug=True, port=8000)