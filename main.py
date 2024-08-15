from flask import Flask, request, render_template, jsonify,redirect,url_for, session
from servicos.modContas import CntrlSConta
from servicos.modMusica import CntrlSPlaylist

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
            session["userID"] = id
            return jsonify({"message":"sucesso ao registrar","status":"success","redirect":url_for('home')}),200
        else:
            return jsonify({"message":"falha ao registrar usuario","status":"fail"}),401
    
    #Mostrar a tela de registro
    elif request.method == "GET":
        return render_template("register.html")
    #Caso aconteça algo inesperado
    else:
        return jsonify({"message":"Acao invalida","status":"fail"}),401


@app.route("/playlist",methods=["GET","POST"])
def playlist():
    if request.method == "POST":
        nameMusic = request.form["musicaInput"]
        nameArtista = request.form["artistaInput"]
        controladora = CntrlSPlaylist
        #id = session["userID"]
        #controladora.adicionarMusica(nameMusic,nameArtista,id)
        #logica para adicionar na playlist se nao houver na playlist
    else:
        #Fazer select do banco de dados
        music = ("Camisado")
        title = "Rock"
        return render_template("playlist.html",Musics=music,Title=title)
    
@app.route("/playlist/saves")
def playlistSaves():
    #Fazer select do banco de dados das playlist salvas pelo usuario
    #controladora = CntrlSPlaylist()

    music = ("Camisado")
    title = "Rock"
    return render_template("playlistSaves.html",Musics=music,Title=title)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
