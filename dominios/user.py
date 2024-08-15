from abc import ABC, abstractmethod
import re

class dominio(ABC):
    def __init__(self):
        self.valor = ""

    @abstractmethod
    def _validar(self,valor):
        pass

    def get(self):
        return self.valor

    def set(self,valor):
        if self._validar(valor):
            self.valor = valor

class Nome(dominio):
    def _validar(self,valor):
        try:
            self.checkName(valor)
            return True
    
        except Exception as e:
            print(f"Erro: {e}")
            return False
    
    def checkName(self,nome):
        nameFirstAux = ""
        nameSecondAux = ""
        secondName = False
        for caracter in nome:
            if caracter == " " and secondName == False:
                secondName = True
                continue

            if caracter.isdigit() or not caracter.isalpha():
                raise ValueError("Insira caracteres válidos")

            if not secondName:
                nameFirstAux += caracter
            else:
                nameSecondAux += caracter
        
        if len(nameFirstAux) > 10 or len(nameFirstAux) < 3:
            raise ValueError("Tamanho de nome invalido")
        
        if not nameFirstAux[0].isupper():
            raise ValueError("Nome invalido")
        
        if secondName:
            if len(nameSecondAux) > 10 or len(nameSecondAux) < 3:
                raise ValueError("Tamanho de sobrenome invalido")
            
            if not nameSecondAux[0].isupper():
                raise ValueError("Sobrenome invalido")
            
        return True

class Senha(dominio):
    def _validar(self,valor):
        try:
            self.__checkDesc(valor)
            self.__checkCresc(valor)
            self.__formatacao(valor)
            return True
        
        except Exception as e:
            print(f"Erro detectado: {e}")
            return False
    
    def __checkCresc(self,valor):
        cont = 0
        for i in range(len(valor)-1):
            if int(valor[i])+1 == int(valor[i+1]):
                cont+=1

        if cont >= 3:
            raise ValueError("Não insira valores em ordem crescente")

    def __checkDesc(self,valor):
        cont = 0
        for i in range(len(valor)-1,0,-1):
            if int(valor[i]) == int(valor[i-1])-1:
                cont+=1

        if cont >= 3:
            raise ValueError("Não insira valores em ordem decrescente")
        
    def __formatacao(self,valor):
        if len(valor) != 6:
            raise ValueError("Insira uma senha de 6 digitos numericos")
        
        for i in range(len(valor)-1):
            if not valor[i].isdigit():
                raise ValueError("Insira somente valores numericos")


class Email(dominio):
    def _validar(self,valor):
        try :
            self.__check(valor)
            return True
        
        except Exception as e:
            print(f"Erro: {e}")
            return False

    def __check(self,valor):
        regex = r'\b[A-Za-z0-9._$-+]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if (not re.match(regex,valor)):
            raise ValueError("Email invalido!")


class Usuario:
    def __init__(self):
        self.nome = Nome()
        self.senha = Senha()
        self.email = Email()
        self.id = 0
        #usar auto-incremento para o id no bd

    def getNome(self):
        return self.nome
    
    def getSenha(self):
        return self.senha
    
    def getEmail(self):
        return self.email
    
    def getId(self):
        return self.id
    
    def setUsuario(self,nome,email,senha,id):
        try:
            self.getNome().set(nome)
            self.getEmail().set(email)
            self.getSenha().set(senha)
            self.id = id
        except Exception as e:
            print(f"Não foi possivel conectar a conta: {e}")


