from django.http import FileResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView
from django_ratelimit.decorators import ratelimit
from comum.permissions import NivelMinimoMixin, ApenasProprioOperadorMixin
from auditoria.models import LogAuditoria
from auditoria.utils import registar
from expedientes.models import Expediente
from .models import Documento
from django.views.generic import View
from django.shortcuts import redirect, get_object_or_404
 
 
class AnexarDocumentoView(NivelMinimoMixin, CreateView):
    model = Documento
    fields = ['categoria', 'titulo', 'ficheiro',]
    nivel_minimo = 3
    template_name = 'documentos/formulario.html'
 
    def form_valid(self, form):
        expediente = Expediente.objects.get(pk=self.kwargs['expediente_id'])
        # Um Operador so pode anexar a EXPEDIENTES SEUS -- reaproveitamos
       # a mesma logica de 'e teu?' que ja usamos para consultar.
        if self.request.user.nivel == self.request.user.NIVEL_OPERADOR \
                and expediente.criado_por_id != self.request.user.id:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied('So podes anexar aos teus proprios expedientes.')
 
        form.instance.expediente = expediente
        form.instance.uploadado_por = self.request.user
        resposta = super().form_valid(form)
        registar(
            self.request, LogAuditoria.Accao.CRIAR,
            modelo='Documento', objecto_id=self.object.id,
            descricao=f'Anexou {self.object.titulo} ao expediente {expediente.numero}',
        )
        return resposta
 
    def get_success_url(self):
        return reverse_lazy('expedientes:ver', args=[self.kwargs['expediente_id']])
 
 
@method_decorator(ratelimit(key='user', rate='30/m', block=True), name='get')
class DownloadDocumentoView(NivelMinimoMixin, DetailView):
    """
    @ratelimit(key='user', rate='30/m'): no MAXIMO 30 downloads por
    MINUTO, por utilizador autenticado. block=True significa que, ao
    ultrapassar o limite, o pedido e rejeitado automaticamente (HTTP 429).
    """
    model = Documento
    nivel_minimo = 3
 
    def get_queryset(self):
        # So documentos ACTIVOS podem ser descarregados (soft delete)
        return Documento.objects.filter(ativo=True)
 
    def get(self, request, *args, **kwargs):
        documento = self.get_object()
 
        # RBAC manual aqui: um Operador so descarrega de EXPEDIENTES SEUS
        if request.user.nivel == request.user.NIVEL_OPERADOR \
                and documento.expediente.criado_por_id != request.user.id:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied('So podes descarregar dos teus proprios expedientes.')
 
        registar(
            request, LogAuditoria.Accao.DOWNLOAD,
            modelo='Documento', objecto_id=documento.id,
            descricao=f'Descarregou {documento.titulo}',
        )
        return FileResponse(documento.ficheiro.open('rb'), as_attachment=True)


class ApagarDocumentoView(NivelMinimoMixin, View):
    nivel_minimo = 3  # mesmo nível de quem anexa

    def post(self, request, *args, **kwargs):
        documento = get_object_or_404(Documento, pk=kwargs['pk'], ativo=True)

        if request.user.nivel == request.user.NIVEL_OPERADOR \
                and documento.expediente.criado_por_id != request.user.id:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied('Só podes remover dos teus próprios expedientes.')

        documento.soft_delete()
        registar(
            request, LogAuditoria.Accao.EDITAR,  # ou criar Accao.REMOVER se preferir
            modelo='Documento', objecto_id=documento.id,
            descricao=f'Removeu {documento.titulo} do expediente {documento.expediente.numero}',
        )
        return redirect('expedientes:ver', expediente_id=documento.expediente_id)