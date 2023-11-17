import boto3
import uuid
import bcrypt
from datetime import datetime

from utils.Cuenta.Cuenta import Cuenta

class Cuenta_Negocio(Cuenta):
    def __init__(self, name, password) -> None:
        super().__init__(name)
        self.client = boto3.client('dynamodb')
        self.__table_name = 'UACJ-PAY_Cuenta_Negocio'
        self.__token = self.__generate_token()
        self.__create_negocio(name, password)
    
    
    def __generate_token(self):
            """
            Generates a unique token using UUID version 4.

            Returns:
                str: A string representation of the generated UUID.
            """
            return str(uuid.uuid4())
    
    def get_token(self):
        return self.__token
    
    def __create_negocio(self, username, password):
        try:
            '''Encriptacion de la contraseña'''
            # salt = bcrypt.gensalt()
            # hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            # hashed_password = hashed_password.decode('utf-8')
            now = datetime.now()
            item = {
                'CLABE': {'N': self.get_CLABE()},
                'num_tarjeta': {'S': self.num_tarjeta},
                'CSV': {'S': self.get_CVC()},
                'fecha_vencimiento': {'S': self.fecha_vencimiento},
                'created': {'S': str(now.month) + '/' + str(now.year)},
                'token': {'S': self.__token},
                'name': {'S': username},
                'password': {'S': password},
                # 'pais': {'S': self.pais},
            }
            
            self.client.put_item(TableName=self.__table_name, Item=item)
            
        except Exception as e:
            print(e)
    