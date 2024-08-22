from flask import Flask, request, render_template, jsonify,url_for, session, redirect
#from flask_session import Session
from servicos.modContas import CntrlSConta
from servicos.modMusica import CntrlSPlaylist

app = Flask(__name__)

#app.config["SESSION_PERMANENT"] = False     #Adiciona timeout padrão pra uma seção
#app.config["SESSION_TYPE"] = "filesystem"   
#Session(app)

###########   Funcionalidades da conta ######################

#Carlos
@app.route("/login", methods=["GET","POST"])
def login():
    #Pegar os dados do usuario e checar
    if request.method == "POST":
        email = request.form['loginEmail']
        senha = request.form['loginPassword']
        controladora = CntrlSConta()
        user = controladora.logar(email,senha)
        if user:
            session["userID"] = user.getId()
            session["nomeUser"] = user.getNome()
            session["emailUser"] = user.getEmail()
            session["passwordUser"] = user.getSenha()

            #session['authenticated'] = True

            return jsonify({"message":"login concluido","status":"success","redirect":url_for('home')}),200
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
            session["userID"] = user.getId()
            session["nomeUser"] = user.getNome()
            session["emailUser"] = user.getEmail()
            session["passwordUser"] = user.getSenha()
            return jsonify({"message":"sucesso ao registrar","status":"success","redirect":url_for('home')}),200
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
@app.route("/Usuario")
def UsuarioPage():
    pass

###########   Funcionalidades da aplicação (musica) ######################

#HomePage do site
#Ricardo
@app.route("/")
def home():
    return redirect(url_for('home_redirect'))

@app.route("/home", methods=["GET", "POST"])
def home_redirect():
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "login":
            print("\n>>> Teste no Login\n")
            return redirect(url_for('login'))
        elif action == "register":
            return redirect(url_for('registrar'))
        elif action == "playlist":
            if 'userID' in session and session['userID'] is not None:
                return redirect(url_for('playlistUsuario'))
            else:
                return redirect(url_for('login'))


    return render_template("home.html")


#Ricardo
@app.route("/navegar")
def navegarMusicas():
    #endpoint para podermos navegar pelos generos das musicas
    pass

#################################################

#Logica a ser desenvolvida em controladora e redirecionamento 
#Ricardo/Carlos
@app.route("/playlistUsuario")
def PlaylistUsuario():
    #Fazer select do banco de dados das playlist criadas pelo usuario
    #CRUD Completo
    idUsuario = session["userID"]
    controladora = CntrlSPlaylist()
    #playlists = controladora.pesquisarPlaylist(idUsuario)
    playlists = True
    #criar o redirecionamento para o PlaylistUsuario/idPlaylist

    return render_template("playlistSaves.html",Playlist=playlists)

#Carlos
@app.route("/playlistUsuario/{id_playlist}",methods=["GET","POST"])
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
            #controladora.adicionarMusica(nameMusic,nameArtista,id)
        else:
            #remover musica da playlist
            #controladora.removerMusica(nameMusic,nameArtista,id)
            pass
    else:
        #Fazer select do banco de dados
        musicasPlaylist = controladora.pesquisarMusicas(id_playlist)
        title = "Rock"
        return render_template("playlist.html",MusicasPlaylist=musicasPlaylist,Title=title)
    
############################################    

#Ricardo
@app.route("/album")
def albumPage():
    #listar os albuns da aplicacao (todos)
    pass

#Ricardo
@app.route("/album/{idAlbum}")
def albumMusicas(idAlbum):
    #listar todas as musicas vinculadas à aquele album
    #Somente seleção
    pass

#Ricardo
#Esse endpoint fica a seu criterio se é necessario ou não
@app.route("/albumSalvos")
def albumSalvos():
    #listar todos os albuns salvos pelo usuario
    #Crud de adição,seleção e remoção
    #Pode fazer o redirecionamento para album/idAlbum ao ser clicado
    pass

###############################################################

#Carlos
#Estou pensando em criar um endpoint para artista 
@app.route("/artista")
def artistaPage():
    #Seleção de artistas salvas na aplicação
    pass

#Carlos
#Informações do artista escolhido, como albuns(pode redirecionar para pagina de album) e hits do artista
@app.route("/artista/{idArtista}")
def artistaPageSongs(idArtista):
    #Selecao de albuns vinculados ao artista, hits
    pass

if __name__ == "__main__":
    app.run(debug=True, port=8000)
