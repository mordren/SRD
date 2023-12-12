import io
from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import redirect
from django.http import JsonResponse
from relatorio.models import Cliente, DadosCompartimento, Finalidade, ProdutoTransportado, RelatorioDescontaminacao, Veiculo
from django.forms import model_to_dict
from relatorio.util.report import imprimirPDF
from django.http import FileResponse

#manipula a URL: localhost/relatorio/id
class relatorioView(View):
    def get(self, request, id):
        data = {}       
        data['tipo_descontaminacao'] =  RelatorioDescontaminacao.descontaminacao_choices
        data['processo_descontaminacao']  = RelatorioDescontaminacao.processo_descontaminacao_choices
        data['tipo_equipamento']  = RelatorioDescontaminacao.tipo_equipamento_choices
        data['id'] = id
        data['veiculo'] = RelatorioDescontaminacao.objects.filter(id=id).first().veiculo
        data['produtos'] = ProdutoTransportado.objects.all()
        data['relatorio'] = RelatorioDescontaminacao.objects.get(id=id)
        if (RelatorioDescontaminacao.objects.filter(id=id).first().tipo_equipamento != None):
            #EDIT
            data['compartimentos'] = DadosCompartimento.objects.filter(relatorio=data['relatorio'])
            data['existe'] = data['relatorio'].finalidade_descontaminacao.all()
            return render(request, 'relatorio/editarRelatorio.html', data)
        else:
            #verifico os números de compartimento e mando para instanciar o FORM
            data['range'] = range(1,data['veiculo'].numero_compartimentos+1)
            return render(request, 'relatorio/relatorio.html', data)
           
    
    def post(self, request, id):
        relatorio = RelatorioDescontaminacao.objects.filter(id=id).first()
        
        finalidade = request.POST.get('selTipoDescontaminacao')
        processo = request.POST.get('selTipoProcesso')
        validade = request.POST.get('validade')
        tipo_equipamento = request.POST['selTipoEquipamento']
        placa = request.POST['placa']
        
        relatorio.finalidade_descontaminacao.clear()
                
        Veiculo.objects.filter(placa=relatorio.veiculo.placa).update(placa=placa)
        
        # A finalidade é uma chave de manytomany para ser várias opções;
        for tipo in RelatorioDescontaminacao.descontaminacao_choices:
            tipo_resposta = request.POST.get('checkbox-'+tipo[0])
            if tipo_resposta == "on":
                finalidade = Finalidade.objects.filter(finalidade = tipo[0]).first()
                relatorio.finalidade_descontaminacao.add(finalidade)
                        
        RelatorioDescontaminacao.objects.filter(id=id).update(processo_descontaminacao=processo,
                                                              prazo_validade=validade, 
                                                              tipo_equipamento=tipo_equipamento)
              

        for i in range(0,relatorio.veiculo.numero_compartimentos):
            i = i+1
            num = str(i)
            volume = request.POST.get('volume'+num)
            combustivel = ProdutoTransportado.objects.filter(produto = request.POST.get('combustivel'+num)).first()
            onu = request.POST.get('ONU'+num)
            classeRisco = request.POST.get('classeRisco'+num)
            pressaoVapor = request.POST.get('pressaoVapor'+num)
            tempo = request.POST.get('tempo'+num)
            massaVapor = request.POST.get('massaVapor'+num)
            volumeAr = request.POST.get('volumeAr'+num)
            neutralizante = request.POST.get('neutralizante'+num)
            if DadosCompartimento.objects.filter(relatorio=relatorio).filter(numero_compartimento=i).exists():
                DadosCompartimento.objects.filter(relatorio=relatorio).filter(numero_compartimento=i).update(volume=volume, ultimo_produto_transportado=combustivel, 
                                              numeroONU=onu, classe_risco=classeRisco, pressao_vapor=pressaoVapor, tempo=tempo,
                                              massa_vapor=massaVapor, volumeAr=volumeAr, neutralizante=neutralizante, relatorio=relatorio)
            else:
                DadosCompartimento.objects.create(numero_compartimento=i, volume=volume, ultimo_produto_transportado=combustivel, 
                                              numeroONU=onu, classe_risco=classeRisco, pressao_vapor=pressaoVapor, tempo=tempo,
                                              massa_vapor=massaVapor, volumeAr=volumeAr, neutralizante=neutralizante, relatorio=relatorio)
        return imprimir(request, id)
    
class CriarRelatorio(View):
    def get(self, request):
        clientes = Cliente.objects.all()
        return render(request, 'relatorio/criarRelatorio.html', {'clientes':clientes, 'visivel':'hidden'}, )
    
    def post(self, request):
        cliente = Cliente.objects.filter(nome_completo=request.POST.get('cliente')).first()
        #veiculo = Viculo.objects.create(placa=placa, cliente=cliente, numero_compartimentos=compatimentos)       
        if cliente == None:           
            cliente = Cliente.objects.create(nome_completo=request.POST.get('cliente'),CNPJ='')
        return redirect('atualizarRelatorio-view', cliente.pk)
       
class atualizarRelatorio(View):
    def get(self, request, id):
        cliente = Cliente.objects.get(id=id)
        veiculos = Veiculo.objects.filter(cliente=cliente)
        return render(request, 'relatorio/continuarRelatorio.html', {'veiculos':veiculos, 'cliente':cliente})
    
    def post(self, request, id):
        CNPJ = request.POST.get('CNPJ')
        Cliente.objects.filter(id=id).update(CNPJ=CNPJ)
        cliente = Cliente.objects.get(id=id)
        placa = request.POST.get('placa')            
        equipamento = request.POST.get('numeroEquipamento')            
        compatimentos = request.POST.get('compartimento')
        veiculo = Veiculo.objects.filter(placa=placa).first()
        if not (Veiculo.objects.filter(placa=placa).exists()):
            veiculo = Veiculo.objects.create(placa=placa, cliente=cliente, numero_compartimentos=compatimentos, numeroEquipamento=equipamento)
        
        relatorio = RelatorioDescontaminacao.objects.create(veiculo=veiculo)
        return redirect('relatorio-view', relatorio.id)
         
def buscarClientes(request):
    data = []
    list_client = Cliente.objects.all()
    for cliente in list_client:
        data.append(model_to_dict(cliente))    
    return JsonResponse({'clientes':data})

def buscarCompartimentos(request, placa):
    numeroCompartimentos = Veiculo.objects.get(placa=placa)
    return JsonResponse({'num':numeroCompartimentos.numero_compartimentos})

def buscarRelatorio(request, id):
    relatorio = RelatorioDescontaminacao.objects.get(id=id)
    return JsonResponse({'placa':relatorio.veiculo.placa})

def buscarProduto(request, nome):
    produto = ProdutoTransportado.objects.filter(produto=nome).first()
    return JsonResponse({'onu':produto.numero_onu})

def teste(request):
    return render(request, 'relatorio/teste.html')

def home(request):
    return render(request, 'relatorio/index.html')

def listarRelatorio(request):
    data = {}
    data['relatorios'] = RelatorioDescontaminacao.objects.all()
    return render(request, 'relatorio/listarRelatorio.html', data)

def delRelatorio(request, id):
    rel = RelatorioDescontaminacao.objects.get(id=id)
    rel.delete()
    data = {}
    data['relatorios'] = RelatorioDescontaminacao.objects.all()
    return redirect('listarRelatorio-view')

def imprimir(request, id):
    relatorio = RelatorioDescontaminacao.objects.get(id=id)
    buffer = io.BytesIO()
    imprimirPDF(buffer, relatorio)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename='teste.pdf')