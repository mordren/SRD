from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(home), name='home-view'),
    path('relatorio/<int:id>', login_required(relatorioView.as_view()), name='relatorio-view'),
    path('listarRelatorio', listarRelatorio, name='listarRelatorio-view'),
    path('criarRelatorio',  login_required(CriarRelatorio.as_view()), name='criarRelatorio-view'),
    path('atualizarRelatorio/<int:id>',  login_required(atualizarRelatorio.as_view()), name='atualizarRelatorio-view'),
    path('delRelatorio/<int:id>', login_required(delRelatorio), name='delRelatorio-view'),
    path('imprimir/<int:id>', login_required(imprimir), name='imprimir'),
    
    #JSON
    path('buscarClientes', buscarClientes, name='buscarClientes-view'),
    path('teste', teste),
    path('buscarComp/<str:placa>', buscarCompartimentos),
    path('buscarRelatorio/<int:id>', buscarRelatorio),   
    path('buscarProduto/<str:nome>', buscarProduto),   
]