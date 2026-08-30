from django.db.models import Q
 
 
class FiltroExpedienteMixin:
    """Lê os parâmetros ?q=, ?situacao= e ?prioridade= da URL e aplica-os
    à queryset da view. Usado por qualquer ListView de Expediente --
    basta herdar este mixin ANTES do ListView."""
 
    def filtrar_queryset(self, queryset):
        pedido = self.request.GET
 
        termo = pedido.get('q', '').strip()
        if termo:
            queryset = queryset.filter(
                Q(numero__icontains=termo) |
                Q(assunto__icontains=termo) |
                Q(requerente__icontains=termo)
            )
 
        situacao = pedido.get('situacao', '').strip()
        if situacao:
            queryset = queryset.filter(situacao=situacao)
 
        prioridade = pedido.get('prioridade', '').strip()
        if prioridade:
            queryset = queryset.filter(prioridade=prioridade)
 
        return queryset
 
    def get_context_data(self, **kwargs):
        # Devolve os valores actuais dos filtros ao template, para os
        # campos do formulário 'lembrarem' o que o utilizador escolheu,
        # e para a paginação conseguir preservá-los ao mudar de página.
        contexto = super().get_context_data(**kwargs)
        contexto['filtros'] = {
            'q': self.request.GET.get('q', ''),
            'situacao': self.request.GET.get('situacao', ''),
            'prioridade': self.request.GET.get('prioridade', ''),
        }
        contexto['situacoes'] = self.model.Situacao.choices
        return contexto
