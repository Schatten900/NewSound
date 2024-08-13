from abc import ABC, abstractmethod

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
        if self.checkName(valor):
            return True
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
                return False

            if not secondName:
                nameFirstAux += caracter
            else:
                nameSecondAux += caracter
        
        if len(nameFirstAux) > 10 or len(nameFirstAux) < 3:
            return False
        
        if not nameFirstAux[0].isupper():
            return False
        
        if secondName:
            if len(nameSecondAux) > 10 or len(nameSecondAux) < 3:
                return False
            
            if not nameSecondAux[0].isupper():
                return False
            
        return True

class Senha(dominio):
    def _validar(self,valor):
        pass


class Email(dominio):
    def _validar(self,valor):
        pass