from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.shortcuts import redirect, get_object_or_404
 
from comum.permissions import NivelMinimoMixin
from auditoria.models import LogAuditoria
from auditoria.utils import registar
from expedientes.models import Expediente
from .forms import UsuarioAdminForm
 
Usuario = get_user_model()
 
 
class PainelInicioView(NivelMinimoMixin, TemplateView):
    """Painel visível a partir do nível 2 (Admin). Mostra números
    rápidos e atalhos -- o atalho 'Gerir Utilizadores' só aparece
    no template se o utilizador for Super Admin (ver contexto)."""
    nivel_minimo = 2
    template_name = 'painel/inicio.html'
 
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['total_expedientes'] = Expediente.objects.count()
        contexto['total_utilizadores'] = Usuario.objects.filter(is_active=True).count()
        contexto['total_pendentes'] = Expediente.objects.exclude(
            situacao=Expediente.Situacao.ARQUIVADO
        ).count()
        return contexto
 
 
class ListarUsuariosView(NivelMinimoMixin, ListView):
    """Só Super Admin gere contas -- Admin (nível 2) gere expedientes,
    não pessoas (ver a divisão de papéis definida na Parte 1)."""
    model = Usuario
    nivel_minimo = 1
    template_name = 'painel/utilizadores.html'
    context_object_name = 'utilizadores'
    paginate_by = 15
    ordering = ['nome']
 
 
class CriarUsuarioView(NivelMinimoMixin, CreateView):
    model = Usuario
    form_class = UsuarioAdminForm
    nivel_minimo = 1
    template_name = 'painel/utilizador_formulario.html'
    success_url = reverse_lazy('painel:utilizadores')
 
    def form_valid(self, form):
        # create_user() (Parte 1, Fase 2) já aplica o hash da password --
        # por isso não gravamos o form directamente, construímos o objecto
        # à mão a partir dos dados limpos.
        dados = form.cleaned_data
        usuario = Usuario.objects.create_user(
            email_login=dados['email_login'],
            nome=dados['nome'],
            senha=dados['nova_senha'] or Usuario.objects.make_random_password(),
            nivel=dados['nivel'],
        )
        usuario.setor = dados['setor']
        usuario.is_active = dados['is_active']
        usuario.save()
 
        registar(
            self.request, LogAuditoria.Accao.CRIAR,
            modelo='Usuario', objecto_id=usuario.id,
            descricao=f'Criou a conta de {usuario.nome}',
        )
        messages.success(self.request, f'Conta de {usuario.nome} criada com sucesso.')
        return redirect(self.success_url)
 
 
class EditarUsuarioView(NivelMinimoMixin, UpdateView):
    model = Usuario
    form_class = UsuarioAdminForm
    nivel_minimo = 1
    template_name = 'painel/utilizador_formulario.html'
    success_url = reverse_lazy('painel:utilizadores')
 
    def form_valid(self, form):
        usuario = form.save(commit=False)
        nova_senha = form.cleaned_data.get('nova_senha')
        if nova_senha:
            usuario.set_password(nova_senha)
        usuario.save()
 
        registar(
            self.request, LogAuditoria.Accao.EDITAR,
            modelo='Usuario', objecto_id=usuario.id,
            descricao=f'Editou a conta de {usuario.nome}',
        )
        messages.success(self.request, f'Conta de {usuario.nome} actualizada.')
        return redirect(self.success_url)
 
 
class AlternarAtivoUsuarioView(NivelMinimoMixin, View):
    """Em vez de apagar uma conta (o que quebraria o histórico de
    expedientes ligados a ela via PROTECT), apenas desactivamos --
    é o mesmo princípio de 'arquivo lógico' usado em Expediente."""
    nivel_minimo = 1
 
    def post(self, request, pk):
        usuario = get_object_or_404(Usuario, pk=pk)
        usuario.is_active = not usuario.is_active
        usuario.save(update_fields=['is_active'])
 
        estado = 'activada' if usuario.is_active else 'desactivada'
        registar(
            request, LogAuditoria.Accao.EDITAR,
            modelo='Usuario', objecto_id=usuario.id,
            descricao=f'Conta de {usuario.nome} foi {estado}',
        )
        messages.success(request, f'Conta de {usuario.nome} {estado}.')
        return redirect('painel:utilizadores')


class EstatisticasView(NivelMinimoMixin, TemplateView):
    """Exibe estatísticas do sistema, como número de expedientes,
    documentos, utilizadores, etc. Acesso restrito a Admin (nível 2)."""
    nivel_minimo = 2
    template_name = 'painel/estatisticas.html'
 
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['total_expedientes'] = Expediente.objects.count()
        contexto['total_utilizadores'] = Usuario.objects.filter(is_active=True).count()
        contexto['total_pendentes'] = Expediente.objects.exclude(
            situacao=Expediente.Situacao.ARQUIVADO
        ).count()
        return contexto



