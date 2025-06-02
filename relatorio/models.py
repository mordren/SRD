from datetime import date
from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Cliente(models.Model):
    nome_completo = models.CharField(max_length=200)
    proprietario = models.CharField(max_length=200)
    documento = models.CharField(max_length=20, null=True, blank=True)    
    whatsapp = models.PositiveBigIntegerField(validators=[MaxValueValidator(99999999999)],
                help_text="DD-9XXXX XXXX sem os espaços",
                unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.nome_completo
        
class ProdutoTransportado(models.Model):
    produto = models.CharField(max_length=200)
    numero_onu = models.IntegerField()
    
    def __str__(self):
        return self.produto
    
class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    placa = models.CharField(max_length=10)
    numero_compartimentos = models.IntegerField()
    numeroEquipamento = models.CharField(max_length=30)
    
    def __str__(self):
        return self.placa
        
class Equipamento(models.Model):
    nome = models.CharField(max_length=200)
    calibracao = models.DateField()
    numero_serie = models.CharField(max_length=100)
    patrimonio = models.CharField(max_length=5)
   

class Finalidade(models.Model):
    finalidade_choices = (('1','Inspeção'),('2','Manutenção'),('3','Reparo'),('4','Reforma'),('5','Verificao metrológica'))
    finalidade = models.CharField(null=True, help_text='Finalidade Descontaminação',max_length=50, choices=finalidade_choices, default='1')
    
    def __str__(self):
        return self.get_finalidade_display()
    
class RelatorioDescontaminacao(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data = models.DateField(default=date.today, null=True, blank=True)
    #cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING)
    descontaminacao_choices = (('1','Inspeção'),('2','Manutenção'),('3','Reparo'),('4','Reforma'),('5','Verificao metrológica'))
    processo_descontaminacao_choices = (('1','Com ventilação forçada'),('2','Com Aplicação de Vapor'),('3','Com exaustão'),('4','Com lavagem química'),('5','Com lavagem com água'))
    tipo_equipamento_choices = (('1', 'Caminhão'),('2', 'Semirreboque'),('3','Rebocado'))
    
    processo_descontaminacao = models.CharField(null=True, help_text = 'Processo de Descontaminação', choices=processo_descontaminacao_choices, max_length=100)
    finalidade_descontaminacao = models.ManyToManyField(Finalidade, null=True, blank=True)
    finalidade_descontaminacao_outros = models.CharField(null=True, max_length=50)
       
    tipo_equipamento = models.CharField(null=True, help_text='Tipo do Equipamento', max_length=10, choices=tipo_equipamento_choices)
    prazo_validade = models.IntegerField(null=True, help_text='Prazo Validade Descontaminação', default=0)
    lacre = models.CharField(null=True, choices=(('N', 'N'), ('S','S')), max_length=10)
    numero_lacre = models.IntegerField(null=True, )
    observacoes = models.TextField(null=True, )
    
    def __str__(self):
        return 'relatório : '+str(self.pk)
    
class DadosCompartimento(models.Model):
    numero_compartimento = models.IntegerField(default=0)   
    volume = models.IntegerField()
    ultimo_produto_transportado = models.ForeignKey(ProdutoTransportado, verbose_name=("Produto Perigoso Transportado"), on_delete=models.DO_NOTHING)
    numeroONU = models.IntegerField()
    classe_risco = models.CharField(max_length=100)
    pressao_vapor = models.CharField(default='NA', max_length=10)
    tempo = models.IntegerField()
    massa_vapor = models.CharField(default='NA', max_length=10)
    neutralizante = models.CharField(default='NA', max_length=10)
    volumeAr = models.IntegerField()
    neutralizante = models.CharField(max_length=200)
    relatorio = models.ForeignKey(RelatorioDescontaminacao, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Relatório : '+ str(self.relatorio.pk) + ' volume: '+ str(self.numero_compartimento)