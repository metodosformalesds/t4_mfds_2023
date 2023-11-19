import uuid
import bcrypt

from utils.Cuenta.Cuenta import Cuenta
from utils.Cuenta.Cuenta_cliente import Cuenta_Cliente

class Cuenta_Negocio(Cuenta):
    def __init__(self, name, password) -> None:
        super().__init__()
        # self.client = boto3.client('dynamodb')
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
        """
        Returns the token associated with the account.
        """
        return self.__token
    
    def __create_negocio(self, username: str, password: str):
            """
            Creates a new negocio in the database.

            Args:
                username (str): The username of the negocio.
                password (str): The password of the negocio.

            Raises:
                Exception: If an error occurs while creating the negocio.

            Returns:
                None
            """
            try:
                '''Encriptacion de la contraseña'''
                # salt = bcrypt.gensalt()
                # hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                # hashed_password = hashed_password.decode('utf-8')
                item = {
                    'CLABE': {'N': self.get_CLABE()},
                    'num_tarjeta': {'S': self.num_tarjeta},
                    'CSV': {'S': self.get_CVC()},
                    'fecha_vencimiento': {'S': self.fecha_vencimiento},
                    'created': {'S': self.created},
                    'token': {'S': self.__token},
                    'name': {'S': username},
                    'password': {'S': password},
                    'pais': {'S': self.pais},
                }
                
                self.client.put_item(TableName=self.__table_name, Item=item)
                
                # Tabla de saldo
                item = {
                    'CLABE': {'N': self.get_CLABE()},
                    'saldo': {'N': '0'},
                }
                
                self.client.put_item(TableName='UACJ-PAY_Saldo_Negocio', Item=item)
                
            except Exception as e:
                print(e)
            
    
    def create_cliente(self, name):
        """
        Creates a new cliente with the given name and returns a list of variable names.

        Args:
            name (str): The name of the cliente.

        Returns:
            dict: A dict of variable names associated with the created cliente.
        """
        cuenta_cliente = Cuenta_Cliente(name, self.get_CLABE())
        cuenta_cliente.create_cliente()
        return cuenta_cliente.get_variable_names()