from dominios.user import Usuario

#Chamada na camada de apresentação para efetuar o serviço
class CntrlSConta:
    def __init__(self):
        self.user = Usuario()

    def getConta(self):
        return self.user

    def cadastrar(self):
        conta = self.getConta()
        container = ContainerConta()
        container.cadastrar(conta)

    def logar(self):
        conta = self.getConta()
        container = ContainerConta()
        container.logar(conta)

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
    def cadastrar(self,conta):
        nome = conta.getNome().get()
        email = conta.getEmail().get()
        senha = conta.getSenha().get()
        #logica para cadastrar no banco

    def logar(self,conta):
        email = conta.getEmail().get()
        senha = conta.getSenha().get()
        #logica para logar no banco
        

    def ler(self,email):
        pass

    def editar(self,email,dicionario):
        pass

    def excluir(self,email):
        pass