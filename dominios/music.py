import os
import tempfile
import spotipy
import pygame
from spotipy.oauth2 import SpotifyClientCredentials
from pygame import mixer
from dominios.user import dominio
from dotenv import load_dotenv

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
                    artistaImagem = artist["images"][0]["url"]
                    self.miniaturaArtista = artistaImagem

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
        self.generos = []

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

            songName = track["name"]
            songArtist = track["artists"][0]["name"]
            album = track["album"]["name"]
            artistaId = track["artists"][0]["id"]

            if songArtist.lower() == artista.lower() and songName.lower() == musica.lower():
                self.musica.set(musica)
                self.artista.set(artista)
                artistaInfo = sp.artist(artistaId)
                generos = artistaInfo["genres"]
                if album:
                    self.album = album
                    if "images" in track["album"] and track["album"]["images"]:
                        capaAlbum = track["album"]["images"][0]["url"]
                        self.capaAlbum = capaAlbum 
                if generos:
                    for genero in generos:
                        self.generos.append(genero)
                        print(genero)
                    
                return True
            return False
        
        except ValueError as e:
            print(f"Erro ao procurar pela musica: {e}")
            return False
    
#Essa classe nao é mais necessaria, pois deve tocar no navegador... mas vou deixar ai por enquanto
class AcoesMusicas:
    def tocarMusica(self,mp3Data):
        #Criar um arquivo temporario para armazenar o blob
        with tempfile.NamedTemporaryFile(delete=False,suffix=".mp3") as temp_mp3_file:
            temp_mp3_file.write(mp3Data)
            temp_mp3_file_path = temp_mp3_file.name

        #Tocar a musica usando o arquivo temporario
        try:
            mixer.init()
            mixer.music.load(temp_mp3_file_path)
            mixer.music.play()

            #Espera ate a musica terminar
            while mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:
            print(f"Erro ao tocar a musica {e}")

        finally:
            #Apagar o arquivo temporario
            try:
                os.remove(temp_mp3_file_path)
            except OSError as e:
                print(f"Erro ao tentar apagar o arquivo temporario {e}")