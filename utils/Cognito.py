import boto3
class AdminCognito:
    def __init__(self, client_cognito):
        self.client = client_cognito
        self.__user_pool_id = 'us-east-1_PPuagupzi'
        self.user_name = 'UACJ-PAY'
        

    def create_user(self, name, email, password):
        """Crea un usuario principal en cognito 

        Args:
            name (str): Nombre de usuario o de empresa a registrar
            email (str): email en donde se enviara la confirmacion de registro
            password (str): Contraseña del usuario
        """
        try:
            self.client.admin_create_user(
                UserPoolId=self.__user_pool_id,
                Username=name,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email
                    },
                ],
                DesiredDeliveryMediums=[
                    'EMAIL',
                ],
                ClientMetadata={
                    'string': 'string'
                }
            )
            
            self.client.admin_set_user_password(
                UserPoolId=self.__user_pool_id,
                Username=name,
                Password=password,
                Permanent=True
            )
            
            return {'status': 'Usuario creado'}
        
        except self.client.exceptions.UsernameExistsException:
            return {'error': 'El usuario ya existe'}
        except Exception as e:
            return {'error': str(e)}
    
    
    def delete_user(self, name):
        try:
            self.client.admin_delete_user(
                UserPoolId=self.__user_pool_id,
                Username=name
            )
        
            return {'status': 'Usuario eliminado'}
        
        except self.client.exceptions.UserNotFoundException:
            return {'error': 'Usuario no encontrado'}
        except Exception as e:
            return {'error': str(e)}
        
    def get_user_token(self, username, password):
        client = boto3.client('cognito-idp')
        try:
            response = client.initiate_auth(
                # AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                },
                # ClientId=app_client_id,
                UserPoolId=self.__user_pool_id
            )
        except client.exceptions.NotAuthorizedException:
            return {'error': 'Invalid username or password'}
        except client.exceptions.UserNotFoundException:
            return {'error': 'User not found'}
        except Exception as e:
            return {'error': str(e)}

        return {
            'access_token': response['AuthenticationResult']['AccessToken'],
            'refresh_token': response['AuthenticationResult']['RefreshToken'],
            'id_token': response['AuthenticationResult']['IdToken']
        }