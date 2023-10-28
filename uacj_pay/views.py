from django.shortcuts import render
from django.http import JsonResponse


"""
    * Registro de usuario con aws cognito
    * Almacenar usuario en dynamoDB (lambda)
"""
def crear_usuario(request):
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
    
    
