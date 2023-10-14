from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Cliente)
admin.site.register(RelatorioDescontaminacao)
admin.site.register(ProdutoTransportado)
admin.site.register(DadosCompartimento)
admin.site.register(Equipamento)
admin.site.register(Veiculo)

