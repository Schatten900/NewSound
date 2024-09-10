from dominios.music import Cancao
from dominios.bancoDef import executeQuery

class CntrlSPlaylist:
    def __init__(self):
        self.music = Cancao()

    def getMusic(self):
        return self.music

    def adicionarMusicaPlaylist(self, artista, nomeMusica, codMusica, codPlaylist):
        #adiciona uma musica aquela playlist
        try:
            musica = self.getMusic()
            existe = musica.setCancao(artista, nomeMusica)
            if not existe:
                print("Nao existe essa musica")
                return False

            container = ContainerPlaylist()
            # Se a musica existe no banco, adicione ela a musicaSalvas
            if self.pesquisarMusica(codMusica) and codMusica not in self.pesquisarMusicas(codPlaylist):

                return container.adicionarMusica(codMusica, codPlaylist)

            #Caso em que a música já está na playlist ou não está cadastrada
            return False

        except ValueError as e:
            print(f"Erro ao adicionar no banco de dados: {e}")
            return False

    def removerMusica(self, codMusica, codPlaylist):
        #remove a musica daquela playlist
        container = ContainerPlaylist()
        return container.removerMusica(codMusica, codPlaylist)

    def pesquisarMusica(self, codMusica):
        #retorna o codigo da musica fornecido, caso a música esteja cadastrada no banco
        container = ContainerPlaylist()
        return container.pesquisarMusica(codMusica)

    def pesquisarMusicas(self,codPlaylist):
        #pesquisar todas as musicas vinculadas aquela playlist
        container = ContainerPlaylist()
        return container.pesquisarPlaylist(codPlaylist)

    def lerPlaylist(self,idPlaylist):
        #retorna todos os atributos da tabela playlist
        pass

    def criarPlaylist(self,nomePlaylist, codUser):
        #Cria uma playlist na lista de playlists do usuario
        container = ContainerPlaylist()
        return container.criarPlaylist(nomePlaylist, codUser)

    def editarPlaylist(self,idUsuario,idPlaylist):
        #Permite editar a playlist do usuario (nome,miniatura etc)
        pass

    def removerPlaylist(self, codPlaylist, codUser):
        #Remove da lista de playlists do usuario a playlist escolhida
        container = ContainerPlaylist()
        return container.removerPlaylist(codPlaylist, codUser)

    def pesquisarPlaylist(self, codUser):
        #lista todas as playlists criadas pelo usuario
        container = ContainerPlaylist()
        return container.pesquisarPlaylist(codUser)

#Classe que manipula o banco de dados
class ContainerPlaylist:
    def adicionarMusica(self, codMusica, codPlaylist):
        #Retorna True ou False
        try:
            QUERY = """
            INSERT INTO PlaylistMusica (CodMusica, CodPlaylist) VALUES (%s,%s)
            """
            params = (codMusica, codPlaylist)
            executeQuery(QUERY,params)
            return True

        except ValueError as e:
            print(f"Erro ao inserir no banco MusicasSalvas: {e}")
            return False

    def removerMusica(self, codMusica, codPlaylist):
        try:
            QUERY = """
            DELETE FROM PlaylistMusica 
            WHERE CodMusica = %s AND CodPlaylist = %s
            """
            params = (codMusica, codPlaylist)
            executeQuery(QUERY,params)
            return True

        except ValueError as e:
            print(f"Erro ao inserir no banco MusicasSalvas: {e}")
            return False

    def pesquisarMusicas(self, codPlaylist):
        try:
            QUERY = """
            SELECT CodMusica FROM PlaylistMusica WHERE CodPlaylist = %s
            """
            params = (codPlaylist)
            return executeQuery(QUERY,params)

        except ValueError as e:
            print(f"Erro ao inserir no banco MusicasSalvas: {e}")
            return False

    def pesquisarMusica(self,codMusica):
        try:
            QUERY = """
            SELECT CodMusica FROM Musica WHERE CodMusica = %s
            """
            params = (codMusica)
            return executeQuery(QUERY,params)

        except ValueError as e:
            print(f"Erro ao inserir no banco MusicasSalvas: {e}")
            return False

    def criarPlaylist(self,nomePlaylist, codUser):
        try:
            QUERY1 = """
            INSERT INTO Playlist (Nome) VALUES (%s)
            """
            params1 = (nomePlaylist)
            codPlaylist = executeQuery(QUERY1,params1)
            if not codPlaylist:
                return False

            QUERY2 = """
            INSERT INTO PlaylistUsuario (CodUser, CodPlaylist) VALUES (%s,%s)
            """
            params2 = (codUser, codPlaylist)
            executeQuery(QUERY2,params2)
            return True

        except ValueError as e:
            print(f"Erro ao inserir no banco MusicasSalvas: {e}")
            return False

    def editarPlaylist(self,idPlaylist):
        pass

    def removerPlaylist(self, codPlaylist, codUser):
        try:
            #Remove aquela playlist, assim como os seus relacionamentos, com Musicas e Usuarios

            QUERY2 = """
            DELETE FROM PlaylistUsuario 
            WHERE CodUser = %s AND CodPlaylist = %s
            """
            params2 = (codUser, codPlaylist)
            executeQuery(QUERY2, params2)

            QUERY3 = """
            DELETE FROM PlaylistMusica 
            WHERE CodPlaylist = %s
            """
            params3 = (codPlaylist)
            executeQuery(QUERY3, params3)
        
            QUERY1 = """
            DELETE FROM Playlist 
            WHERE CodPlaylist = %s
            """
            params1 = (codPlaylist)
            executeQuery(QUERY1, params1)
            return True

        except ValueError as e:
            print(f"Erro ao inserir no banco MusicasSalvas: {e}")
            return False

    def pesquisarPlaylist(self, codUser):
        try:
            QUERY = """
            SELECT P.CodPlaylist,P.Nome 
            FROM Playlist P
            INNER JOIN PlaylistUsuario PU ON P.CodPlaylist = PU.CodPlaylist
            WHERE PU.CodUser = %s
            """
            params = (codUser)
            return executeQuery(QUERY, params)

        except ValueError as e:
            print(f"Erro ao inserir no banco MusicasSalvas: {e}")
            return False

    def pesquisarPlaylistSaves(self,idUsuario):
        pass