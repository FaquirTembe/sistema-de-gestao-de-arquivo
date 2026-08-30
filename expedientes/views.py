from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from comum.permissions import NivelMinimoMixin, ApenasProprioOperadorMixin
from auditoria.models import LogAuditoria
from auditoria.utils import registar
from .models import Expediente
from .forms import ExpedienteForm
 
 
class ListarExpedientesView(NivelMinimoMixin, ListView):
    """Nivel 1 e 2 veem TODOS os expedientes. Operadores nunca chegam
    aqui -- para eles ha a MeusExpedientesView, mais abaixo."""
    model = Expediente
    nivel_minimo = 2
    template_name = 'expedientes/listar.html'
    context_object_name = 'expedientes'
    paginate_by = 20
 
 
class MeusExpedientesView(NivelMinimoMixin, ListView):
    """Um Operador so ve os expedientes que ELE PROPRIO criou --
    filtramos a 'queryset' (a lista pedida a base de dados) logo na origem,
    o que e mais seguro do que filtrar so depois, no template."""
    model = Expediente
    nivel_minimo = 3
    template_name = 'expedientes/listar.html'
    context_object_name = 'expedientes'
 
    def get_queryset(self):
        return Expediente.objects.filter(criado_por=self.request.user)
 
 
class VerExpedienteView(NivelMinimoMixin, ApenasProprioOperadorMixin, DetailView):
    model = Expediente
    nivel_minimo = 3   # qualquer autenticado PODE tentar; o mixin acima
                       # e que decide se ESTE expediente em particular e seu
    template_name = 'expedientes/ver.html'
 
 
class CriarExpedienteView(NivelMinimoMixin, CreateView):
    model = Expediente
    form_class = ExpedienteForm
    nivel_minimo = 3   # qualquer nivel pode registar uma entrada
    template_name = 'expedientes/formulario.html'
    success_url = reverse_lazy('expedientes:meus')
 
    def form_valid(self, form):
        # 1) PRIMEIRO atribuímos quem criou o expediente...
        form.instance.criado_por = self.request.user
 
        # 2) ...SÓ DEPOIS chamamos o super(), que é quem efectivamente
        #    grava a linha na base de dados (INSERT INTO ...).
        resposta = super().form_valid(form)
 
        registar(
            self.request, LogAuditoria.Accao.CRIAR,
            modelo='Expediente', objecto_id=self.object.id,
            descricao=f'Registou o expediente {self.object.numero}',
        )
        messages.success(self.request, 'Expediente registado com sucesso!')
        return resposta




