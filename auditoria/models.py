from django.conf import settings
from django.db import models
 
 
class LogAuditoria(models.Model):
    class Accao(models.TextChoices):
        LOGIN = 'LOGIN', 'Autenticacao'
        CRIAR = 'CRIAR', 'Criacao'
        EDITAR = 'EDITAR', 'Edicao'
        TRAMITAR = 'TRAMITAR', 'Tramitacao'
        DESPACHAR = 'DESPACHAR', 'Despacho'
        ARQUIVAR = 'ARQUIVAR', 'Arquivo'
        DOWNLOAD = 'DOWNLOAD', 'Download'
 
    # null=True: mesmo que a conta do utilizador seja um dia apagada,
    # o registo de auditoria PERMANECE (SET_NULL em vez de CASCADE) --
        # perder o historico seria pior do que so perder a referencia ao nome.
    utilizador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    accao = models.CharField(max_length=20, choices=Accao.choices)
    modelo = models.CharField(max_length=50)      # ex.: 'Expediente'
    objecto_id = models.CharField(max_length=20)  # ex.: '7'
    descricao = models.CharField(max_length=255)
    endereco_ip = models.GenericIPAddressField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Registo de Auditoria'
        verbose_name_plural = 'Registos de Auditoria'
 
    def __str__(self):
        quem = self.utilizador.nome if self.utilizador else 'utilizador removido'
        return f'{self.criado_em:%Y-%m-%d %H:%M} — {quem} — {self.get_accao_display()}'
