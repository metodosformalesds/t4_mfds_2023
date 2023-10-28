import boto3
class User:
    def __init__(self, id, user_pool_id, name, email, password):
        self.id = id
        self.user_pool_id = user_pool_id
        self.name = name
        self.email = email
        self.password = password
        
    
    def get_token(self):
        client = boto3.client('cognito-idp', region_name='us-east-1')
        try:
            response = client.initiate_auth(
                ClientId=self.id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': self.email,
                    'PASSWORD': self.password
                }
            )
            
            return {'token': response['AuthenticationResult']['AccessToken']}
        
        except client.exceptions.NotAuthorizedException:
            return {'error': 'Usuario o contraseña incorrectos'}
        except client.exceptions.UserNotFoundException:
            return {'error': 'Usuario no encontrado'}
        except Exception as e:
            return {'error': str(e)}
        