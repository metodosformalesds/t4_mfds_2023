import boto3
import random
from datetime import datetime

from utils.CLABE import calcular_digito_verificador

class Cuenta:
    def __init__(self) -> None:
        self.client = boto3.client('dynamodb')
        self.__CLABE = self.__generate_CLABE()
        self.num_tarjeta = self.__generate_num_tarjeta()
        self.pais = 'MEXICO'
        self.__CVC = str(self.__generate_CVC())
        self.fecha_vencimiento = self.__generate_fecha_vencimiento()
        self.__saldo = 0
        self.created = str(datetime.now().month) + '/' + str(datetime.now().year)
    
    def __generate_CLABE(self):
            """
            Generates a CLABE (Clave Bancaria Estandarizada) for the account.

            Returns:
                str: The generated CLABE.
            """
            struct_CLABE = '646180'
            random_number = str(random.randint(10**8, 10**9 -1))
            verification_digit = calcular_digito_verificador(random_number)
            return struct_CLABE + random_number + str(verification_digit)
    
    def get_CLABE(self):
        return self.__CLABE
    
    def __generate_num_tarjeta(self):
        # Modificar para tarjetas validas mastercard
        mastercard = random.choice(['51', '55'])
        mastercard = mastercard + str(random.randint(10**12, 10**13 -1))
        return mastercard
    
    def __generate_CVC(self):
        return str(random.randint(100, 999))
    
    def get_CVC(self):
        return self.__CVC
    
    def __generate_fecha_vencimiento(self):
        today = datetime.now()
        mount = today.month
        year = today.year + 5
        return f'{mount}/{year}'
    
    def get_saldo(self):
        return self.__saldo
    
    # def add_saldo(self, new_saldo: int):
    #     self.__saldo = self.__saldo + new_saldo
    
    