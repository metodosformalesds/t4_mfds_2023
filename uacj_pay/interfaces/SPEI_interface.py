from abc import ABC

class SPEIInterface(ABC):
    """
    Esta clase es la base de todas las operaciones que vayamos a realizar
    """
    
    @abstractmethod
    def codi(self, pay_information):
        raise NotImplementedError

    @abstractmethod
    def payment(self, parameter_list):
        raise NotImplementedError
    
    @abstractmethod
    def transferencia(self, parameter_list):
        raise NotImplementedError

    @abstractmethod 
    @staticmethod
    def validate_account(self, parameter_list):
        raise NotImplementedError
