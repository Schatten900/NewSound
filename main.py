from flask import Flask, request, render_template, jsonify,url_for, session,redirect
from servicos.modContas import CntrlSConta
from servicos.modMusica import CntrlSPlaylist
from dotenv import load_dotenv
import os
import base64

app = Flask(__name__)

###########   Funcionalidades da conta ######################

#Carlos
@app.route("/login", methods=["GET","POST"])
def Login():
    #Pegar os dados do usuario e checar
    if request.method == "POST":
        data = request.json
        email = data.get("email")
        senha = data.get("senha")
        controladora = CntrlSConta()
        user = controladora.logar(email,senha)
        if user:
            session["userID"] = user.getId()
            session["nomeUser"] = user.getNome()
            session["emailUser"] = user.getEmail()
            session["passwordUser"] = user.getSenha()
            return jsonify({"message":"login concluido","status":"success","redirect":url_for('Home')}),200
        else:
            return jsonify({"message":"falha ao logar","status":"fail"}),401
    #Mostrar a tela de registro
    elif request.method == "GET":
        return render_template("login.html")
    
    #Caso aconteça algo inesperado
    else:
        return jsonify({"message":"Ação invalida","status":"fail"}),401
    
#Carlos
@app.route("/register", methods=["GET","POST"])
def Registrar():
    #Pegar os dados do usuario e checar
    if request.method == "POST":
        data = request.json
        nome = data.get("nome")
        email = data.get("email")
        senha = data.get("senha")
        confirm = data.get("confirm")
        nome = request.form['registerNome']
        email = request.form['registerEmail']
        senha = request.form['registerPassword']
        confirm = request.form['registerConfirm']
        controladora = CntrlSConta()
        user = controladora.cadastrar(nome,email,senha,confirm)
        if user:
            session["userID"] = user.getId()
            session["nomeUser"] = user.getNome()
            session["emailUser"] = user.getEmail()
            session["passwordUser"] = user.getSenha()
            return jsonify({"message":"sucesso ao registrar","status":"success","redirect":url_for('Home')}),200
        else:
            return jsonify({"message":"falha ao registrar usuario","status":"fail"}),401
        
    
    #Mostrar a tela de registro
    elif request.method == "GET":
        return render_template("register.html")
    #Caso aconteça algo inesperado
    else:
        return jsonify({"message":"Acao invalida","status":"fail"}),401
    
#Pagina do usuario onde ele pode fazer o CRUD
#Carlos 
@app.route("/usuario")
def UsuarioPage():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "edit":
            nome = request.form.get("nome")
            email = request.form.get("email")
            imagem = request.files.get("imagem")
            dicionario = {}
            if nome:
                dicionario["nome"] = nome
            if email:
                dicionario["email"] = email
            if imagem:
                imagem_blob = imagem.read()
                dicionario["imagem"] = imagem_blob

            #print(dicionario)
            #logica para receber dicionario e editar o usuario no banco de dados
            return jsonify({"message":"Edição valida","status":"success","redirect":url_for("UsuarioPage")}),200
        elif action == "excluir":
            #logica para excluir usuario do banco de dados
            return jsonify({"message":"Edição valida","status":"success","redirect":url_for("UsuarioPage")}),200
        
        elif action == "playlist":
            #Redirecionar para playlists do usuario
            return jsonify({"message":"Edição valida","status":"success","redirect":url_for("PlaylistCriadas")}),200

        elif action == "musicas":
            #Redirecionar para musicas salvas pelo usuario
            return jsonify({"message":"Edição valida","status":"success","redirect":url_for("MusicasSalvas")}),200
        else:
            return jsonify({"message":"Acao invalida","status":"fail"}),401
    else:
        #Metodo GET, mostrar usuario na tela
        usuario = ("Rodolfo","teste@gmail.com","https://via.placeholder.com/150")
        return render_template("usuario.html",Usuario=usuario)

###########   Funcionalidades da aplicação (musica) ######################

#HomePage do site
#Ricardo
@app.route("/")
def Home():
    return redirect(url_for('HomeRedirect'))

@app.route("/home", methods=["GET", "POST"])
def HomeRedirect():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "login":
            return redirect(url_for('Login'))
        elif action == "artistas":
            if 'userID' in session and session['userID'] is not None:
                return redirect(url_for('ArtistasPage'))
            else:
                return redirect(url_for('Login'))
        
        elif action == "navegar":
            if 'userID' in session and session['userID'] is not None:
                return redirect(url_for('NavegarPage'))
            else:
                return redirect(url_for('Login'))

        elif action == "usuario":
            if 'userID' in session and session['userID'] is not None:
                return redirect(url_for('UsuarioPage'))
            else:
                return redirect(url_for('Login'))
    return render_template("home.html")

@app.route("/navegar")
def NavegarPage():
    pass

#Carlos
@app.route("/MusicasSalvas")
def MusicasSalvas():
    #endpoint para navegar pelas musicas salvas pelo usuario
    pass

#################################################

#Logica a ser desenvolvida em controladora e redirecionamento 
#Ricardo/Carlos
@app.route("/playlistUser")
def PlaylistCriadas():
    #Fazer select do banco de dados das playlist criadas pelo usuario
    #CRUD Completo
    #idUsuario = session["userID"]
    #controladora = CntrlSPlaylist()
    #playlists = controladora.pesquisarPlaylist(idUsuario)e
    #criar o redirecionamento para o PlaylistUsuario/idPlaylist
    if request.method == "POST":
        #logica pra pegar o id
        render_template("playlistUser.html")
        
    else:
        playlist = [("Panic at Disco","https://via.placeholder.com/150"),("Panic at Disco","https://via.placeholder.com/150")]

    return render_template("playlistCreation.html",Playlist=playlist)

#Carlos
@app.route("/playlistUser/{id_playlist}",methods=["GET","POST"])
def playlistUsuario(id_playlist):
    #Adicao, seleção e remoção  relacionadas a uma playlist criada pelo usuario
    if request.method == "POST":
        controladora = CntrlSPlaylist()
        nameMusic = request.form["musicaInput"]
        nameArtista = request.form["artistaInput"]
        idUsuario = session["userID"]

        if request.action == "add":
            pass
            #adicionar musica na playlist
            #controladora.adicionarMusica(nameMusic,nameArtista,id_playlist)
        else:
            #remover musica da playlist
            #controladora.removerMusica(nameMusic,nameArtista,id_playlist)
            pass
    else:
        #Fazer select do banco de dados
        musicasPlaylist = controladora.pesquisarMusicas(id_playlist)
        title = "Rock"
        return render_template("playlistUser.html",MusicasPlaylist=musicasPlaylist,Title=title)
    
############################################    

#Ricardo
@app.route("/album/{idAlbum}")
def AlbumMusicas(idAlbum):
    #listar todas as musicas vinculadas à aquele album
    #Somente seleção ate então
    pass

###############################################################

#Carlos 
@app.route("/artista")
def ArtistasPage():
    #Seleção de artistas salvas na aplicação
    #controladora = cntrlSArtista()
    #artistas = controladora.pesquisarArtistas()
    artistas = [("Panic at Disco", "https://via.placeholder.com/150")]
    return render_template("artista.html",Artistas=artistas)

#Carlos
@app.route("/artista/{idArtista}")
def ArtistasPageSongs(idArtista):
    #Selecao de albuns vinculados ao artista de idArtista
    #Logica para pesquisar albuns do artista
    #Exemplo
    info = [("Panic at Disco","Album2", "https://via.placeholder.com/150"),("Panic at Disco","Album1","https://via.placeholder.com/150")]
    return render_template("artistaMusica.html",informacoes=info)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
