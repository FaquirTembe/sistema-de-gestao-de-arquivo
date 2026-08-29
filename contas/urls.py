from django.urls import path
from . import views
 
app_name = 'contas'   # permite referir estas rotas como 'contas:entrar'
 
urlpatterns = [
    path('entrar/', views.EntrarView.as_view(), name='entrar'),
    path('sair/', views.SairView.as_view(), name='sair'),
]
