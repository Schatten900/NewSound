from dominios.user import Usuario

#Chamada na camada de apresentação para efetuar o serviço
class CntrlSConta:
    def __init__(self):
        self.user = Usuario()

    def getConta(self):
        return self.user
    
    def setConta(self,conta):
        self.user = conta

    def cadastrar(self,nome,email,senha,confirm):
        if not nome or not email or not senha:
            return None
        if senha != confirm:
            return None

        conta = self.getConta()
        container = ContainerConta()
        conta = container.cadastrar(nome,email,senha)
        print(nome,email,senha)
        return conta

    def logar(self,email,senha):
        conta = self.getConta()
        container = ContainerConta()
        container.logar(email,senha)
        conta = container.logar(email,senha)
        print(email,senha)
        return conta

    def ler(self):
        conta = self.getConta()
        email = conta.getEmail().get()
        container = ContainerConta()
        container.ler(email)

    #usar dicionario para poder editar os valores recebidos
    def editar(self,dicionario):
        conta = self.getConta()
        email = conta.getEmail().get()
        container = ContainerConta()
        container.editar(email,dicionario)

    def excluir(self):
        conta = self.getConta()
        email = conta.getEmail().get()
        container = ContainerConta()
        container.excluir(email)

#Acessa o banco de dados e faz as operacoes
class ContainerConta:
    def cadastrar(self,nome,email,senha):
        user = Usuario()
        return user
        #logica para cadastrar no banco

    def logar(self,email,senha):
        user = Usuario()
        return user
        #logica para logar no banco
        
    def ler(self,email):
        #logica para ler do banco de dados a conta
        pass

    def editar(self,email,dicionario):
        #logica para editar informacoes do usuario no banco
        pass

    def excluir(self,email):
        #logica para excluir conta do usuario no banco
        pass