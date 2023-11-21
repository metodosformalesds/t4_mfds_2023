import json
# Django modules
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# AWS modules
import boto3

# My modules
#from utils.usuario import User
from utils.Transferencia import TransferenciasImplementacion
from utils.Pagos import Payment

"""
    * Registro de usuario con aws cognito
    * Almacenar usuario en dynamoDB (lambda)
"""
def crear_usuario(request):
    # Definir usuario con cognito
    # user = User()
    # return JsonResponse(user.get_token())
    pass

"""
    * Verificar que el usuario exista
    * Verificar que el token que genero anteriormente expiro
    * Creacion de nuevo token
    * Retornar token de acceso
"""
def generar_token(request):
    return JsonResponse({"token": 'akjdhaskjdhas',
                         "expire": ':v'})
    
    
def generar_pago(request):
    
    pass

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
    
    # Pagos
@csrf_exempt
def generate_payment(request):
    pass

@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        payment_data = json.loads(request.body)
        payment_impl = Payment()
        return payment_impl.process_payment(payment_data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def verify_payment(request):
    if request.method == 'GET':
        payment_impl = Payment()
        return payment_impl.verify_payment(request.GET)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
