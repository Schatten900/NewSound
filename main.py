from flask import Flask, request, render_template, jsonify,url_for, session,redirect,send_file
from servicos.modContas import CntrlSConta
from servicos.modPlaylist import CntrlSPlaylist
from servicos.modMusica import CntrlSMusica
from servicos.modArtistas import CntrlSArtista
from dominios.bancoDef import flaskSecret
import io
import random
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
    if not session["userID"]:
        return redirect(url_for('Login'))
    codUser = session["userID"]
    if request.method == "POST":
        controladora = CntrlSConta()
        action = request.form.get("action")
        if action == "edit":
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
            if controladora.editar(codUser,dicionario):
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
            result = controladora.excluir(codUser)
            if result:
                #Desconectar o usuario
                session.clear()
                return jsonify({"message":"exclusao valida","status":"success","redirect":url_for("Login")}),200
            return jsonify({"message":"Remoção invalida","status":"fail"}),401
        
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
        usuario = controladora.ler(codUser)
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
    if 'userID' not in session or not session["userID"]:
        return redirect(url_for('Login'))
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

@app.route("/navegar", methods=["GET", "POST"])
def NavegarPage():
    
    controladora = CntrlSMusica()
    musicas = controladora.listarTodasMusicas()
    generos = controladora.listarGeneros()
    #generos = [g for g in generos: g[0]]
    codUser = session['userID']
    print("\n>>> Codigo Usuario:", codUser)
    print("\n>>> Generos:", generos[0], type(generos[0]))
    
    
    if request.method == "POST":
        action = request.form.get("action")
        print("action: ", action)
        if action == "salvarMusica":
            #Botão de salvar a musica
            codMusica = request.form.get('codMusica')
            controladora.adicionarMusicaSalvas(codUser, codMusica)

        if action == "add":
            #Cadastrar uma nova musica no BD
            m_nome = request.form.get("musicaName")
            m_artista = request.form.get("artistaName")
            m_enviada = request.files.get("musica")
            #m_genero = 
            #print("\n>>> Form lido:", m_nome, m_artista, type(m_enviada.read()))
            if m_enviada:
                controladora.adicionarMusicaBD(m_nome, m_artista, m_enviada.read())
                #controladora.adicionarGeneroBD(m_genero, codMusica)
                return jsonify({"message":"Adicionado com sucesso","status":"success","redirect":url_for("NavegarPage")}), 200
            
            else:
                return jsonify({"message":"Mp3 não identificado.", "status":"fail"}), 401

    if request.method == "GET":
        #Dropdown pra pegar o genero
        genero_escolhido = request.args.get('genre', 'Todos')  # Default para 'Todos'
        musicas = controladora.listarMusicasGenero(genero_escolhido)

    if not musicas:
        musicas = []

    if not generos:
        generos = []        

    # Renderizar a página HTML e passar a lista de músicas
    return render_template('navegar.html', Musics=musicas, generos=generos, Title="Minhas Músicas")


#Carlos
@app.route("/musicasSalvas",methods=["GET","POST"])
def MusicasSalvas():
    #endpoint para navegar pelas musicas salvas pelo usuario
    #Fazer select do banco de dados
    if 'userID' not in session or not session["userID"]:
        return redirect(url_for('Login'))
    
    codUsuario = session["userID"]
    controladora = CntrlSMusica()
    if request.method == "POST":
        if request.form.get("action"):
            action = request.form.get("action")
            nameMusic = request.form.get("musicaName")
            nameArtista = request.form.get("artistaName")
        else:
            data = request.json
            action = data.get("action")
            print(action)

        if action == "add":
            nameMusic = data.get("musicName")
            nameArtista = data.get("artistaName")
            result,codMusica = controladora.pesquisarMusica(nameMusic,nameArtista)
            if result:
                adicionou = controladora.adicionarMusicaSalvas(codUsuario,codMusica)
                if adicionou:
                    print(adicionou)
                    return jsonify({"message":"Adicionado com sucesso","status":"success","redirect":url_for("MusicasSalvas")}),200
                else:
                    return jsonify({"message":"Houve um erro na adicao","status":"fail"}),401
            else:
                return jsonify({"message":"Musica nao existe no banco","status":"fail"}),401
        
        elif action == "remove":
            data = request.json
            removeMusicaCod = data.get("CodMusic")
            removeu = controladora.removerMusicaSalvas(codUsuario,removeMusicaCod)
            if removeu:
                return jsonify({"message":"Removido com sucesso","status":"success","redirect":url_for("MusicasSalvas")}),200
            return jsonify({"message":"Houve um erro na remoção","status":"fail"}),401

        elif action == "tocar":
            data = request.json
            primeiraMusicaCod = data.get("CodMusic")
            print(f"Codigo obtido: {primeiraMusicaCod}")

            mp3Primeira = controladora.obterMP3(primeiraMusicaCod)
            if not mp3Primeira:
                return jsonify({"message":"ocorreu um erro ao pegar Musica","status":"fail"}),401
            #Tocar a musica que o usuario escolheu
            #Converter o mp3 do BD para arquivo
            mp3Arquivo = mp3Primeira[0]

            #Retorna a musica para o navegador poder reproduzir
            #Codifica em bytes, permite que seja enviado em forma mp3, nao deixa ser baixado e nome do objeto
            return send_file(io.BytesIO(mp3Arquivo), mimetype='audio/mpeg', as_attachment=False, download_name='musica.mp3')
        
        elif action == "embaralhar":
            musicasSalvas = controladora.listarMusicasSalvas(codUsuario)
            musicas = musicasSalvas
            codigos = []
            musicasBlob = []

            #Pega Codigo das musicas
            for musica in musicas:
                codAux = musica[0]
                codigos.append(codAux)

            #Obtem o mp3 das musicas
            for codigo in codigos:
                blobAux = controladora.obterMP3(codigo)
                if not blobAux:
                    return jsonify({"message":"ocorreu um erro ao pegar Musica","status":"fail"}),401
                musicasBlob.append(blobAux[0])
                
            #Faz a logica de embaralhar a lista
            random.shuffle(musicasBlob)

            #Cria um arquivo binario com todas as musicas
            arquivoMusicas = b"".join(musicasBlob)
            
            print("Todas musicas enviadas com sucesso", len(musicas))
            return send_file(io.BytesIO(arquivoMusicas), mimetype='audio/mpeg', as_attachment=False, download_name='musica.mp3')

        else:
            print(f"Acao invalida: {action}")
            return jsonify({"message":"ocorreu um erro inesperado","status":"fail"}),401
    else: 
        musicas = controladora.listarMusicasSalvas(codUsuario)
        if musicas:
            return render_template("musicasSalvas.html",Musicas=musicas)
        return render_template("MusicasSalvas.html")

#################################################

#Logica a ser desenvolvida em controladora e redirecionamento 
#Ricardo
@app.route("/playlistUser")
def PlaylistCriadas():
    #Fazer select do banco de dados das playlist criadas pelo usuario
    #CRUD Completo
    #idUsuario = session["userID"]
    #controladora = CntrlSPlaylist()
    #playlists = controladora.pesquisarPlaylist(idUsuario)e
    #criar o redirecionamento para o PlaylistUsuario/idPlaylist
    if 'userID' not in session or not session["userID"]:
        return redirect(url_for('Login'))

    if request.method == "POST":
        #logica pra pegar o id pelo click na musica
        render_template("playlistUser.html")
    else:
        playlist = [("Panic at Disco","https://via.placeholder.com/150"),("Panic at Disco","https://via.placeholder.com/150")]

    return render_template("playlistCreation.html",Playlist=playlist)

#Ricardo
@app.route("/playlistUser/{id_playlist}",methods=["GET","POST"])
def playlistUsuario(id_playlist):
    #Adicao, seleção e remoção  relacionadas a uma playlist criada pelo usuario
    if 'userID' not in session or not session["userID"]:
        return redirect(url_for('Login'))
    
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
        else:
            pass
    else:
        #Fazer select do banco de dados, musicas e titulo da playlist
        musicasPlaylist = controladora.pesquisarMusicas(id_playlist)
        title = "Rock"
        return render_template("playlistUser.html",MusicasPlaylist=musicasPlaylist,Title=title,idPlaylist=id_playlist)
    
############################################    

#Carlos 
@app.route("/artista",methods=["GET","POST"])
def ArtistasPage():
    #Seleção de artistas salvas na aplicação
    if 'userID' not in session or not session["userID"]:
        return redirect(url_for('Login'))
    if request.method == "POST":
        data = request.json
        action = data.get("action")
        if action == "enviar":
            codArtista = data.get("codArtista")
            if codArtista:
                return jsonify({"message":"Redirecionado com sucesso","status":"success","redirect":url_for("ArtistasPageSongs",idArtista = codArtista)}),200
            return jsonify({"message":"Erro ao redirecionar","status":"fail"}),401
    else:
        controladora = CntrlSArtista()
        artistas = controladora.pesquisarArtistas()
        if artistas:
            return render_template("artista.html",Artistas=artistas)
        return render_template("artista.html")

#Carlos
@app.route("/artista/<idArtista>",methods=["GET","POST"])
def ArtistasPageSongs(idArtista):
    #Logica para pesquisar albuns do artista
    #nome do artista,album,imagem
    if 'userID' not in session or not session["userID"]:
        return redirect(url_for('Login'))
    
    codUsuario = session["userID"]
    controladora = CntrlSArtista()
    controladoraMusicas = CntrlSMusica()
    if request.method == "POST":
        data = request.json
        action = data.get("action")
        if action == "tocar":
            primeiraMusicaCod = data.get("CodMusic")
            print(f"Codigo obtido: {primeiraMusicaCod}")

            mp3Primeira = controladoraMusicas.obterMP3(primeiraMusicaCod)
            if not mp3Primeira:
                return jsonify({"message":"ocorreu um erro ao pegar Musica","status":"fail"}),401
            #Tocar a musica que o usuario escolheu
            #Converter o mp3 do BD para arquivo
            mp3Arquivo = mp3Primeira[0]

            #Retorna a musica para o navegador poder reproduzir
            #Codifica em bytes, permite que seja enviado em forma mp3, nao deixa ser baixado e nome do objeto
            return send_file(io.BytesIO(mp3Arquivo), mimetype='audio/mpeg', as_attachment=False, download_name='musica.mp3')
        
        if action == "favoritar":
            primeiraMusicaCod = data.get("CodMusic")
            adicionou = controladoraMusicas.adicionarMusicaSalvas(codUsuario,primeiraMusicaCod)
            if adicionou:
                print("Favoritado com sucesso")
                return jsonify({"message":"favoritou com sucesos","status":"success","redirect":url_for("ArtistasPageSongs",idArtista = idArtista)}),200
            return jsonify({"message":"favoritou nao deu certo","status":"fail"}),401

    else:
        #Logica para pesquisar albuns e musicas vinculadas a aquele album por meio de uma view
        informacoes = controladora.viewAlbumMusica(idArtista)
        if informacoes:
            #Criar um dicionario de albuns e musicas
            album = {}
            capas = []
            for info in informacoes:
                musicaNome = info[0]
                musicaArtista = info[1]
                albumNome = info[2]
                capaAlbum = info[3]
                codMusica = info[5]
                musicaInfo = (musicaNome,musicaArtista,codMusica)

                #Checa se a tupla de informações existe dentro do album
                if albumNome not in album:
                    album[albumNome] = []

                if musicaInfo not in album[albumNome]:
                    album[albumNome].append(musicaInfo)

                if capaAlbum not in capas:
                    capas.append(capaAlbum)

            return render_template("artistaAlbum.html",informacoes=album,titulo=musicaArtista,listaCapa=capas,codArtista=idArtista)
        return render_template("ArtistaAlbum.html") 

if __name__ == "__main__":
    app.run(debug=True, port=8000)
