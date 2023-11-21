from datetime import datetime
from decimal import Decimal
import uuid
import boto3
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Configuración y nombres de las tablas
dynamodb = boto3.resource('dynamodb')
table_name = 'UACJ-PAY_Cuenta_Negocio'  # Tabla para verificar el token
admin_table_name = 'Transfers'  # Tabla donde se insertarán los datos de transferencia
client_table_name = 'UACJ-PAY_Cuenta_Cliente'  # Tabla de cuentas de cliente

# Asegúrate de que las tablas existan antes de continuar
dynamodb.meta.client.get_waiter('table_exists').wait(TableName=table_name)
dynamodb.meta.client.get_waiter('table_exists').wait(TableName=admin_table_name)
dynamodb.meta.client.get_waiter('table_exists').wait(TableName=client_table_name)

class TransferenciasImplementacion:
    @staticmethod
    def verify_user_token(token):
        try:
            # Utiliza la tabla "UACJ-PAY_Cuenta_Negocio" para verificar el token
            admin_table = dynamodb.Table(table_name)
            response = admin_table.get_item(Key={'token_column_name': token})
            admin_data = response.get('Item')

            if not admin_data:
                return {'error': 'Token de usuario no válido'}

            return {'status': 'Token de usuario válido'}

        except Exception as e:
            return {'error': str(e)}

    def verify_account_exists(self, clabe) -> bool:
        try:
            # Utiliza la tabla "UACJ-PAY_Cuenta_Cliente" para verificar la existencia de la cuenta
            client_table = dynamodb.Table(client_table_name)
            response = client_table.get_item(Key={'CLABE': {'N': str(clabe)}})
            account_data = response.get('Item')

            return account_data is not None

        except Exception as e:
            return False

    def transferencia(self, transfer_information):
        data = transfer_information
        transfer_id = str(uuid.uuid4())  # Utilizar UUID para generar un ID único
        timestamp = str(datetime.utcnow())

        # Verificar token del usuario
        token_verification_result = self.verify_user_token(data['token'])

        if 'error' in token_verification_result:
            return JsonResponse({'error': 'Token de usuario no válido'}, status=401)

        # Verificar si las cuentas de sender y recipient existen
        sender_exists = self.verify_account_exists(data['sender'])
        recipient_exists = self.verify_account_exists(data['recipient'])

        if not sender_exists or not recipient_exists:
            return JsonResponse({'error': 'Cuenta de sender o recipient no encontrada'}, status=404)

        # Ejemplo: Realizar transferencia y almacenar en DynamoDB
        transfer_data = {
            'transfer_id': transfer_id,
            'sender': data['sender'],
            'recipient': data['recipient'],
            'amount': Decimal(str(data['amount'])),
            'timestamp': timestamp
        }

        # Utiliza la tabla "Transfers" para almacenar los datos de transferencia
        transfers_table = dynamodb.Table(admin_table_name)
        transfers_table.put_item(Item=transfer_data)

        return JsonResponse({'status': 'Transferencia realizada exitosamente'})

    def consultar_transferencia(self, transfer_id):
        # Utiliza la tabla "Transfers" para consultar la información de transferencia
        transfers_table = dynamodb.Table(admin_table_name)

        try:
            response = transfers_table.get_item(Key={'transfer_id': transfer_id})
            transfer_data = response.get('Item')

            if not transfer_data:
                return JsonResponse({'error': 'Transferencia no encontrada'}, status=404)

            return JsonResponse({'status': 'Consulta de transferencia exitosa', 'data': transfer_data})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def __generate_pay_link(self, account, ammount:float=0, concept='No concept', reference='1')->str:
        PAYMENT_URL = 'codi_pay'
        params = f"a{ammount}ac{account}c{concept}r{reference}"
        
        return reverse(PAYMENT_URL, args=(id))
        pass
    
    #Override
    def codi(self, payment_information)->str:

        if not self.verify_account_exists(payment_information.account):
            return JsonResponse({'error': 'La cuenta clabe no existe o es invalida'})
        link:str = self.__generate_pay_link(**payment_information)
        return JsonResponse({'codi':link})
        raise NotImplementedError
        pass  
