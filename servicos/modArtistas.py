from dominios.music import Cancao
from dominios.bancoDef import executeQuery

class CntrlSArtista:
    def __init__(self):
        self.cancao = Cancao()

    def pesquisarArtistas(self):
        #Pesquisa todos os artistas no banco de dados
        container = ContainerArtista()
        return container.pesquisarArtistas()

    def pesquisarAlbuns(self,idArtista):
        #Pesquisa todos os albuns relacionados ao artista x
        pass

    def pesquisarArtista(self,musicaNome,artista):
        #Pesquisar pelo artista especifico no banco de dados
        container = ContainerArtista()
        return container.pesquisarArtista(musicaNome,artista)

    def musicasAlbuns(self,idAlbum):
        #Pesquisa as musicas vinculadas ao album x 
        pass

    def adicionarArtista(self,nomeArtista,artistaMiniatura=None):
        #Adicionar o artista no banco de dados
        container = ContainerArtista()
        return container.adicionarArtista(nomeArtista,artistaMiniatura)
    
    def adicionarAlbum(self,nomeAlbum,idArtista,capaAlbum):
        #Adiciona o album no banco de dados
        controladora = ContainerArtista()
        return controladora.adicionarAlbum(nomeAlbum,idArtista,capaAlbum)
    
    def pesquisarAlbum(self,codArtista,nomeAlbum):
        container = ContainerArtista()
        return container.pesquisarAlbum(codArtista,nomeAlbum)


class ContainerArtista:
    def pesquisarArtistas(self):
        try:
            QUERY = """
            SELECT * FROM Artista
            """
            result = executeQuery(QUERY)
            if result:
                print(result)
                return result
            return None

        except ValueError as e:
            print(f"Erro ao pesquisar artistas {e}")
            return None

    def pesquisarArtista(self,musicaNome,artista):
        #Pesquisar pelo artista especifico no banco de dados
        try:
            QUERY = """
            SELECT A.CodArtista 
            FROM Artista as A
            INNER JOIN ArtistaMusica as AM ON A.CodArtista = AM.CodArtista
            INNER JOIN Musica as M ON M.CodMusica = AM.CodMusica
            WHERE M.Nome = %s AND A.Nome = %s
            """
            params = (musicaNome,artista)
            result = executeQuery(QUERY,params)
            if result:
                return True,result[0][0]
            return False,-1
        
        except ValueError as e:
            print(e)
            return False,-1
        
    def adicionarAlbum(self,nomeAlbum,codArtista,capaAlbum):
        try:
            QUERY = """
            INSERT INTO Album (CodArtista,Nome,CapaAlbum) VALUES (%s,%s,%s)
            """
            params = (codArtista,nomeAlbum,capaAlbum)
            idAlbum = executeQuery(QUERY,params)
            if idAlbum:
                return True,idAlbum
            return False,-1

        except ValueError as e:
            print(f"Erro ao tentar inserir em Album: {e}")
            return False,-1
        
    def pesquisarAlbum(self,codArtista,nome):
        try:
            QUERY= """
            SELECT CodAlbum FROM Album WHERE CodArtista= %s AND Nome = %s 
            """
            params = (codArtista,nome)
            result = executeQuery(QUERY,params)
            if result:
                return True,result[0]
            else:
                return False,-1

        except ValueError as e:
            print(f"Erro ao procurar em Album: {e}")
            return False,-1
        
    def adicionarArtista(self,nomeArtista,artistaMiniatura=None):
        try:
            if artistaMiniatura:
                QUERY = """
                INSERT INTO Artista (Nome,ArtistaMiniatura) VALUES (%s,%s)
                """
                params = (nomeArtista,artistaMiniatura)
            else:
                QUERY = """
                INSERT INTO Artista (Nome) VALUES (%s)
                """
                params = (nomeArtista,)

            idArtista = executeQuery(QUERY,params)
            if idArtista:
                return True,idArtista
            else:
                return False,-1

        except ValueError as e:
            print(f"Erro ao inserir em Artistas: {e}")
            return False,-1