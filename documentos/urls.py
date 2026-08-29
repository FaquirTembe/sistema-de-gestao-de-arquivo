from django.urls import path
from . import views
 
app_name = 'documentos'
 
urlpatterns = [
    path('anexar/<int:expediente_id>/', views.AnexarDocumentoView.as_view(), name='anexar'),
    path('<int:pk>/download/', views.DownloadDocumentoView.as_view(), name='download'),
]
