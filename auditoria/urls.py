from django.urls import path
from . import views
 
app_name = 'auditoria'
 
urlpatterns = [
    path('relatorio/pdf/', views.RelatorioPDFView.as_view(), name='relatorio_pdf'),
    path('relatorio/excel/', views.RelatorioExcelView.as_view(), name='relatorio_excel'),
]
