import os
from django.core.exceptions import ValidationError

from documentos.models import caminho_upload
 
EXTENSOES_PERMITIDAS = ['.pdf', '.jpg', '.jpeg', '.png', '.docx']
TAMANHO_MAXIMO_MB = 5
 
 
def validar_ficheiro(ficheiro):
    # 1) Verificar a extensao (a 'terminacao' do nome do ficheiro)
    extensao = os.path.splitext(ficheiro.name)[1].lower()
    if extensao not in EXTENSOES_PERMITIDAS:
        raise ValidationError(
            f'Tipo de ficheiro nao permitido. Usa: {", ".join(EXTENSOES_PERMITIDAS)}'
        )
 
    # 2) Verificar o tamanho, para evitar que alguem envie um
    #    ficheiro gigante e sobrecarregue o servidor
    limite_bytes = TAMANHO_MAXIMO_MB * 1024 * 1024
    if ficheiro.size > limite_bytes:
        raise ValidationError(f'O ficheiro nao pode exceder {TAMANHO_MAXIMO_MB}MB.')

