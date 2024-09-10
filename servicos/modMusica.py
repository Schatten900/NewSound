from dominios.music import Cancao
from dominios.bancoDef import executeQuery
from servicos.modArtistas import CntrlSArtista
class CntrlSMusica:
    def __init__(self):
        self.music = Cancao()

    def getMusic(self):
        return self.music

    def adicionarMusicaBD(self,nomeMusica,artista,musicaMP3):
        #Adiciona musica ao banco de dados Musica 
        try:
            musica = self.getMusic()
            existe = musica.setCancao(artista,nomeMusica)
            if not existe:
                print("Nao existe essa musica")
                return False
            
            container = ContainerMusica()
            # Se a musica existe no banco, adicione ela a musicaSalvas
            result,CodMusica = self.pesquisarMusica(nomeMusica,artista)
            if result:
                print(f"Codigo obtido: {CodMusica}")
                print("Já existe a musica no BD")
                return True

            else:
                print("Musica nao existe na BD, vamos adiciona-la")
                #Musica nao existe no banco de dados

                nomeAlbum = musica.getAlbum()
                print(f"Nome do album: {nomeAlbum}")
                artistaMiniatura = musica.getArtista().getMiniatura()
                #Checar se o artista existe
                cntrlArtista = CntrlSArtista()

                result,codArtista = cntrlArtista.pesquisarArtista(nomeMusica,artista)
                print("Esse é o cod Artista:")
                print(result,codArtista)
                if not result:
                    if artistaMiniatura:
                    #Caso nao haja artista no banco
                        print("Existe Miniatura")
                        result,codArtista = cntrlArtista.adicionarArtista(artista,artistaMiniatura)
                    else:
                        print("Nao existe miniatura")
                        result,codArtista = cntrlArtista.adicionarArtista(artista)
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
                        #Vincula artista e vincula genero
                        result = container.adicionarMusicaArtista(codMusica,codArtista)
                        if not result:
                            return False
                        generos = []
                        auxGeneros = musica.getGeneros()
                        if not auxGeneros:
                            print("Musica nao possui genero")
                            return True
                        #Existe genero e vamos adicionar no bd e vincular a musica
                        generos = auxGeneros
                        for genero in generos:
                            result,codGenero = self.checkGenero(genero)
                            if not result:
                                resultAdd,codGenero = self.adicionarGenero(genero)
                                if not resultAdd:
                                    return False
                            self.adicionarMusicaGenero(codGenero,codMusica)
                        return True
                    
                    print("Deu erro na BD")
                    return False
                else:
                    #Adicionar no banco de dados a musica que nao tenha album vinculado
                    resultMusica,codMusica = container.adicionarMusicasBD(nomeMusica,musicaMP3)
                    print("Adicionou a musica na BD sem album")
                    print(resultMusica,codMusica)
                    if resultMusica:
                        #Vincula artista e vincula genero
                        print("Adicionou na musicaBD sem album")
                        result = container.adicionarMusicaArtista(codMusica,codArtista)
                        if not result:
                            return False
                        generos = []
                        auxGeneros = musica.getGeneros()
                        if not auxGeneros:
                            print("Musica nao possui genero")
                            return True
                        #Existe genero e vamos adicionar no bd e vincular a musica
                        generos = auxGeneros
                        for genero in generos:
                            result,codGenero = self.checkGenero(genero)
                            if not result:
                                resultAdd,codGenero = self.adicionarGenero(genero)
                                if not resultAdd:
                                    return False
                            self.adicionarMusicaGenero(codGenero,codMusica)
                        return True
                            
                    print("Deu erro ao adicionar sem album")
                    return False

        except ValueError as e:
            print(f"Erro ao adicionar no banco de dados: {e}")
            return False
        
    def adicionarMusicaSalvas(self,codUser,codMusica):
        container = ContainerMusica()
        return container.adicionarMusicaSalvas(codUser,codMusica)
        
    def obterMP3(self,idMusica):
        container = ContainerMusica()
        return container.obterMP3(idMusica)

    def removerMusicaSalvas(self,codUsuario,codMusica):
        #Remove musica das musicas salvas pelo usuario
        container = ContainerMusica()
        return container.removerMusicaSalvas(codUsuario,codMusica)

    def listarMusicasSalvas(self,idUser):
        #Lista todas as musicas salvas pelo usuario
        container = ContainerMusica()
        return container.listarMusicasSalvas(idUser)

    def pesquisarMusica(self,nomeMusica,artista):
        #Pesquisa se a musica existe no banco de dados ou nao
        container = ContainerMusica()
        return container.pesquisarMusica(nomeMusica,artista)
    
    def checkMusicaSalvas(self,codUser,codMusica):
        container = ContainerMusica()
        return container.checkMusicaSalvas(codUser,codMusica)
    
    def listarTodasMusicas(self):
        #Lista Nome, Artista, Album, e Genero de todas as musicas cadastradas
        container = ContainerMusica()
        return container.listarTodasMusicas()
    
    def listarMusicasGenero(self, genero):
        #Lista Nome, Artista, Album, e Genero das musicas cadastradas do genero informado
        container = ContainerMusica()
        return container.listarMusicasGenero(genero)
    
    def listarGeneros(self):
        #Lista todos os generos cadastrados no banco (tabela Genero)
        container = ContainerMusica()
        return container.listarGeneros()
    
    def checkGenero(self,genero):
        #Checa se o genero ja existe no banco de dados
        container = ContainerMusica()
        return container.checkGenero(genero)
    
    def adicionarGenero(self,genero):
        #Adiciona o genero no banco de dados
        container = ContainerMusica()
        return container.adicionarGenero(genero)
    
    def adicionarMusicaGenero(self,codGenero,genero):
        #Vincula genero e musica
        container = ContainerMusica()
        return container.adicionarMusicaGenero(codGenero,genero)
    
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

        except Exception as e:
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

        except Exception as e:
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
        
        except Exception as e:
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

        except Exception as e:
            print(f"Erro ao obter mp3: {e}")
            return None

    def pesquisarMusica(self,nomeMusica,artista):
        try:
            QUERY = """
            SELECT M.CodMusica
            FROM ArtistaMusica as AM
            INNER JOIN Musica as M ON M.CodMusica = AM.CodMusica
            INNER JOIN Artista as A ON A.CodArtista = AM.CodArtista
            WHERE M.Nome = %s AND A.Nome = %s
            """
            params = (nomeMusica,artista,)
            result = executeQuery(QUERY,params)
            if result:
                return True,result[0][0]
            return False,-1

        except Exception as e:
            print(f"Erro ao pesquisar pela musica: {e}")
            return False,-1
        
    def listarMusicasSalvas(self,idUser):
        #Lista todas as musicas salvas pelo usuario
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

        except Exception as e:
            print(f"Erro ao pesquisar musicas do usuario {e}")
            return None
        
    def removerMusicaSalvas(self,codUsuario,codMusica):
        try:
            QUERY = """
            DELETE FROM MusicasSalvas WHERE CodUser = %s and CodMusica = %s
            """
            
            print(codMusica,codUsuario)
            params = (codUsuario,codMusica)
            executeQuery(QUERY,params)
            print("removeu")
            return True

        except Exception as e:
            print(f"Houve um erro ao remover: {e}")
            return False
        
    def checkMusicaSalvas(self,codUser,codMusica):
        try:
            QUERY = """
            SELECT * FROM MusicasSalvas WHERE codUser = %s and codMusica = %s
            """
            params = (codUser,codMusica)
            result = executeQuery(QUERY,params)
            if result:
                return True
            return False

        except Exception as e:
            print(f"Erro ao checar a musica existente no usuario {e}")
            return False
        
    def listarTodasMusicas(self):
        try:
            QUERY = """
            SELECT * FROM MusicaNavegar
            """
            result = executeQuery(QUERY)
            print("QUERY result:", result)
            if result:
                return result
            return False

        except Exception as e:
            print(f"Erro ao checar a musica existente no usuario {e}")
            return False
        
    def listarMusicasGenero(self, genero):
        try:
            QUERY = """
            SELECT * FROM MusicaNavegar
            WHERE NomeGenero = %s
            """
            params = (genero)
            result = executeQuery(QUERY, params)
            if result:
                return result[0]
            return None

        except Exception as e:
            print(f"Erro ao checar a musica existente no usuario {e}")
            return None
        
    def listarGeneros(self):
        try:
            QUERY = """
            SELECT Nome FROM Genero
            """
            result = executeQuery(QUERY)
            if result:
                return result
            return False

        except Exception as e:
            print(f"Erro ao checar a musica existente no usuario {e}")
            return False
        
    def checkGenero(self,genero):
        try:
            QUERY = """
            SELECT CodGenero,Nome FROM Genero WHERE Nome = %s
            """
            params = (genero,)
            result = executeQuery(QUERY,params)
            if result:
                return result[0]
            return False,-1

        except Exception as e:
            print(f"Não foi possivel encontrar o genero {e}")
            return False,-1
        
    def adicionarGenero(self,genero):
        try:
            QUERY = """
            INSERT INTO Genero (Nome) VALUES (%s)
            """
            params = (genero,)
            codGenero = executeQuery(QUERY,params)
            if codGenero:
                print(codGenero)
                return True,codGenero
            return False,-1

        except Exception as e:
            print(f"Não foi possivel adicionar o genero {e}")
            return False,-1

    def adicionarMusicaGenero(self,codGenero,codMusica):
        try:
            QUERY = """
            INSERT INTO MusicaGenero (codGenero,codMusica) VALUES (%s,%s)
            """
            params = (codGenero,codMusica,)
            codGenero = executeQuery(QUERY,params)
            print("Vinculado genero com sucesso",codGenero)
            return True

        except Exception as e:
            print(f"Não foi possivel adicionar o genero {e}")
            return False
