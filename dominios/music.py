import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dominios.user import dominio
from dotenv import load_dotenv
import os


dotenv_path='.env'
load_dotenv(dotenv_path=dotenv_path)

def getSpotifyConnection():
    #dados de conexao com a api
    clientID = os.getenv("API_ID")
    clientKEY = os.getenv("API_KEY")
    auth_manager= SpotifyClientCredentials(client_id=clientID, client_secret=clientKEY)
    #retornar a conexao com a api
    return spotipy.Spotify(auth_manager=auth_manager) 

class Musica(dominio):
    def _validar(self,valor):
        sp = getSpotifyConnection()
        musicName = valor
        results = sp.search(q=musicName,type="track",limit=1)
        tracks = results['tracks']['items'][0]
        songName = tracks["name"]
        if songName:
            return True
        return False

class Artista(dominio):
    def _validar(self,valor):
        artist_name = valor
        sp = getSpotifyConnection()
        results = sp.search(q=artist_name,type="artist")
        artist = results["artists"]["items"][0]
        if artist["name"]:
            return True
        return False

class Cancao:
    def __init__(self):
        self.artista = Artista()
        self.musica = Musica()

    def getArtista(self):
        return self.artista
    
    def getMusica(self):
        return self.musica
    
    def setCancao(self,artista,musica):
        sp = getSpotifyConnection()

        results = sp.search(q=musica,type="track",limit=1)
        tracks = results['tracks']['items'][0]
        songName = tracks["name"]
        songArtist = tracks["artists"][0]["name"]

        if songArtist.lower() == artista.lower() and songName.lower() == musica.lower():
            self.musica.set(musica)
            self.artista.set(artista)


