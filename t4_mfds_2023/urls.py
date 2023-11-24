"""
URL configuration for t4_mfds_2023 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from utils import Pagos
import uacj_pay.views as uacj_pay_views
from uacj_pay.views import create_transfer, consultar_transferencia, codi, codi_pay

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', uacj_pay_views.generar_token),
    path('payment/', Pagos.Payment, name='payment'),
    
    #URLS para API transferencias
    path('api/create_transfer/', create_transfer, name='create_transfer'),
    path('api/consultar_transferencia/<str:transfer_id>/', consultar_transferencia, name='consultar_transferencia'),
    path('api/codi/create/', codi, name='codi'),
    path('api/codi/pay/<str:codi_id>', codi_pay, name='codi_pay')
]

