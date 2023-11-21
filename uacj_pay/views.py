import json
# Django modules
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import PayForm

# AWS modules
import boto3

# My modules
#from utils.usuario import User
from utils.Transferencia import TransferenciasImplementacion

transferencia_impl = TransferenciasImplementacion()
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
        return transferencia_impl.transferencia(data)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def consultar_transferencia(request, transfer_id):
    if request.method == 'GET':
        return transferencia_impl.consultar_transferencia(transfer_id)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def codi(request):
    if request.method== 'GET':
        pass
    else:
        return JsonResponse({'error':'Invalid request method'}, status=400)

def codi_pay(request, codi_id):
    if request.method == 'GET':
        form = PayForm()
        return render('codi.html', context={'codi':codi_id, 'form':form})
    elif request.method == 'POST':
        return transferencia_impl.codi_pay(codi_id, request.body)
        pass
    else:
        return JsonResponse({'error':'Invalid request method'}, status=400)
