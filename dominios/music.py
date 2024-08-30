import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pygame import mixer
from dominios.user import dominio
from dotenv import load_dotenv
import os
import requests

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
        musicName = valor.lower()
        try:
            results = sp.search(q=musicName,type="track",limit=1)
            tracks = results['tracks']['items'][0]
            songName = tracks["name"]
            if songName:
                return True
            return False
        except ValueError as e:
            print(f"Erro ao validar Musica: {e}")   
            return False

class Artista(dominio):
    def __init__(self):
        self.miniaturaArtista = ""

    def getMiniatura(self):
        return self.miniaturaArtista

    def _validar(self,valor):
        artist_name = valor.lower()
        sp = getSpotifyConnection()
        try:
            results = sp.search(q=artist_name,type="artist",limit=1)
            artist = results["artists"]["items"][0]
            if not artist:
                return False
            
            if artist["name"]:
                if "images" in artist and artist["images"]:
                    self.miniaturaArtista = artist["images"][0]["url"]

                return True
            return False
        
        except ValueError as e:
            print(f"Erro ao validar Artista {e}")
            return False
        

class Cancao:
    def __init__(self):
        self.artista = Artista()
        self.musica = Musica()
        self.album = ""
        self.capaAlbum = ""

    def getArtista(self):
        return self.artista
    
    def getMusica(self):
        return self.musica
    
    def getAlbum(self):
        return self.album
    
    def getCapaAlbum(self):
        return self.capaAlbum
    
    def setCancao(self,artista,musica):
        sp = getSpotifyConnection()
        try:
            results = sp.search(q=musica,type="track",limit=1)
            tracks = results['tracks']['items']
            if not tracks:
                print("Nao existe essa track")
                return False
            track = tracks[0]
            #print(track)

            songName = track["name"]
            songArtist = track["artists"][0]["name"]
            album = track["album"]["name"]

            if songArtist.lower() == artista.lower() and songName.lower() == musica.lower():
                self.musica.set(musica)
                self.artista.set(artista)
                if album:
                    self.album = album
                    #print(self.album)
                    if "images" in track["album"] and track["album"]["images"]:
                        capaAlbum = track["album"]["images"][0]["url"]
                        self.capaAlbum = capaAlbum 
                        #print(self.capaAlbum)
                return True
            return False
        
        except ValueError as e:
            print(f"Erro ao procurar pela musica: {e}")
            return False
    

    def pegarCancao(self,idMusica):
        #Funcao para pegar o .mp3 pelo id(click do usuario)
        pass

    def tocarPlay(self,arquivo):
        #arquivo é o .mp3 pego no banco de dados
        try:
            mixer.init()
            mixer.music.load(arquivo)
            mixer.music.play()
            input("Pressione qualquer tecla para parar")
            mixer.music.stop()
        except ValueError as e:
            print(f"Erro ao tocar a musica {e}")


