from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import LogAuditoria
from .utils import registar
 
 
@receiver(user_logged_in)
def registar_login(sender, request, user, **kwargs):
    registar(request, LogAuditoria.Accao.LOGIN, modelo='Usuario',
             objecto_id=user.id, descricao=f'{user.nome} autenticou-se')
