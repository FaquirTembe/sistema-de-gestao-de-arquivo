from django.conf import settings
from django.db import models
 
 
class Expediente(models.Model):
    """Representa um processo administrativo, da entrada ao arquivo."""
 
    class Situacao(models.TextChoices):
        # TextChoices cria automaticamente um 'menu' de opcoes validas --
        # impede que alguem grave, por engano, 'situacao = "xpto"'.
        ENTRADA = 'ENTRADA', 'Entrada'
        EM_TRAMITACAO = 'EM_TRAMITACAO', 'Em Tramitacao'
        DESPACHADO = 'DESPACHADO', 'Despachado'
        ARQUIVADO = 'ARQUIVADO', 'Arquivado'
 
    numero = models.CharField(max_length=30, unique=True)
    assunto = models.CharField(max_length=200)
    requerente = models.CharField(max_length=150)
    tipo = models.CharField(max_length=80)
    situacao = models.CharField(
        max_length=20, choices=Situacao.choices, default=Situacao.ENTRADA
    )
    setor_atual = models.CharField(max_length=100, blank=True)
    prioridade = models.CharField(max_length=10, default='NORMAL')
 
    # PROTECT: impede apagar um Usuario se ele ainda tiver expedientes
    # criados -- protege o historico de nunca ficar 'orfao'.
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
        related_name='expedientes_criados',
    )
 
    data_entrada = models.DateField(auto_now_add=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ['-criado_em']   # mais recentes primeiro
 
    def __str__(self):
        return f'{self.numero} — {self.assunto}'
 
    def tramitar(self, novo_setor):
        """Move o expediente para outro sector.
        A verificacao de QUEM pode chamar isto e feita na VIEW
        (usando o NivelMinimoMixin), nunca aqui dentro do modelo --
        o modelo so sabe COMO mudar de estado, nao QUEM tem permissao."""
        self.situacao = self.Situacao.EM_TRAMITACAO
        self.setor_atual = novo_setor
        self.save(update_fields=['situacao', 'setor_atual', 'atualizado_em'])
 
    def despachar(self):
        self.situacao = self.Situacao.DESPACHADO
        self.save(update_fields=['situacao', 'atualizado_em'])
 
    def arquivar(self):
        """'Arquivo logico': o registo NUNCA e apagado da base de dados,
        apenas muda de estado. Isto preserva o historico para auditoria
        e para se poder, no futuro, reabrir um processo se necessario."""
        self.situacao = self.Situacao.ARQUIVADO
        self.save(update_fields=['situacao', 'atualizado_em'])
