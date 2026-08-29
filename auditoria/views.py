from comum.permissions import NivelMinimoMixin
from django.views import View
from expedientes.models import Expediente
from .relatorios import gerar_pdf_expedientes, gerar_excel_expedientes
 
 
class RelatorioPDFView(NivelMinimoMixin, View):
    nivel_minimo = 2   # so Admin/Super Admin exportam relatorios gerais
 
    def get(self, request):
        return gerar_pdf_expedientes(Expediente.objects.all())
 
 
class RelatorioExcelView(NivelMinimoMixin, View):
    nivel_minimo = 2
 
    def get(self, request):
        return gerar_excel_expedientes(Expediente.objects.all())
