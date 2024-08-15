from dominios.music import Cancao

class CntrlSPlaylist:
    def __init__(self):
        self.music = Cancao()

    def adicionarMusica(self,musica,artista,idUsuario):
        pass

    def removerMusica(self,musica,artista,idUsuario):
        pass

    def pesquisarMusica(self,idUsuario):
        pass

    def adicionarPlaylist(self,idUsuario):
        pass

    def editarPlaylist(self,idUsuario):
        pass

    def removerPlaylist(self,idUsuario):
        pass

    #pesquisar playlists criadas pelo usuario
    def pesquisarPlaylist(self,idUsuario):
        pass

    #pesquisar playlists salvas pelo usuario
    def pesquisarPlaylistSaves(self,idUsuario):
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