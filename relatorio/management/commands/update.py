import datetime
from django.db import models
from django.core.management.base import BaseCommand
import pandas as pd
import csv
from pathlib import Path

from relatorio.models import Equipamento, ProdutoTransportado


class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        with open(BASE_DIR / './static/produtos_transportados.csv', 'r', encoding='utf-8') as arquivo:
            arquivo_csv = csv.reader(arquivo, delimiter=";")
            for linha in arquivo_csv:                
                ProdutoTransportado.objects.create(produto=linha[0], numero_onu=linha[1]) 
                
        Equipamento.objects.create(nome="Oxi", calibracao=datetime.date(2022,8,22), numero_serie='H210911223', patrimonio="MED01")        
                        
                
    