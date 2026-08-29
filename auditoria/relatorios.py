from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse
 
 
def gerar_pdf_expedientes(expedientes):
    """Recebe uma lista de Expediente e devolve uma HttpResponse
    com um PDF pronto a ser descarregado pelo browser."""
 
    # HttpResponse com este 'content_type' diz ao browser: 'isto e um PDF'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_expedientes.pdf"'
 
    documento = SimpleDocTemplate(response, pagesize=A4)
    estilos = getSampleStyleSheet()
    elementos = [Paragraph('Relatório de Expedientes — SGE-Mandlakazi', estilos['Title'])]
 
    # Monta a tabela: primeiro a linha de cabecalho, depois uma linha por expediente
    dados = [['Número', 'Assunto', 'Situação', 'Data de Entrada']]
    for exp in expedientes:
        dados.append([exp.numero, exp.assunto, exp.get_situacao_display(), str(exp.data_entrada)])
 
    tabela = Table(dados, repeatRows=1)   # repeatRows=1: cabecalho repete em cada pagina nova
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5E4E')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    elementos.append(tabela)
 
    documento.build(elementos)   # escreve o PDF directamente dentro da response
    return response
