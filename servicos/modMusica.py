from dominios.music import Cancao

class CntrlSPlaylist:
    def __init__(self):
        self.music = Cancao()

    def adicionarMusica(self,musica,artista,idPlaylist):
        #adiciona uma musica aquela playlist
        pass

    def removerMusica(self,musica,artista,idPlaylist):
        #remove a musica daquela playlist
        pass

    def pesquisarMusicas(self,idPlaylist):
        #pesquisar todas as musicas vinculadas aquela playlist
        pass

    def lerPlaylist(self,idPlaylist):
        #retorna todos os atributos da tabela playlist
        pass

    def adicionarPlaylist(self,idUsuario,idPlaylist):
        #Cria uma playlist na lista de playlists do usuario
        pass

    def editarPlaylist(self,idUsuario,idPlaylist):
        #Permite editar a playlist do usuario (nome,miniatura etc)
        pass

    def removerPlaylist(self,idUsuario,idPlaylist):
        #Remove da lista de playlists do usuario a playlist escolhida
        pass

    def pesquisarPlaylist(self,idUsuario):
        #lista todas as playlists criadas pelo usuario
        pass

    #Essa funcao pode ser removida se não for necessaria
    def pesquisarPlaylistSaves(self,idUsuario):
        #pesquisar playlists salvas pelo usuario(não foram criadas por ele)
        pass

#Classe que manipula o banco de dados
class ContainerPlaylist:
    def adicionarMusica(self,musica,artista,idPlaylist):
        pass

    def removerMusica(self,musica,artista,idPlaylist):
        pass

    def pesquisarMusica(self,idPlaylist):
        pass

    def adicionarPlaylist(self,idPlaylist):
        pass

    def editarPlaylist(self,idPlaylist):
        pass

    def removerPlaylist(self,idUsuario):
        pass

    def pesquisarPlaylist(self,idUsuario):
        pass

    def pesquisarPlaylistSaves(self,idUsuario):
        pass