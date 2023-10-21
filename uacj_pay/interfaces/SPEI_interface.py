from abc import ABC

class TransferenciasInterface(ABC):
    """
    Esta clase es la base de todas las operaciones que vayamos a realizar
    """
    
    @abstractmethod
    def codi(self, pay_information):
        raise NotImplementedError

    @abstractmethod
    def pago(self, parameter_list):
        raise NotImplementedError
    
    @abstractmethod
    def transferencia(self, parameter_list):
        raise NotImplementedError
