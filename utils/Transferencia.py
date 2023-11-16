import json
from datetime import datetime
from decimal import Decimal
import uuid
import boto3
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Importa la clase AdminCognito desde tu módulo Cognito
from utils.Cognito import AdminCognito
#my modules
from uacj_pay.interfaces.SPEI_interface import TransferenciasInterface

dynamodb = boto3.resource('dynamodb')
table_name = 'Transfers'

# Asegúrate de que la tabla exista antes de continuar
dynamodb.meta.client.get_waiter('table_exists').wait(TableName=table_name)

class TransferenciasImplementacion(TransferenciasInterface):
    def transferencia(self, transfer_information):
        # Lógica para la operación de transferencia
        data = transfer_information
        transfer_id = str(uuid.uuid4())  # Utilizar UUID para generar un ID único
        timestamp = str(datetime.utcnow())

        # Crear instancia de AdminCognito y verificar token
        cognito_client = boto3.client('cognito-idp', region_name='us-east-1')
        admin_cognito = AdminCognito(cognito_client)

        # Verificar token del usuario
        token_verification_result = admin_cognito.verify_user_token(data['token'])

        if 'error' in token_verification_result:
            return JsonResponse({'error': 'Token de usuario no válido'}, status=401)

        # Ejemplo: Realizar transferencia y almacenar en DynamoDB
        transfer_data = {
            'transfer_id': transfer_id,
            'sender': data['sender'],
            'recipient': data['recipient'],
            'amount': Decimal(str(data['amount'])),
            'timestamp': timestamp
        }

        transfers_table = dynamodb.Table(table_name)
        transfers_table.put_item(Item=transfer_data)

        return JsonResponse({'status': 'Transferencia realizada exitosamente'})
    
    def consultar_transferencia(self, transfer_id):
            # Lógica para consultar información de una transferencia por ID
            transfers_table = dynamodb.Table(table_name)

            try:
                response = transfers_table.get_item(Key={'transfer_id': transfer_id})
                transfer_data = response.get('Item')

                if not transfer_data:
                    return JsonResponse({'error': 'Transferencia no encontrada'}, status=404)

                return JsonResponse({'status': 'Consulta de transferencia exitosa', 'data': transfer_data})

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def create_transfer(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transferencia_impl = TransferenciasImplementacion()
        return transferencia_impl.transferencia(data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def consultar_transferencia(request, transfer_id):
    if request.method == 'GET':
        transferencia_impl = TransferenciasImplementacion()
        return transferencia_impl.consultar_transferencia(transfer_id)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
