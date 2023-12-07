from reportlab.pdfgen.canvas import Canvas
from pdfrw import PdfReader
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.lib.pagesizes import A4
from django.conf import settings
from datetime import datetime
from relatorio.models import DadosCompartimento, Equipamento, RelatorioDescontaminacao


def mp(mm):
    return mm/0.352777

def imprimirPDF(link, relatorio):    
    relatorio = RelatorioDescontaminacao.objects.get(id=relatorio.id)
    media_url = settings.MEDIA_ROOT
    template = PdfReader(media_url+"/templates/template.pdf", decompress=False).getPage(0)

    template_obj = pagexobj(template)
    
    canvas = Canvas(link)
    canvas.setPageSize(A4)
    
    xobj_name = makerl(canvas, template_obj)
    canvas.doForm(xobj_name)
    
    canvas.setTitle("Relatorio :"+datetime.strftime(relatorio.data, "%d/%m/%Y"))
    
    canvas.drawString(mp(184),mp(241.5), str(relatorio.id))
    
    canvas.setFontSize(8)
      
    canvas.drawString(mp(49),mp(222.5), relatorio.veiculo.cliente.nome_completo)
    canvas.drawString(mp(50),mp(219.3), relatorio.veiculo.cliente.CNPJ)
    canvas.drawString(mp(44),mp(215.6), str(relatorio.get_tipo_equipamento_display()))
    canvas.drawString(mp(80),mp(212.5), relatorio.veiculo.placa)
    
    finalidades = relatorio.finalidade_descontaminacao.all()
    
    for finalidade in finalidades:       
      
        if(finalidade.finalidade == "1"):
            canvas.drawString(mp(35),mp(199.5), "X")
        elif(finalidade.finalidade == "2"):
            canvas.drawString(mp(71),mp(199.5), "X")
        elif(finalidade.finalidade == "3"):
            canvas.drawString(mp(106),mp(199.5), "X")
        elif(finalidade.finalidade == "4"):
            canvas.drawString(mp(142),mp(199.5), "X")
        elif(finalidade.finalidade == "5"):
            canvas.drawString(mp(177.5),mp(199.5), "X")
    
    canvas.setFontSize(11)
    canvas.drawString(mp(62),mp(189.5), str(relatorio.prazo_validade))
    
    canvas.setFontSize(8)
    
    if(relatorio.processo_descontaminacao == "2"):
        canvas.drawString(mp(21.5),mp(183.6), "X")
    elif(relatorio.processo_descontaminacao == "1"):
        canvas.drawString(mp(21.5),mp(179.9), "X")
    elif(relatorio.processo_descontaminacao == "3"):
        canvas.drawString(mp(21.5),mp(176.2), "X")
    elif(relatorio.processo_descontaminacao == "4"):
        canvas.drawString(mp(21.5),mp(172.8), "X")
    elif(relatorio.processo_descontaminacao == "5"):
        canvas.drawString(mp(21.5),mp(169.4), "X")
    elif(relatorio.processo_descontaminacao == "6"):
        canvas.drawString(mp(21.5),mp(166), "X")
    
    compartimentos = DadosCompartimento.objects.filter(relatorio=relatorio)
    
    coluna = mp(43)
    linha = mp(157)
    expessuraLinha = mp(5)
    l = 0
    
    for compartimento in compartimentos:
        canvas.drawString(coluna+mp(7.5),mp(157), str(compartimento.volume))
        canvas.drawString(coluna,mp(151), str(compartimento.ultimo_produto_transportado))
        canvas.drawString(coluna+mp(5),mp(145), str(compartimento.numeroONU))
        canvas.drawString(coluna+mp(7.5),mp(141), str(compartimento.classe_risco))
        canvas.drawString(coluna+mp(7.5),mp(136), str(compartimento.pressao_vapor))
        canvas.drawString(coluna+mp(7.5),mp(130), str(compartimento.tempo))
        canvas.drawString(coluna+mp(7.5),mp(126), str(compartimento.massa_vapor))
        canvas.drawString(coluna+mp(6),mp(122), str(compartimento.volumeAr))
        canvas.drawString(coluna+mp(7.5),mp(118), str(compartimento.neutralizante))

        linha = mp(157)
        coluna = coluna + mp(20.5)           

    equipamento = Equipamento.objects.filter().first()
    
    canvas.drawString(mp(61.5),mp(111.2), equipamento.numero_serie)
    canvas.drawString(mp(138),mp(111.2), datetime.strftime(equipamento.calibracao, "%d/%m/%Y"))
    
    canvas.drawString(mp(55.5),mp(107.5), equipamento.numero_serie)
    canvas.drawString(mp(138),mp(107.5), datetime.strftime(equipamento.calibracao, "%d/%m/%Y"))
    
    canvas.drawString(mp(50.5),mp(103.8), equipamento.numero_serie)
    canvas.drawString(mp(138),mp(103.8), datetime.strftime(equipamento.calibracao, "%d/%m/%Y"))

    
    canvas.drawString(mp(39),mp(32.2), datetime.strftime(relatorio.data, "%d/%m/%Y"))
    canvas.showPage()
    
    template = PdfReader(media_url+"/templates/template.pdf", decompress=False).getPage(1)
    template_obj = pagexobj(template)

    canvas.setFontSize(8)
    
    canvas.setPageSize(A4)

    xobj_name = makerl(canvas, template_obj)
    canvas.doForm(xobj_name)
    
    canvas.drawString(mp(20),mp(241), relatorio.veiculo.cliente.nome_completo)
    canvas.drawString(mp(20),mp(233), relatorio.veiculo.numeroEquipamento)    
    canvas.drawString(mp(20),mp(225), relatorio.get_tipo_equipamento_display())   
    canvas.drawString(mp(99),mp(225), relatorio.veiculo.placa)
    
    canvas.drawString(mp(22),mp(211.5), 'X')
    
    canvas.setFontSize(14)
    canvas.drawString(mp(24.4),mp(88.2), str(relatorio.pk))
    
    canvas.setFontSize(12)
    
    canvas.drawString(mp(17), mp(45), 'Palmas, '+datetime.strftime(relatorio.data, "%d/%m/%Y"))
    
    canvas.save()
    return canvas
       