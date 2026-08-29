from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


# Create your views here.
class EntrarView(LoginView):
    """
    Reutiliza toda a logica de autenticacao ja testada do Django --
    validacao de password, criacao de sessao, protecao CSRF -- e so
    personaliza o template (aparencia) usado.
    """
    template_name = 'contas/login.html'
    redirect_authenticated_user = True   # se ja tiver sessao, salta o login
 
 
class SairView(LogoutView):
    """Termina a sessao e volta para o login."""
    next_page = reverse_lazy('contas:entrar')
