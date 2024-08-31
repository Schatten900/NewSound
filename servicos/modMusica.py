from dominios.music import Cancao
from dominios.bancoDef import executeQuery
from servicos.modArtistas import CntrlSArtista
class CntrlSMusica:
    def __init__(self):
        self.music = Cancao()

    def getMusic(self):
        return self.music

    def adicionarMusica(self,nomeMusica,artista,codUser,musicaMP3=None):
        #Adiciona musica ao banco de dados Musica ou somente em musicas salvas
        try:
            musica = self.getMusic()
            existe = musica.setCancao(artista,nomeMusica)
            if not existe:
                print("Nao existe essa musica")
                return False
            
            container = ContainerMusica()
            # Se a musica existe no banco, adicione ela a musicaSalvas
            if self.pesquisarMusica(nomeMusica,artista):
                print("Devemos adicionar a musica ja existente")
                return container.adicionarMusicaSalvas(nomeMusica,artista)
    
            else:
                print("Musica nao existe na BD, vamos adiciona-la")
                #Musica nao existe no banco de dados
                nomeAlbum = musica.getAlbum()
                print(f"Nome do album: {nomeAlbum}")
                artistaMiniatura = musica.getArtista().getMiniatura()
                #Fazer o insert em Artistas
                cntrlArtista = CntrlSArtista()
                result,codArtista = cntrlArtista.pesquisarArtista(nomeMusica,artista)
                print(result,codArtista)
                if not result:
                    if artistaMiniatura:
                    #Caso nao haja artista no banco
                        print("Existe Miniatura")
                        result,codArtista = cntrlArtista.adicionarArtista(artista,artistaMiniatura)
                    else:
                        print("Nao existe miniatura")
                        result,codArtista = cntrlArtista.adicionarArtista(artista)

                    print("Apos a adicao ficou: ")
                    print(result,codArtista)
                #Se a musica estiver vinculada a um album
                if nomeAlbum:
                    print(f"Nome do album: {nomeAlbum}")
                    #Fazer o INSERT em album
                    capaAlbum= musica.getCapaAlbum()
                    resultAlbum,codAlbum = cntrlArtista.pesquisarAlbum(codArtista,nomeAlbum)
                    print(resultAlbum,codAlbum)

                    if not resultAlbum:
                        #Adicionar album caso nao haja no banco e pegar ID
                        resultAlbum,codAlbum = cntrlArtista.adicionarAlbum(nomeAlbum,codArtista,capaAlbum)
                        print("Apos a adicao do album ficou: ")
                        print(resultAlbum,codAlbum)
        
                    #Adicionar no banco de dados a musica que tenha album vinculado
                    resultMusica,codMusica = container.adicionarMusicasBD(nomeMusica,musicaMP3,codAlbum)
                    print("Adicionou a musica na BD")
                    print(resultMusica,codMusica)
                    if resultMusica:
                        #Adiciona a musica salva pelo usuario 
                        print("existe na MusicaBD")
                        return container.adicionarMusicaArtista(codMusica,codArtista) and container.adicionarMusicaSalvas(codUser,codMusica)
                    print("Deu erro na BD")
                    return False
                else:
                    #Adicionar no banco de dados a musica que nao tenha album vinculado
                    resultMusica,codMusica = container.adicionarMusicasBD(nomeMusica,musicaMP3)
                    print("Adicionou a musica na BD sem album")
                    print(resultMusica,codMusica)
                    if resultMusica:
                        print("Adicionou na musicaBD sem album")
                        #Adiciona a musica salva pelo usuario 
                        return container.adicionarMusicaArtista(codMusica,codArtista) and container.adicionarMusicaSalvas(codUser,codMusica)
                    print("Deu erro ao adicionar sem album")
                    return False

        except ValueError as e:
            print(f"Erro ao adicionar no banco de dados: {e}")
            return False
        
    def obterMP3(self,idMusica):
        container = ContainerMusica()
        return container.obterMP3(idMusica)

    def removerMusica(self,nomeMusica,artista):
        #Remove musica das musicas salvas pelo usuario
        pass

    def listarMusicas(self,idUser):
        #Lista todas as musicas salvas pelo usuario
        container = ContainerMusica()
        return container.listarMusicas(idUser)

    def pesquisarMusica(self,nomeMusica,artista):
        #Pesquisa se a musica existe no banco de dados ou nao
        container = ContainerMusica()
        return container.pesquisarMusica(nomeMusica,artista)

class ContainerMusica:
    def adicionarMusicaSalvas(self,codUser,codMusica):
        #Retorna True ou False
        try:
            QUERY = """
            INSERT INTO MusicasSalvas (Coduser,CodMusica) VALUES (%s,%s)
            """
            params = (codUser,codMusica)
            executeQuery(QUERY,params)
            return True

        except ValueError as e:
            print(f"Erro ao inserir no banco MusicasSalvas: {e}")
            return False

    def adicionarMusicasBD(self,nomeMusica,MP3,codAlbum=None):
        try:
            #Fazer o insert em Musica e retornar o codMusica
            if codAlbum:
                QUERY = """
                INSERT INTO Musica (CodAlbum,Nome,MP3) VALUES (%s,%s,%s)
                """
                params = (codAlbum,nomeMusica,MP3)
            else:
                QUERY = """
                INSERT INTO Musica (Nome,MP3) VALUES (%s,%s)
                """
                params = (nomeMusica,MP3)
            
            codMusica = executeQuery(QUERY,params)
            if codMusica:
                return True,codMusica
            return False,-1

        except ValueError as e:
            print(f"Erro ao inserir no banco Musica: {e}")
            return False
        
    def adicionarMusicaArtista(self,codMusica,codArtista):
        #Vincular os codigos em ArtistasMusica e retorna true ou false
        try:
            QUERY = """
            INSERT INTO ArtistaMusica (CodMusica,CodArtista) VALUES (%s,%s)
            """
            params = (codMusica,codArtista)
            executeQuery(QUERY,params)
            return True
        
        except ValueError as e:
            print(f"erro ao inserir no banco MusicaArtista: {e}")
            return False

    def obterMP3(self,idMusica):
        try:
            QUERY = """
            SELECT MP3 FROM Musica WHERE CodMusica = %s
            """
            params = (idMusica,)
            mp3 = executeQuery(QUERY,params)
            if mp3:
                return mp3[0]
            return None 

        except ValueError as e:
            print(f"Erro ao obter mp3: {e}")
            return None

    def pesquisarMusica(self,nomeMusica,artista):
        try:
            QUERY = """
            SELECT M.Nome,A.Nome
            FROM ArtistaMusica as AM
            INNER JOIN Musica as M ON M.CodMusica = AM.CodMusica
            INNER JOIN Artista as A ON A.CodArtista = AM.CodArtista
            WHERE M.Nome = %s AND A.Nome = %s
            """
            params = (nomeMusica,artista,)
            result = executeQuery(QUERY,params)
            if result:
                return True
            return False

        except ValueError as e:
            print(f"Erro ao pesquisar pela musica: {e}")
            return False
        
    def listarMusicas(self,idUser):
        try:
            QUERY = """
            SELECT M.CodMusica,M.Nome,A.Nome,M.MP3
            FROM MusicasSalvas as MS
            INNER JOIN Musica as M ON M.CodMusica = MS.CodMusica
            INNER JOIN ArtistaMusica as AM ON M.CodMusica = AM.CodMusica
            INNER JOIN Artista as A ON A.CodArtista = AM.CodArtista
            WHERE CodUser = %s;
            """
            params = (idUser)
            result = executeQuery(QUERY,params)
            if result:
                return result
            return None

        except ValueError as e:
            print(f"Erro ao pesquisar musicas do usuario {e}")
            return None