import json
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

dynamodb = boto3.resource('dynamodb')
tabla_cliente = 'UACJ_PAY_Cuenta_Cliente'
saldo_tabla = 'UACJ_PAY_Saldo_Cliente'

class Payment:
    @staticmethod
    @csrf_exempt
    def process_payment(request):
        if request.method == 'POST':
            try:
                payment_info = json.loads(request.body)

                # Obtiene los datos de la tarjeta
                cliente_table = dynamodb.Table(tabla_cliente)
                response = cliente_table.query(
                    KeyConditionExpression=Key('num_tarjeta').eq(payment_info['num_tarjeta'])
                )
                card_data = response.get('Items')[0] if response.get('Items') else None

                if not card_data:
                    return JsonResponse({'error': 'Tarjeta no encontrada'}, status=404)

                # Obtiene el saldo desde la tabla de saldos de cliente
                saldo_table = dynamodb.Table(saldo_tabla)
                response = saldo_table.get_item(
                    Key={'num_tarjeta': payment_info['num_tarjeta']}
                )
                saldo_data = response.get('Item') if response.get('Item') else None

                if not saldo_data:
                    return JsonResponse({'error': 'Saldo no encontrado'}, status=404)

                # Verifica los datos de la tarjeta
                if card_data['fecha_vencimiento'] != payment_info['fecha_vencimiento'] or \
                   card_data['csv'] != payment_info['csv']:
                    return JsonResponse({'error': 'Información de tarjeta inválida'}, status=400)

                # Verifica si hay saldo suficiente
                saldo = Decimal(saldo_data['saldo'])
                monto_pago = Decimal(payment_info['monto'])

                if saldo < monto_pago:
                    return JsonResponse({'error': 'Saldo insuficiente'}, status=400)

                # Actualizaa el saldo de la cuenta despues del pago
                nuevo_saldo = saldo - monto_pago
                saldo_table.update_item(
                    Key={'num_tarjeta': payment_info['num_tarjeta']},
                    UpdateExpression='SET saldo = :nuevo_saldo',
                    ExpressionAttributeValues={':nuevo_saldo': nuevo_saldo}
                )

                return JsonResponse({'status': 'Pago procesado exitosamente'})

            except json.JSONDecodeError as json_error:
                return JsonResponse({'error': 'Error al decodificar JSON', 'details': str(json_error)}, status=400)

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        else:
            return JsonResponse({'error': 'Método no permitido'}, status=405)

def verify_payment(self, request_params):
    propietario = request_params.get('propietario')
    num_tarjeta = request_params.get('num_tarjeta')
    csv = request_params.get('csv')
    fecha_vencimiento = request_params.get('fecha_vencimiento')

    try:
        client_table = dynamodb.Table(tabla_cliente)
        response = client_table.query(
            KeyConditionExpression=Key('propietario').eq(propietario) &
                                   Key('num_tarjeta').eq(num_tarjeta) &
                                   Key('csv').eq(csv) &
                                   Key('fecha_vencimiento').eq(fecha_vencimiento)
        )

        verification_result = len(response['Items']) > 0

        if verification_result:
            return JsonResponse({'status': 'Verificación de pago exitosa'})
        else:
            return JsonResponse({'error': 'La verificación de pago falló'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

