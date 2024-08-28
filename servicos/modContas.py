from dominios.user import Usuario,Email,Nome,Senha
from dominios.bancoDef import executeQuery

#Chamada na camada de apresentação para efetuar o serviço
class CntrlSConta:
    def __init__(self):
        self.user = Usuario()

    def getConta(self):
        return self.user
    
    def setConta(self,conta):
        self.user = conta

    def cadastrar(self,nome,email,senha):
        #Checar se os valores sao validos
        emailAux = Email()
        emailAux.set(email)
        if not emailAux.get():
            return None

        nomeAux = Nome()
        nomeAux.set(nome)
        if not nomeAux.get():
            return None

        senhaAux = Senha()
        senhaAux.set(senha)
        if not senhaAux.get():
            return None

        conta = self.getConta()
        container = ContainerConta()
        conta = container.cadastrar(nome,email,senha)
        if conta:
            return conta
        else:
            return None

    def logar(self,email,senha):
        #Checar se os valores sao validos
        emailAux = Email()
        emailAux.set(email)
        if not emailAux.get():
            return None
        
        senhaAux = Senha()
        senhaAux.set(senha)
        if not senhaAux.get():
            return None

        conta = self.getConta()
        container = ContainerConta()
        conta = container.logar(email,senha)
        if conta:
            return conta
        return None

    def ler(self,email):
        container = ContainerConta()
        existe = container.ler(email)
        if existe:
            return existe
        else:
            return None

    #usar dicionario para poder editar os valores recebidos
    def editar(self,id,dicionario):
        container = ContainerConta()
        if container.editar(id,dicionario):
            return True
        return False

    def excluir(self):
        conta = self.getConta()
        email = conta.getEmail().get()
        container = ContainerConta()
        container.excluir(email)

#Acessa o banco de dados e faz as operacoes
class ContainerConta:
    def cadastrar(self,nome,email,senha):
        #logica para cadastrar no banco
        try:
            QUERY = """
            INSERT INTO Usuario (Nome,Senha,Email) VALUES (%s,%s,%s)
            """
            params = (nome,senha,email)
            #pega o id do usuario e faz a insercao em Usuario
            id = executeQuery(QUERY,params)
            user = Usuario()
            user.setUsuario(nome,email,senha,id)
            if user:
                return user
            else:
                return None
        except ValueError as e:
            print(e)
            return None

    def logar(self,email,senha):
        #logica para logar no banco
        try:
            QUERY = """
                SELECT * FROM Usuario WHERE Email = %s and Senha = %s
            """
            params = (email,senha,)
            existe = executeQuery(QUERY,params)
            if existe:
                usuarioDB = existe[0]
                nome = usuarioDB[1]
                id = usuarioDB[0]
                user = Usuario()
                user.setUsuario(nome,email,senha,id)
                return user
            else:
                return None
            
        except ValueError as e:
            print(e)
            return None
        
    def ler(self,id):
        QUERY = """
            SELECT * FROM Usuario WHERE Coduser = %s
        """
        params = (id)
        existe = executeQuery(QUERY,params)
        if existe:
            #retorna todas informacoes do usuario
            return existe[0]
        else:
            return None

    def editar(self,id,dicionario):
        #logica para editar informacoes do usuario no banco
        try:
            if not self.ler(id):
                return False
            query = """
            UPDATE USUARIO SET 
            """
            placeholders = []
            params = []
            for chave,valor in dicionario.items():
                placeholders.append(f"{chave} = %s")
                params.append(valor)

            query += ", ".join(placeholders)
            query += " WHERE CodUser = %s "
            params.append(id)
            executeQuery(query,tuple(params))
            return True 
        
        except ValueError as e:
            print(e)
            return False
        

    def excluir(self,email):
        #logica para excluir conta do usuario no banco
        pass