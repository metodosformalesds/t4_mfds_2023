import boto3
import uuid
import bcrypt

class Admin:
    def __init__(self, client_dynamoDB) -> None:
        self.client = client_dynamoDB
        self.__table_name = 'UACJ-PAY_Admin'
        
    def __generate_token(self):
            """
            Generates a unique token using UUID version 4.

            Returns:
                str: A string representation of the generated UUID.
            """
            return str(uuid.uuid4())
    
    def __generate_CLABE(self):
        pass
    
    def create_admin(self, username, password):
            try:
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                hashed_password = hashed_password.decode('utf-8')
                item = {
                    'token': {'S': self.__generate_token()},
                    'username': {'S': username},
                    'password': {'S': hashed_password},
                }

                
                self.client.put_item(TableName=self.__table_name, Item=item)
                
                return {'status': 'Usuario creado',
                        'token': item['token']['S'],
                        'username': item['username']['S']
                        }
                
            except Exception as e:
                return {'error': str(e)}
    