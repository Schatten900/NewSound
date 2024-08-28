from flask import Flask, request, render_template, jsonify,url_for, session,redirect
from servicos.modContas import CntrlSConta
from servicos.modMusica import CntrlSPlaylist
from dominios.bancoDef import flaskSecret
from dotenv import load_dotenv
import os
import base64

app = Flask(__name__)
app.secret_key = flaskSecret

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
            session["nomeUser"] = user.getNome().get()
            session["emailUser"] = user.getEmail().get()
            session["passwordUser"] = user.getSenha().get()
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
        controladora = CntrlSConta()
        user = controladora.cadastrar(nome,email,senha)
        if user:
            session["userID"] = user.getId()
            session["nomeUser"] = user.getNome().get()
            session["emailUser"] = user.getEmail().get()
            session["passwordUser"] = user.getSenha().get()
            return jsonify({"message":"sucesso ao registrar","status":"success","redirect":url_for('Login')}),200
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
@app.route("/usuario",methods=["GET","POST"])
def UsuarioPage():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "edit":
            id = session["userID"]
            nome = request.form.get("nome")
            email = request.form.get("email")
            imagem = request.files.get("imagem")
            dicionario = {}
            if nome:
                dicionario["Nome"] = nome
            if email:
                dicionario["Email"] = email
            if imagem:
                imagem_blob = imagem.read()
                dicionario["FotoPerfil"] = imagem_blob

            #logica para receber dicionario e editar o usuario no banco de dados
            controladora = CntrlSConta()
            if controladora.editar(id,dicionario):
                if "Email" in dicionario:
                    session["emailUser"] = dicionario["Email"]

                if "Nome" in dicionario:
                    session["nomeUser"] = dicionario["Nome"]

                return jsonify({"message":"Edição valida","status":"success","redirect":url_for("UsuarioPage")}),200
            else:
                return jsonify({"message":"Edição invalida","status":"fail"}),401
        elif action == "excluir":
            #logica para excluir usuario do banco de dados
            #para poder excluir a conta, deve-se excluir musicas salvas e playlist usuario
            return jsonify({"message":"exclusao valida","status":"success","redirect":url_for("UsuarioPage")}),200
        
        elif action == "playlist":
            #Redirecionar para playlists do usuario
            return jsonify({"message":"redirecionando playlist","status":"success","redirect":url_for("PlaylistCriadas")}),200

        elif action == "musicas":
            #Redirecionar para musicas salvas pelo usuario
            return jsonify({"message":"redirecionando musicas","status":"success","redirect":url_for("MusicasSalvas")}),200
        else:
            return jsonify({"message":"Acao invalida","status":"fail"}),401
    else:
        #Metodo GET, mostrar usuario na tela
        controladora = CntrlSConta()
        id = session["userID"]
        usuario = controladora.ler(id)
        imagem = usuario[4]
        if imagem:
            #decodifica a imagem em base 64
            imagem64 = base64.b64encode(imagem).decode('utf-8')
            #cria um caminho para o html poder processar
            imagem = f"data:image/jpeg;base64,{imagem64}"
        else:
            imagem = None
        return render_template("usuario.html",Usuario=usuario,Imagem=imagem)

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
@app.route("/musicasSalvas",methods=["GET","POST"])
def MusicasSalvas():
    #endpoint para navegar pelas musicas salvas pelo usuario
    #Fazer select do banco de dados
    if request.method == "POST":
        action = request.form.get("action")
        nameMusic = request.form.get("musicaName")
        nameArtista = request.form.get("artistaName")
        if action == "add":
            musica = request.files.get("musica")
            idUsuario = session["userID"]
            if musica:
                musica_blob = musica.read()
            #controladora = CntrlSMusica()
            #Checar se existe a musica no banco de dados
            #existe = controladora.pesquisarMusica(nameMusic,nameArtista)
            #if existe:
                #constroladora.adicionarMusicaUsuario(nameMusic,nameArtista,idUsuario)
            #else:
                #adiciona no banco de dados a musica e no musicas Salvas do usuario
                #controladora.adicionarMusica(nameMusic,nameArtista,idUsuario,musica)
                #constroladora.adicionarMusicaUsuario(nameMusic,nameArtista,idUsuario)

    else: 
        #musicasPlaylist = controladora.pesquisarMusicas(idUSuario)
        musicas = [("Euforia","Teste1"),("Ceu azul","Charlie Brown"),("Rise","Katty")]
        return render_template("musicasSalvas.html",Musicas=musicas)

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
        #logica pra pegar o id pelo click na musica
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
        action = request.form.get("action")
        nameMusic = request.form.get("musicaName")
        nameArtista = request.form.get("artistaName")
        musica = request.files.get("musica")
        idUsuario = session["userID"]
        if musica:
            musica_blob = musica.read()
        if action == "add":
            pass
            #adicionar musica na playlist
            #if musica:
                #controladora.adicionarMusica(nameMusic,nameArtista,id_playlist,musica_blob)
            #else:
                #controladora.adicionarMusica(nameMusic,nameArtista,id_Playlist)
        else:
            #remover musica da playlist
            #controladora.removerMusica(nameMusic,nameArtista,id_playlist)
            pass
    else:
        #Fazer select do banco de dados, musicas e titulo da playlist
        musicasPlaylist = controladora.pesquisarMusicas(id_playlist)
        title = "Rock"
        return render_template("playlistUser.html",MusicasPlaylist=musicasPlaylist,Title=title,idPlaylist=id_playlist)
    
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
    #nome do artista,album,imagem
    info = [("Panic at Disco","Album2", "https://via.placeholder.com/150"),("Panic at Disco","Album1","https://via.placeholder.com/150")]
    return render_template("artistaMusica.html",informacoes=info)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
