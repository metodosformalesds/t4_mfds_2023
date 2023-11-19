import json
import os

from datetime import datetime 
from decimal import Decimal

import boto3

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment(request):
    """
    Funcion para procesar pagos y verificar la existencia de una cuenta de cliente en DynamoDB.

    Args:
        request (HttpRequest): Objeto HttpRequest que representa la solicitud HTTP.

    Returns:
        JsonResponse: Respuesta en formato JSON con un mensaje de confirmación o error.

    Esta vista procesa solicitudes GET para verificar la existencia de una cuenta de cliente en DynamoDB.
    Los parametros esperados en la solicitud GET incluyen:
    - propietario: Nombre del propietario de la cuenta.
    - num_tarjeta: Numero de tarjeta de la cuenta.
    - csv: Codigo CSV de la tarjeta.
    - fecha_vencimiento: Fecha de vencimiento de la tarjeta (en el formato MM/YYYY).

    La funcion realiza una consulta a DynamoDB para obtener la cuenta correspondiente a los parametros proporcionados.
    Si se encuentra la cuenta, se devuelve una respuesta con un mensaje de confirmacion.
    Si no se encuentra la cuenta, se devuelve una respuesta con un mensaje de error.
    Si la solicitud no es de tipo GET, se devuelve una respuesta indicando que el metodo no esta permitido (405).
    """
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    dynamodb = boto3.resource('dynamodb')

    if request.method == 'GET':
        propietario = request.GET.get('propietario')
        num_tarjeta = request.GET.get('num_tarjeta')
        csv = request.GET.get('csv')
        fecha_vencimiento = request.GET.get('fecha_vencimiento')

        dynamodb = boto3.resource('dynamodb')
        tabla = dynamodb.Table('UACJ-PAY_Cuenta_Cliente')

        respuesta = tabla.get_item(
            Key={
                'propietario': propietario,
                'num_tarjeta': num_tarjeta,
                'csv': csv,
                'fecha_vencimiento': fecha_vencimiento
            }
        )

        if 'Item' in respuesta:
            return JsonResponse({'mensaje': 'Confirmacion: Los datos son correctos.'})
        else:
            return JsonResponse({'mensaje': 'Error: Los datos no son correctos.'})

    return JsonResponse({'mensaje': 'Error: Metodo no permitido.'}, status=405)
