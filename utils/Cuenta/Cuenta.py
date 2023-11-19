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
        """
        Returns the CLABE (Clave Bancaria Estandarizada) of the account.

        Returns:
            str: The CLABE of the account.
        """
        return self.__CLABE
    
    def __generate_num_tarjeta(self):
            """
            Generates a random Mastercard number for the account.

            Returns:
                str: The generated Mastercard number.
            """
            mastercard = random.choice(['51', '55'])
            mastercard = mastercard + str(random.randint(10**12, 10**13 -1))
            return mastercard
    
    def __generate_CVC(self):
            """
            Generates a random Card Verification Code (CVC) for the account.

            Returns:
                str: The generated CVC.
            """
            return str(random.randint(100, 999))
    
    def get_CVC(self):
        """
        Returns the CVC (Card Verification Code) of the account.

        Returns:
            str: The CVC of the account.
        """
        return self.__CVC
    
    def __generate_fecha_vencimiento(self):
            """
            Generate the expiration date for the account.

            Returns:
                str: The expiration date in the format 'month/year'.
            """
            today = datetime.now()
            mount = today.month
            year = today.year + 5
            return f'{mount}/{year}'
    
    def get_saldo(self):
            """
            Returns the current balance of the account.
            
            Returns:
                float: The current balance of the account.
            """
            return self.__saldo