from django.conf import settings
from django.db import models
from expedientes.models import Expediente
 
 
def caminho_upload(instancia, nome_ficheiro):
    """
    Em vez de guardar todos os ficheiros soltos numa unica pasta gigante,
    organizamo-los por expediente: media/expedientes/7/comprovativo.pdf
    Isto tambem evita que dois utilizadores que enviem um ficheiro com
    o MESMO nome (ex.: 'documento.pdf') se sobreponham um ao outro.
    """
    return f'expedientes/{instancia.expediente_id}/{nome_ficheiro}'
 
 
class Documento(models.Model):
    class Categoria(models.TextChoices):
        REQUERIMENTO = 'REQUERIMENTO', 'Requerimento'
        COMPROVATIVO = 'COMPROVATIVO', 'Comprovativo'
        DESPACHO = 'DESPACHO', 'Despacho'
        OUTRO = 'OUTRO', 'Outro'
 
    expediente = models.ForeignKey(
        Expediente, on_delete=models.CASCADE, related_name='documentos'
    )
    # CASCADE aqui (ao contrario do PROTECT em Expediente.criado_por):
    # se um expediente for mesmo apagado, os SEUS documentos deixam
    # de fazer sentido sozinhos, por isso vao juntos.
 
    categoria = models.CharField(max_length=20, choices=Categoria.choices)
    titulo = models.CharField(max_length=150)
    arquivo = models.FileField(upload_to=caminho_upload)
    versao = models.PositiveIntegerField(default=1)
    uploadado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT
    )
    ativo = models.BooleanField(default=True)   # soft delete (ver abaixo)
    criado_em = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.titulo
 
    def soft_delete(self):
        """Nao apagamos o ficheiro fisicamente -- so o marcamos como
        inactivo, para nao aparecer mais nas listagens, mas continuar
        disponivel para auditoria/investigacao se for preciso."""
        self.ativo = False
        self.save(update_fields=['ativo'])
