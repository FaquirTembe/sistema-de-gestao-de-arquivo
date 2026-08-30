from django.urls import path
from . import views
 
app_name = 'painel'
 
urlpatterns = [
    path('', views.PainelInicioView.as_view(), name='inicio'),
    path('utilizadores/', views.ListarUsuariosView.as_view(), name='utilizadores'),
    path('utilizadores/novo/', views.CriarUsuarioView.as_view(), name='utilizador_novo'),
    path('utilizadores/<int:pk>/editar/', views.EditarUsuarioView.as_view(), name='utilizador_editar'),
    path('utilizadores/<int:pk>/alternar/', views.AlternarAtivoUsuarioView.as_view(), name='utilizador_alternar'),
]
