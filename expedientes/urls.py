from django.urls import path
from . import views
 
app_name = 'expedientes'
 
urlpatterns = [
    path('', views.ListarExpedientesView.as_view(), name='listar'),
    path('meus/', views.MeusExpedientesView.as_view(), name='meus'),
    path('novo/', views.CriarExpedienteView.as_view(), name='criar'),
    path('<int:pk>/', views.VerExpedienteView.as_view(), name='ver'),
    path('apagar/<int:pk>/', views.ApagarExpedienteView.as_view(), name='apagar'),
]
