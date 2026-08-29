from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
 
 
class NivelMinimoMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    'Vestir' este mixin numa view significa: 'so entra quem tiver
    nivel numerico MENOR OU IGUAL a nivel_minimo'.
    Relembrar: 1=Super Admin (mais poder), 2=Admin, 3=Operador (menos poder).
    """
    nivel_minimo = 3   # por omissao, qualquer autenticado pode entrar
 
    def test_func(self):
        # Este metodo e chamado automaticamente pelo UserPassesTestMixin,
        # DEPOIS de o LoginRequiredMixin ja ter confirmado que ha sessao.
        return self.request.user.nivel <= self.nivel_minimo
 
    def handle_no_permission(self):
        # Se nem sequer estiver autenticado, manda para o login (comportamento
        # normal do Django). Se JA estiver autenticado mas sem nivel suficiente,
        # mostramos um erro 403 (Acesso Negado) em vez de o mandar para o login
        # outra vez -- ele ja fez login, o problema e OUTRO.
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        raise PermissionDenied('O teu nivel de acesso nao permite esta operacao.')
 
 
class ApenasProprioOperadorMixin:
    """
    Defesa contra 'IDOR' (Insecure Direct Object Reference) -- um termo
    tecnico para um problema muito simples: um Operador nao pode ver o
    expediente de outra pessoa so por adivinhar o numero na barra de
    enderecos (ex.: mudar /expedientes/12/ para /expedientes/13/).
    """
    def get_object(self, queryset=None):
        objecto = super().get_object(queryset)
        user = self.request.user
        # So se aplica a Operadores (nivel 3); Admin e Super Admin veem tudo.
        if user.nivel == user.NIVEL_OPERADOR and objecto.criado_por_id != user.id:
            raise PermissionDenied('So podes aceder aos expedientes que tu criaste.')
        return objecto
