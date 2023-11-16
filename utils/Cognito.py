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
        """Borra un usuario de cognito

        Args:
            name (str): Nombre de usuario a eliminar

        Returns:
            dict: status
        """
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
            response = client.create_user_pool_client(
                UserPoolId=self.__user_pool_id,
                ClientName=username,
                GenerateSecret=True,
                RefreshTokenValidity=30,
                AccessTokenValidity=30,
                # IdTokenValidity=30,
                TokenValidityUnits={
                    'AccessToken': 'days',
                    'IdToken': 'days',
                    'RefreshToken': 'days'
                },
                ReadAttributes=[
                    'string',
                ],
                WriteAttributes=[
                    'string',
                ],
                ExplicitAuthFlows=[
                    # 'ADMIN_NO_SRP_AUTH'|'CUSTOM_AUTH_FLOW_ONLY'|'USER_PASSWORD_AUTH'|'ALLOW_ADMIN_USER_PASSWORD_AUTH'|'ALLOW_CUSTOM_AUTH'|'ALLOW_USER_PASSWORD_AUTH'|'ALLOW_USER_SRP_AUTH'|'ALLOW_REFRESH_TOKEN_AUTH',
                    'ALLOW_USER_PASSWORD_AUTH',
                ],
                SupportedIdentityProviders=[
                    'string',
                ],
                CallbackURLs=[
                    'string',
                ],
                LogoutURLs=[
                    'string',
                ],
                DefaultRedirectURI='string',
                AllowedOAuthFlows=[
                    'client_credentials',
                ],
                AllowedOAuthScopes=[
                    'string',
                ],
                AllowedOAuthFlowsUserPoolClient=True,
                # AnalyticsConfiguration={
                #     'ApplicationId': 'string',
                #     'ApplicationArn': 'string',
                #     'RoleArn': 'string',
                #     'ExternalId': 'string',
                #     'UserDataShared': True|False
                # },
                # PreventUserExistenceErrors='ENABLED',
                # EnableTokenRevocation=True,
                # EnablePropagateAdditionalUserContextData=True,
                # AuthSessionValidity=123
            )
            
            return response
            
        except client.exceptions.NotAuthorizedException:
            return {'error': 'Invalid username or password'}
        except client.exceptions.UserNotFoundException:
            return {'error': 'User not found'}
        except Exception as e:
            return {'error': str(e)}